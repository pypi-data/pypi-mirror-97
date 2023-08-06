from pathlib import Path
from typing import Tuple, Type, Dict, Union, Optional

import numpy as np

import torch

from kekas.callbacks import OneCycleLR, Callbacks
# Callback, Callbacks, ProgressBarCallback, \
#     PredictionsSaverCallback, OneCycleLR, SimpleLossCallback, MetricsCallback, \
#     TBLogger, LRFinder, CheckpointSaverCallback, SimpleSchedulerCallback, \
#     EarlyStoppingCallback, SimpleOptimizerCallback, LRUpdater
from kekas.utils import DotDict
#     get_pbar, exp_weight_average, extend_postfix, to_numpy


# Implement annealing_cos
# https://github.com/fastai/fastai/blob/master/fastai/callbacks/one_cycle.py#L32


def kek_one_cycle(self,
                  max_lr: float,
                  cycle_len: int,
                  momentum_range: Tuple[float, float] = (0.95, 0.85),
                  div_factor: float = 25,
                  increase_fraction: float = 0.3,
                  opt: Optional[Type[torch.optim.Optimizer]] = None,
                  opt_params: Optional[Dict] = None,
                  logdir: Optional[Union[str, Path]] = None,
                  cp_saver_params: Optional[Dict] = None,
                  early_stop_params: Optional[Dict] = None,
                  annealing_cos: bool = False,
                  simulate: bool = False) -> None:
    """Kek your model to the moon with One Cycle policy!

    Conducts a one-cycle train-val procedure with several options for
    customization.
    For info about One Cycle policy please see:
    https://arxiv.org/abs/1803.09820
    https://sgugger.github.io/the-1cycle-policy.html

    Args:
        max_lr: the maximum learning rate that will be achieved during
            training process
        cycle_len: the number of full passes through the training dataset.
            It is quite similar to epochs number
        momentum_range: the range of optimizers momentum changes
        div_factor: is equal to max_lr / min_lr during one-cycle training
        increase_fraction: the fraction of the whole iterations during which
            the learning rate will increase
        opt: torch optimizer. If specified, than specified optimizer will be
            used for this train-val procedure, else the default one.
        opt_params: The kwargs dict for custom optimizer initialization.
            It should contain any opt params you want EXCEPT learning rate,
            Can be defined even for default optimizer.
        logdir: If provided, the TBLogger will be created and tensorboard
            logs will be written in this directory.
            For more info see kekas.callbacks.TBLogger and example ipynb's.
        cp_saver_params: kwargs dict parameters for CheckpointSaverCallback.
            If provided, then a CheckpointSaverCallback will be created.
            For more info see kekas.callbacks.CheckpointSaverCallback
            and example ipynb's.
        early_stop_params: kwargs dict parameters for EarlyStoppingCallback.
            If provided, then a EarlyStoppingCallback will be created.
            For more info see kekas.callbacks.EarlyStoppingCallback
            and example ipynb's.
    """

    callbacks = self.callbacks

    # temporarily add OneCycle callback
    len_loader = len(self.state.core.dataowner.train_dl)
    if annealing_cos:
        OCLR = OneCycleLR_AnnealingCos
    else:
        OCLR = OneCycleLR
    one_cycle_cb = OCLR(max_lr, cycle_len, len_loader,
                        momentum_range, div_factor, increase_fraction)

#   TODO: update on train begin
#    if one_cycle_cb.cut_point == 0:
#        one_cycle_cb.cut_point = 1
#        assert one_cycle_cb.total_iter - one_cycle_cb.cut_point != 0

    if simulate:
        from matplotlib import pyplot as plt
        one_cycle_cb.on_train_begin(None)
        xx = np.arange(one_cycle_cb.total_iter)
        yy = []
        yy_m = []
        for x in xx:
            one_cycle_cb.cycle_iter = x
            yy.append(one_cycle_cb.calc_lr())
            yy_m.append(one_cycle_cb.calc_momentum())
        fig, axes = plt.subplots(ncols=2, figsize=(16, 8))
        ax = axes[0]
        ax.plot(xx, yy)
        ax.set_xlabel('batch')
        ax.set_ylabel('LR')
        ax.set_title('LR')
        ax = axes[1]
        ax.plot(xx, yy_m)
        ax.set_xlabel('batch')
        ax.set_ylabel('momentum')
        ax.set_title('momentum')
        return {'batch_i': xx, 'LR': yy, 'mometum': yy_m}

    else:
        try:
            self.callbacks = Callbacks(callbacks.callbacks + [one_cycle_cb])

            self.kek(lr=max_lr,
                     epochs=cycle_len,
                     opt=opt,
                     opt_params=opt_params,
                     logdir=logdir,
                     cp_saver_params=cp_saver_params,
                     early_stop_params=early_stop_params)
        finally:
            # set old callbacks without OneCycle
            self.callbacks = callbacks


class OneCycleLR_AnnealingCos(OneCycleLR):
    """

    BAsed on OneCycleLR

    https://github.com/belskikh/kekas/blob/master/kekas/callbacks.py
    https://github.com/fastai/fastai/blob/master/fastai/callbacks/one_cycle.py

    An learning rate updater
        that implements the CircularLearningRate (CLR) scheme.
    Learning rate is increased then decreased linearly.
    Inspired by
    https://github.com/fastai/fastai/blob/master/fastai/callbacks/one_cycle.py
    """

    def on_train_begin(self, state: DotDict) -> None:
        self.total_iter = self.len_loader * self.cycle_len - 1
        self.cut_point = int(self.total_iter * self.increase_fraction)

        if self.cut_point == 0:
            self.cut_point = 1
            assert self.total_iter - self.cut_point != 0

    def calc_lr(self) -> float:

        # calculate percent for learning rate change
        if self.cycle_iter <= self.cut_point:
            percent = self.cycle_iter / self.cut_point
        else:
            percent = 1 - (self.cycle_iter - self.cut_point) / (self.total_iter - self.cut_point)

        percent = self.annealing_cos(0, 1, percent)

        res = self.init_lr * (1 + percent * (self.div_factor - 1)) / self.div_factor
        return res

    def calc_momentum(self) -> float:
        if self.cycle_iter <= self.cut_point:
            percent = 1 - self.cycle_iter / self.cut_point

        else:
            percent = (self.cycle_iter - self.cut_point) / (self.total_iter - self.cut_point)

        percent = self.annealing_cos(0, 1, percent)

        res = self.momentum_range[1] + percent * (self.momentum_range[0] - self.momentum_range[1])
        return res

    def annealing_cos(self, start: int, end: int, pct: float) -> float:
        "Cosine anneal from `start` to `end` as pct goes from 0.0 to 1.0."
        cos_out = np.cos(np.pi * pct) + 1
        return end + (start - end) / 2 * cos_out
