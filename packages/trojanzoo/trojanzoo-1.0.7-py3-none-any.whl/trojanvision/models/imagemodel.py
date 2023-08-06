#!/usr/bin/env python3

from trojanvision.datasets import ImageSet
from trojanzoo.models import _Model, Model
from trojanvision.utils import apply_cmap

import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.transforms as transforms
import re
import functools


from typing import TYPE_CHECKING
from torch.utils.tensorboard import SummaryWriter
from torch.optim.optimizer import Optimizer
from torch.optim.lr_scheduler import _LRScheduler
from torchvision.transforms import Normalize
import argparse
from matplotlib.colors import Colormap
from collections.abc import Callable
if TYPE_CHECKING:
    import torch.autograd
    import torch.nn
    import torch.cuda.amp
    import torch.utils.data

from matplotlib.cm import get_cmap
jet = get_cmap('jet')


class _ImageModel(_Model):
    module_list = ['normalize', 'features', 'pool', 'flatten', 'classifier', 'softmax']
    filter_tuple: tuple[nn.Module] = (transforms.Normalize,
                                      nn.Dropout, nn.BatchNorm2d,
                                      nn.ReLU, nn.Sigmoid)

    def __init__(self, norm_par: dict[str, list[float]] = {'mean': [0.0], 'std': [1.0]},
                 num_classes=None, **kwargs):
        if num_classes is None:
            num_classes = 1000
        super().__init__(num_classes=num_classes, norm_par=norm_par, **kwargs)

    def define_preprocess(self, norm_par: dict[str, list[float]] = {'mean': [0.0], 'std': [1.0]}, **kwargs):
        self.normalize = Normalize(mean=norm_par['mean'], std=norm_par['std'])

    # get feature map
    # input: (batch_size, channels, height, width)
    # output: (batch_size, [feature_map])
    def get_fm(self, x: torch.Tensor) -> torch.Tensor:
        return self.features(self.normalize(x))


class ImageModel(Model):

    @ classmethod
    def add_argument(cls, group: argparse._ArgumentGroup):
        super().add_argument(group)
        group.add_argument('--layer', dest='layer', type=int,
                           help='layer (optional, maybe embedded in --model)')
        group.add_argument('--width_factor', dest='width_factor', type=int,
                           help='width factor for wide-ResNet (optional, maybe embedded in --model)')
        group.add_argument('--sgm', dest='sgm', action='store_true',
                           help='whether to use sgm gradient, defaults to False')
        group.add_argument('--sgm_gamma', dest='sgm_gamma', type=float,
                           help='sgm gamma, defaults to 1.0')
        return group

    def __init__(self, name: str = 'imagemodel', layer: int = None, width_factor: int = None,
                 model_class: type[_ImageModel] = _ImageModel, dataset: ImageSet = None,
                 sgm: bool = False, sgm_gamma: float = 1.0, **kwargs):
        name, layer, width_factor = self.split_model_name(name, layer=layer, width_factor=width_factor)
        self.layer = layer
        self.width_factor = width_factor
        if 'norm_par' not in kwargs.keys() and isinstance(dataset, ImageSet):
            kwargs['norm_par'] = dataset.norm_par
        if 'num_classes' not in kwargs.keys() and dataset is None:
            kwargs['num_classes'] = 1000
        super().__init__(name=name, model_class=model_class, layer=layer, width_factor=width_factor, dataset=dataset, **kwargs)
        self.sgm: bool = sgm
        self.sgm_gamma: float = sgm_gamma
        self.param_list['imagemodel'] = ['layer', 'width_factor', 'sgm']
        if sgm:
            self.param_list['imagemodel'].extend(['sgm_gamma'])
        self._model: _ImageModel
        self.dataset: ImageSet
        self.pgd = None  # TODO: python 3.10 type annotation
        self.ce_loss_fn = torch.nn.CrossEntropyLoss(weight=self.loss_weights)

    def adv_loss(self, _input: torch.Tensor, _label: torch.Tensor) -> torch.Tensor:
        _output = self(_input)
        return -self.ce_loss_fn(_output, _label)

    def get_data(self, data: tuple[torch.Tensor, torch.Tensor], adv: bool = False, **kwargs) -> tuple[torch.Tensor, torch.Tensor]:
        if adv and self.pgd is not None:
            _input, _label = super().get_data(data, **kwargs)
            adv_loss_fn = functools.partial(self.adv_loss, _label=_label)
            adv_x, _ = self.pgd.optimize(_input=_input, loss_fn=adv_loss_fn)
            return adv_x, _label
        return super().get_data(data, **kwargs)

    # TODO: requires _input shape (N, C, H, W)
    # Reference: https://keras.io/examples/vision/grad_cam/
    def get_heatmap(self, _input: torch.Tensor, _label: torch.Tensor, method: str = 'grad_cam', cmap: Colormap = jet) -> torch.Tensor:
        squeeze_flag = False
        if _input.dim() == 3:
            _input = _input.unsqueeze(0)    # (N, C, H, W)
            squeeze_flag = True
        if isinstance(_label, int):
            _label = [_label] * len(_input)
        _label = torch.as_tensor(_label, device=_input.device)
        heatmap = _input    # linting purpose
        if method == 'grad_cam':
            feats = self._model.get_fm(_input).detach()   # (N, C', H', W')
            feats.requires_grad_()
            _output: torch.Tensor = self._model.pool(feats)   # (N, C', 1, 1)
            _output = self._model.flatten(_output)   # (N, C')
            _output = self._model.classifier(_output)   # (N, num_classes)
            _output = _output.gather(dim=1, index=_label.unsqueeze(1)).sum()
            grad = torch.autograd.grad(_output, feats)[0]   # (N, C',H', W')
            feats.requires_grad_(False)
            weights = grad.mean(dim=-2, keepdim=True).mean(dim=-1, keepdim=True)    # (N, C',1,1)
            heatmap = (feats * weights).sum(dim=1, keepdim=True).clamp(0)  # (N, 1, H', W')
            # heatmap.sub_(heatmap.min(dim=-2, keepdim=True)[0].min(dim=-1, keepdim=True)[0])
            heatmap.div_(heatmap.max(dim=-2, keepdim=True)[0].max(dim=-1, keepdim=True)[0])
            heatmap: torch.Tensor = F.upsample(heatmap, _input.shape[-2:], mode='bilinear')[:, 0]   # (N, H, W)
            # Note that we violate the image order convension (W, H, C)
        elif method == 'saliency_map':
            _input.requires_grad_()
            _output = self(_input).gather(dim=1, index=_label.unsqueeze(1)).sum()
            grad = torch.autograd.grad(_output, _input)[0]   # (N,C,H,W)
            _input.requires_grad_(False)

            heatmap = grad.abs().max(dim=1)[0]   # (N,H,W)
            heatmap.sub_(heatmap.min(dim=-2, keepdim=True)[0].min(dim=-1, keepdim=True)[0])
            heatmap.div_(heatmap.max(dim=-2, keepdim=True)[0].max(dim=-1, keepdim=True)[0])
        heatmap = apply_cmap(heatmap.detach().cpu(), cmap)
        return heatmap[0] if squeeze_flag else heatmap

    @ staticmethod
    def split_model_name(name: str, layer: int = None, width_factor: int = None) -> tuple[str, int, int]:
        re_list = re.findall(r'[0-9]+|[a-z]+|_', name)
        if len(re_list) > 1:
            name = re_list[0]
            layer = int(re_list[1])
        if len(re_list) > 2 and re_list[-2] == 'x':
            width_factor = int(re_list[-1])
        if layer is not None:
            name += str(layer)
        if width_factor is not None:
            name += f'x{width_factor:d}'
        return name, layer, width_factor

    def _train(self, epoch: int, optimizer: Optimizer, lr_scheduler: _LRScheduler = None,
               print_prefix: str = 'Epoch', start_epoch: int = 0,
               validate_interval: int = 10, save: bool = False, amp: bool = False,
               loader_train: torch.utils.data.DataLoader = None, loader_valid: torch.utils.data.DataLoader = None,
               epoch_fn: Callable[..., None] = None,
               get_data_fn: Callable[..., tuple[torch.Tensor, torch.Tensor]] = None,
               loss_fn: Callable[..., torch.Tensor] = None,
               after_loss_fn: Callable[..., None] = None,
               validate_fn: Callable[..., tuple[float, float]] = None,
               save_fn: Callable[..., None] = None, file_path: str = None, folder_path: str = None, suffix: str = None,
               writer: SummaryWriter = None, main_tag: str = 'train', tag: str = '',
               verbose: bool = True, indent: int = 0,
               adv_train: bool = False, adv_train_alpha: float = 2.0 / 255, adv_train_epsilon: float = 8.0 / 255,
               adv_train_iter: int = 7, adv_train_valid_epsilon: float = 8.0 / 255, **kwargs):
        if adv_train:
            after_loss_fn_old = after_loss_fn
            if not callable(after_loss_fn) and hasattr(self, 'after_loss_fn'):
                after_loss_fn_old = getattr(self, 'after_loss_fn')
            validate_fn_old = validate_fn if callable(validate_fn) else self._validate
            loss_fn = loss_fn if callable(loss_fn) else self.loss
            from trojanvision.optim import PGD  # TODO: consider to move import sentences to top of file
            self.pgd = PGD(alpha=adv_train_alpha, epsilon=adv_train_valid_epsilon,
                           iteration=adv_train_iter, stop_threshold=None)

            def after_loss_fn_new(_input: torch.Tensor, _label: torch.Tensor, _output: torch.Tensor,
                                  loss: torch.Tensor, optimizer: Optimizer, loss_fn: Callable[..., torch.Tensor] = None,
                                  amp: bool = False, scaler: torch.cuda.amp.GradScaler = None, **kwargs):
                noise = torch.zeros_like(_input)
                adv_loss_fn = functools.partial(self.adv_loss, _label=_label)

                for m in range(self.pgd.iteration):
                    if amp:
                        scaler.step(optimizer)
                        scaler.update()
                    else:
                        optimizer.step()
                    self.eval()
                    adv_x, _ = self.pgd.optimize(_input=_input, noise=noise,
                                                 loss_fn=adv_loss_fn,
                                                 iteration=1, epsilon=adv_train_epsilon)
                    self.train()
                    loss = loss_fn(adv_x, _label)
                    if callable(after_loss_fn_old):
                        after_loss_fn_old(_input=_input, _label=_label, _output=_output,
                                          loss=loss, optimizer=optimizer, loss_fn=loss_fn,
                                          amp=amp, scaler=scaler, **kwargs)
                    if amp:
                        scaler.scale(loss).backward()
                    else:
                        loss.backward()

            def validate_fn_new(get_data_fn: Callable[..., tuple[torch.Tensor, torch.Tensor]] = None,
                                print_prefix: str = 'Validate', **kwargs) -> tuple[float, float]:
                _, clean_acc = validate_fn_old(print_prefix='Validate Clean', main_tag='valid clean',
                                               get_data_fn=None, **kwargs)
                _, adv_acc = validate_fn_old(print_prefix='Validate Adv', main_tag='valid adv',
                                             get_data_fn=functools.partial(get_data_fn, adv=True), **kwargs)
                return adv_acc, clean_acc

            after_loss_fn = after_loss_fn_new
            validate_fn = validate_fn_new

        super()._train(epoch=epoch, optimizer=optimizer, lr_scheduler=lr_scheduler,
                       print_prefix=print_prefix, start_epoch=start_epoch,
                       validate_interval=validate_interval, save=save, amp=amp,
                       loader_train=loader_train, loader_valid=loader_valid,
                       epoch_fn=epoch_fn, get_data_fn=get_data_fn, loss_fn=loss_fn, after_loss_fn=after_loss_fn, validate_fn=validate_fn,
                       save_fn=save_fn, file_path=file_path, folder_path=folder_path, suffix=suffix,
                       writer=writer, main_tag=main_tag, tag=tag, verbose=verbose, indent=indent, **kwargs)
