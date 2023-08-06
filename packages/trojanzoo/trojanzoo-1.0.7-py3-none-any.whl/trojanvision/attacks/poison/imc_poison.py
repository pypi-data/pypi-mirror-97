#!/usr/bin/env python3

from .poison_basic import PoisonBasic
from trojanvision.attacks import PGD
from trojanvision.defenses.adv.curvature import Curvature
from trojanvision.optim import PGD as PGD_Optimizer
from trojanvision.models import MagNet
from trojanzoo.utils import to_list

import torch
import numpy as np
import os
from scipy.stats import ks_2samp
import argparse


class IMC_Poison(PoisonBasic):

    name: str = 'imc_poison'

    # TODO: change PGD to Uname.optimizer
    @classmethod
    def add_argument(cls, group: argparse._ArgumentGroup):
        super().add_argument(group)
        group.add_argument('--pgd_alpha', dest='pgd_alpha', type=float)
        group.add_argument('--pgd_epsilon', dest='pgd_epsilon', type=float)
        group.add_argument('--pgd_iteration', dest='pgd_iteration', type=int)
        group.add_argument('--stop_conf', dest='stop_conf', type=float)

        group.add_argument('--magnet', dest='magnet', action='store_true')
        group.add_argument('--randomized_smooth', dest='randomized_smooth', action='store_true')
        group.add_argument('--curvature', dest='curvature', action='store_true')

    def __init__(self, pgd_alpha: float = 1.0, pgd_epsilon: float = 8.0, pgd_iteration: int = 8,
                 stop_conf: float = 0.9,
                 magnet: bool = False, randomized_smooth: bool = False, curvature: bool = False, **kwargs):
        super().__init__(**kwargs)
        self.param_list['pgd'] = ['pgd_alpha', 'pgd_epsilon', 'pgd_iteration']
        self.pgd_alpha: float = pgd_alpha
        self.pgd_epsilon: float = pgd_epsilon
        self.pgd_iteration: int = pgd_iteration
        self.pgd = PGD_Optimizer(alpha=self.pgd_alpha / 255, epsilon=self.pgd_epsilon / 255,
                                 iteration=self.pgd_iteration)
        self.stop_conf: float = stop_conf
        if magnet:
            self.magnet: MagNet = MagNet(dataset=self.dataset, pretrain=True)
        self.randomized_smooth: bool = randomized_smooth
        if curvature:
            self.curvature: Curvature = Curvature(model=self.model)

    def attack(self, epoch: int, **kwargs):
        # model._validate()
        total = 0
        target_conf_list = []
        target_acc_list = []
        clean_acc_list = []
        pgd_norm_list = []
        alpha = 1.0 / 255
        epsilon = 8.0 / 255
        if self.dataset.name in ['cifar10', 'gtsrb', 'isic2018']:
            alpha = 1.0 / 255
            epsilon = 8.0 / 255
        if self.dataset.name in ['sample_imagenet', 'sample_vggface2']:
            alpha = 0.25 / 255
            epsilon = 2.0 / 255
        pgd_checker = PGD(alpha=alpha, epsilon=epsilon, iteration=8,
                          dataset=self.dataset, model=self.model, target_idx=self.target_idx, stop_threshold=0.95)
        easy = 0
        difficult = 0
        normal = 0
        loader = self.dataset.get_dataloader(mode='valid', batch_size=self.dataset.test_batch_size)
        if 'curvature' in self.__dict__.keys():
            benign_curvature = self.curvature.benign_measure()
            tgt_curvature_list = []
            org_curvature_list = []
        if self.randomized_smooth:
            org_conf_list = []
            tgt_conf_list = []
        if 'magnet' in self.__dict__.keys():
            org_magnet_list = []
            tgt_magnet_list = []
        for data in loader:
            print(easy, normal, difficult)
            if normal >= 100:
                break
            self.model.load()
            _input, _label = self.model.remove_misclassify(data)
            if len(_label) == 0:
                continue
            target_label = self.model.generate_target(_input, idx=self.target_idx)
            self.temp_input = _input
            self.temp_label = target_label
            _, _iter = pgd_checker.craft_example(_input)
            if _iter is None:
                difficult += 1
                continue
            if _iter < 4:
                easy += 1
                continue
            normal += 1
            target_conf, target_acc, clean_acc = self.validate_fn()
            noise = torch.zeros_like(_input)
            poison_input = self.craft_example(_input=_input, _label=target_label, epoch=epoch, noise=noise, **kwargs)
            pgd_norm = float(noise.norm(p=float('inf')))
            target_conf, target_acc, clean_acc = self.validate_fn()
            target_conf_list.append(target_conf)
            target_acc_list.append(target_acc)
            clean_acc_list.append(max(self.clean_acc - clean_acc, 0.0))
            pgd_norm_list.append(pgd_norm)
            print(f'[{total+1} / 100]\n'
                  f'target confidence: {np.mean(target_conf_list)}({np.std(target_conf_list)})\n'
                  f'target accuracy: {np.mean(target_acc_list)}({np.std(target_acc_list)})\n'
                  f'clean accuracy Drop: {np.mean(clean_acc_list)}({np.std(clean_acc_list)})\n'
                  f'PGD Norm: {np.mean(pgd_norm_list)}({np.std(pgd_norm_list)})\n\n\n')
            org_conf = self.model.get_target_prob(_input=poison_input, target=_label)
            tgt_conf = self.model.get_target_prob(_input=poison_input, target=target_label)
            if 'curvature' in self.__dict__.keys():
                org_curvature_list.extend(to_list(self.curvature.measure(poison_input, _label)))    # type: ignore
                tgt_curvature_list.extend(to_list(self.curvature.measure(poison_input, target_label)))    # type: ignore
                print('Curvature:')
                print(f'    org_curvature: {ks_2samp(org_curvature_list, benign_curvature)}')    # type: ignore
                print(f'    tgt_curvature: {ks_2samp(tgt_curvature_list, benign_curvature)}')    # type: ignore
                print()
            if self.randomized_smooth:
                org_new = self.model.get_target_prob(_input=poison_input, target=_label, randomized_smooth=True)
                tgt_new = self.model.get_target_prob(_input=poison_input, target=target_label, randomized_smooth=True)
                org_increase = (org_new - org_conf).clamp(min=0.0)
                tgt_decrease = (tgt_new - tgt_conf).clamp(min=0.0)
                org_conf_list.extend(to_list(org_increase))    # type: ignore
                tgt_conf_list.extend(to_list(tgt_decrease))    # type: ignore
                print('Randomized Smooth:')
                print(f'    org_confidence: {np.mean(org_conf_list)}')    # type: ignore
                print(f'    tgt_confidence: {np.mean(tgt_conf_list)}')    # type: ignore
                print()
            if 'magnet' in self.__dict__.keys():
                poison_input = self.magnet(poison_input)
                org_new = self.model.get_target_prob(_input=poison_input, target=_label)
                tgt_new = self.model.get_target_prob(_input=poison_input, target=target_label)
                org_increase = (org_new - org_conf).clamp(min=0.0)
                tgt_decrease = (tgt_conf - tgt_new).clamp(min=0.0)
                org_magnet_list.extend(to_list(org_increase))    # type: ignore
                tgt_magnet_list.extend(to_list(tgt_decrease))    # type: ignore
                print('MagNet:')
                print(f'    org_confidence: {np.mean(org_magnet_list)}')    # type: ignore
                print(f'    tgt_confidence: {np.mean(tgt_magnet_list)}')    # type: ignore
                print()
            total += 1

    def craft_example(self, _input: torch.Tensor, _label: torch.Tensor, noise: torch.Tensor = None, save=False, **kwargs):
        if noise is None:
            noise = torch.zeros_like(_input)
        poison_input = None
        for _iter in range(self.pgd_iteration):
            target_conf, target_acc = self.validate_target(indent=4, verbose=False)
            if target_conf > self.stop_conf:
                break
            poison_input, _ = self.pgd.optimize(_input, noise=noise, loss_fn=self.loss_pgd, iteration=1)
            self.temp_input = poison_input
            target_conf, target_acc = self.validate_target(indent=4, verbose=False)
            if target_conf > self.stop_conf:
                break
            self._train(_input=poison_input, _label=_label, **kwargs)
        target_conf, target_acc = self.validate_target(indent=4, verbose=False)
        return poison_input

    def save(self, **kwargs):
        filename = self.get_filename(**kwargs)
        file_path = os.path.join(self.folder_path, filename)
        self.model.save(file_path + '.pth')
        print('attack results saved at: ', file_path)

    def get_filename(self, **kwargs):
        return self.model.name

    def loss_pgd(self, x: torch.Tensor) -> torch.Tensor:
        return self.model.loss(x, self.temp_label)
