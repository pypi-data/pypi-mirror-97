import warnings
warnings.filterwarnings('ignore')  # noqa

import logging

import matplotlib
matplotlib.use('Agg')  # noqa
from albumentations import BboxParams

import numpy as np
import torch

from rastervision.pytorch_learner.learner import Learner
from rastervision.pytorch_learner.object_detection_utils import (
    MyFasterRCNN, compute_coco_eval, collate_fn, plot_xyz)

log = logging.getLogger(__name__)


class ObjectDetectionLearner(Learner):
    def build_model(self):
        # TODO we shouldn't need to pass the image size here
        pretrained = self.cfg.model.pretrained
        model = MyFasterRCNN(
            self.cfg.model.get_backbone_str(),
            len(self.cfg.data.class_names),
            self.cfg.data.img_sz,
            pretrained=pretrained)
        return model

    def build_metric_names(self):
        metric_names = [
            'epoch', 'train_time', 'valid_time', 'train_loss', 'map', 'map50'
        ]
        return metric_names

    def get_bbox_params(self):
        return BboxParams(
            format='albumentations', label_fields=['category_id'])

    def get_collate_fn(self):
        return collate_fn

    def train_step(self, batch, batch_ind):
        x, y = batch
        loss_dict = self.model(x, y)
        return {'train_loss': loss_dict['total_loss']}

    def validate_step(self, batch, batch_ind):
        x, y = batch
        outs = self.model(x)
        ys = self.to_device(y, 'cpu')
        outs = self.to_device(outs, 'cpu')

        return {'ys': ys, 'outs': outs}

    def validate_end(self, outputs, num_samples):
        outs = []
        ys = []
        for o in outputs:
            outs.extend(o['outs'])
            ys.extend(o['ys'])
        num_class_ids = len(self.cfg.data.class_names)
        coco_eval = compute_coco_eval(outs, ys, num_class_ids)

        metrics = {'map': 0.0, 'map50': 0.0}
        if coco_eval is not None:
            coco_metrics = coco_eval.stats
            metrics = {'map': coco_metrics[0], 'map50': coco_metrics[1]}
        return metrics

    def numpy_predict(self, x: np.ndarray,
                      raw_out: bool = False) -> np.ndarray:
        transform, _ = self.get_data_transforms()
        x = self.normalize_input(x)
        x = self.to_batch(x)
        x = np.stack([
            transform(image=img, bboxes=[], category_id=[])['image']
            for img in x
        ])
        x = torch.from_numpy(x)
        x = x.permute((0, 3, 1, 2))
        out = self.predict(x, raw_out=raw_out)
        return self.output_to_numpy(out)

    def output_to_numpy(self, out):
        numpy_out = []
        for boxlist in out:
            boxlist = boxlist.cpu()
            numpy_out.append({
                'boxes':
                boxlist.boxes.numpy(),
                'class_ids':
                boxlist.get_field('class_ids').numpy(),
                'scores':
                boxlist.get_field('scores').numpy()
            })
        return numpy_out

    def plot_xyz(self, ax, x, y, z=None):
        plot_xyz(ax, x, y, self.cfg.data.class_names, z=z)

    def prob_to_pred(self, x):
        return x
