#!/usr/bin/env python3
from .imagemodel import _ImageModel, ImageModel
from trojanvision.utils.dla import BasicBlock, Tree, SimpleTree

import torch.nn as nn


class _DLA(_ImageModel):

    def __init__(self, **kwargs):
        super().__init__(conv_dim=512, fc_depth=1, **kwargs)

    @staticmethod
    def define_features(block=BasicBlock, simple: bool = False, **kwargs) -> nn.Sequential:
        TreeClass = SimpleTree if simple else Tree
        features = nn.Sequential()
        features.add_module('base', nn.Sequential(
            nn.Conv2d(3, 16, kernel_size=3, stride=1, padding=1, bias=False),
            nn.BatchNorm2d(16),
            nn.ReLU(True)
        ))
        features.add_module('layer1', nn.Sequential(
            nn.Conv2d(16, 16, kernel_size=3, stride=1, padding=1, bias=False),
            nn.BatchNorm2d(16),
            nn.ReLU(True)
        ))
        features.add_module('layer2', nn.Sequential(
            nn.Conv2d(16, 32, kernel_size=3, stride=1, padding=1, bias=False),
            nn.BatchNorm2d(32),
            nn.ReLU(True)
        ))
        features.add_module('layer3', TreeClass(block, 32, 64, level=1, stride=1))
        features.add_module('layer4', TreeClass(block, 64, 128, level=1, stride=1))
        features.add_module('layer5', TreeClass(block, 128, 256, level=1, stride=1))
        features.add_module('layer6', TreeClass(block, 256, 512, level=1, stride=1))
        return features


class DLA(ImageModel):

    def __init__(self, name: str = 'dla', simple: bool = None,
                 model_class: type[_DLA] = _DLA, **kwargs):
        if name == 'dlasimple' and simple is None:
            simple = True
        elif simple:
            name = 'dlasimple'
        super().__init__(name=name, model_class=model_class, simple=simple, **kwargs)
