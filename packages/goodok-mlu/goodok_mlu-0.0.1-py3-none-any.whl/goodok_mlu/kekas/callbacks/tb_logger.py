from collections import defaultdict
from pathlib import Path
from typing import Union

import numpy as np
from tensorboardX import SummaryWriter
from kekas.utils import DotDict, get_opt_lr

from kekas.callbacks import Callback

__all__ = ['TBLogger']


class TBLogger(Callback):
    def __init__(self, logdir: Union[str, Path]) -> None:
        self.logdir = Path(logdir)
        self.writer = None
        self.total_iter = 0
        self.train_iter = 0
        self.val_iter = 0
        self.train_batch_iter = 0
        self.val_batch_iter = 0
        self.train_metrics = defaultdict(list)
        self.val_metrics = defaultdict(list)
        self.total_epoch_iter = 0

    def update_total_iter(self, mode: str) -> None:
        if mode == "train":
            self.train_iter += 1
            self.train_batch_iter += 1
        if mode == "val":
            self.val_iter += 1
            self.val_batch_iter += 1
        self.total_iter += 1

    def on_train_begin(self, state: DotDict) -> None:
        # self.train_iter = 0
        # self.val_iter = 0
        self.logdir.mkdir(exist_ok=True)
        self.train_writer = SummaryWriter(str(self.logdir / "train"))
        self.val_writer = SummaryWriter(str(self.logdir / "val"))
        self.train_metrics = defaultdict(list)
        self.val_metrics = defaultdict(list)

    def on_epoch_begin(self, epoch: int, epochs: int, state: DotDict):
        self.train_batch_iter = 0
        self.val_batch_iter = 0

    def on_batch_end(self, i: int, state: DotDict) -> None:
        if state.core.mode == "train":
            for name, metric in state.core.metrics["train"].items():
                self.train_writer.add_scalar(f"batch/{name}",
                                             float(metric),
                                             global_step=self.total_iter)
                self.train_metrics[name].append(float(metric))

            lr = get_opt_lr(state.core.opt)
            self.train_writer.add_scalar("batch/lr",
                                         float(lr),
                                         global_step=self.train_iter)

            self.update_total_iter(state.core.mode)

        elif state.core.mode == "val":
            for name, metric in state.core.metrics["val"].items():
                self.val_writer.add_scalar(f"batch/{name}",
                                           float(metric),
                                           global_step=self.total_iter)
                self.val_metrics[name].append(float(metric))

            self.update_total_iter(state.core.mode)

    def on_epoch_end(self, epoch: int, state: DotDict) -> None:

        epoch = self.total_epoch_iter

        if state.core.mode == "train":
            for name, metric in self.train_metrics.items():
                mean = np.mean(metric[-self.train_batch_iter:])
                self.train_writer.add_scalar(f"epoch/{name}",
                                             float(mean),
                                             global_step=epoch)
        if state.core.mode == "val":
            for name, metric in self.val_metrics.items():
                mean = np.mean(metric[-self.val_batch_iter:])  # last epochs vals
                self.val_writer.add_scalar(f"epoch/{name}",
                                           float(mean),
                                           global_step=epoch)

            for name, param in state.core.model.named_parameters():
                self.val_writer.add_histogram(name, param.clone().cpu().data.numpy(), epoch)

            self.total_epoch_iter += 1

    def on_train_end(self, state: DotDict) -> None:
        self.train_writer.close()
        self.val_writer.close()
