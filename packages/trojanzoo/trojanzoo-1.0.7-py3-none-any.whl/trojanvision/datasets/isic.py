#!/usr/bin/env python3

from .imagefolder import ImageFolder
from trojanvision.environ import env

import numpy as np
import os
import shutil
import pandas as pd
from tqdm import tqdm

from trojanvision import __file__ as root_file
root_dir = os.path.dirname(root_file)


class ISIC(ImageFolder):

    name: str = 'isic'
    data_shape = [3, 224, 224]
    valid_set: bool = False

    def initialize_folder(self, **kwargs):
        super().initialize_folder(**kwargs)
        self.split_class()

    def split_class(self):
        csv_path = os.path.normpath(os.path.join(root_dir, 'data', self.name, 'label.csv'))
        print(f'Collect Label Information from CSV file: {csv_path}')
        obj = pd.read_csv(csv_path)
        labels = list(obj.columns.values)
        org_dict = {}
        for label in labels:
            org_dict[label] = np.array(obj[label]) if label == 'image' else np.array([
                bool(value) for value in obj[label]])
        new_dict = {}
        for label in labels[1:]:
            new_dict[label] = org_dict['image'][org_dict[label]]

        print('Splitting dataset to class folders ...')
        src_folder = os.path.normpath(os.path.join(self.folder_path, self.name, 'train'))
        if env['tqdm']:
            labels = tqdm(labels[1:])
        for label in labels:
            seq = new_dict[label]
            dst_folder = os.path.join(src_folder, label)
            if not os.path.exists(dst_folder):
                os.makedirs(dst_folder)
            for img in seq:
                src = os.path.join(src_folder, img + '.jpg')
                dest = os.path.join(dst_folder, img + '.jpg')
                shutil.move(src, dest)


class ISIC2018(ISIC):

    name: str = 'isic2018'
    num_classes = 7
    url = {'train': 'https://isic-challenge-data.s3.amazonaws.com/2018/ISIC2018_Task3_Training_Input.zip'}
    md5 = {'train': '0c281f121070a8d63457caffcdec439a'}
    org_folder_name = {'train': 'ISIC2018_Task3_Training_Input'}
