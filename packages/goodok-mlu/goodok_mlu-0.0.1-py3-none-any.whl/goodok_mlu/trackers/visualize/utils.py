from typing import Any, Dict, Hashable, List, Optional, Union
import numpy as np
import warnings
from matplotlib import pyplot as plt
from IPython.display import display, FileLink, HTML
from pathlib import Path
from tensorboard.backend.event_processing.event_accumulator import EventAccumulator, ScalarEvent

import plotly.graph_objs as go


def plot_lr_loss(logdir, fn_save=None):
    fig, ax = plt.subplots(figsize=(8, 8))

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")

        train_scalars = get_tensorboard_scalars(logdir + '/train', metrics=['loss', 'lr'], step='batch')
        tm_loss = get_scatter(train_scalars, 'batch/loss', prefix='train/')
        tm_lr = get_scatter(train_scalars, 'batch/lr', prefix='train/')

    ax.plot(np.log10(tm_lr['y']), np.log10(tm_loss['y']))
    ax.set_title('LR finder results:')
    ax.set_xlabel('lg(lr)')
    ax.set_ylabel('lg(loss)')

    if fn_save is None:
        plt.show()
    else:
        plt.savefig(fn_save)
        plt.close(fig)
        display(FileLink(Path(fn_save)))
        # return Image(filename=fn_animation)
        display(HTML(f"<img src='{fn_save}' />"))


def plot_metrics(logdir, step="batch",
                 metrics: Union[Any, List, Hashable] = None,
                 log10=False, alpha=0.8, multiruns=True,
                 fn_save=None,
                 ):

    logdir = Path(logdir)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")

        if multiruns:
            train_scalars = get_tensorboard_scalars_multiruns(logdir / 'train', metrics=metrics, step=step)
            val_scalars = get_tensorboard_scalars_multiruns(logdir / 'val', metrics=metrics, step=step)
        else:
            train_scalars = get_tensorboard_scalars(logdir / 'train', metrics=metrics, step=step)
            val_scalars = get_tensorboard_scalars(logdir / 'val', metrics=metrics, step=step)

    n = len(train_scalars)
    fig, axes = plt.subplots(figsize=(8 * n, 8), ncols=n)
    if n == 1:
        axes = [axes]

    for m, ax in zip(train_scalars, axes):

        tm = get_scatter(train_scalars, m, prefix="train/", multiruns=multiruns)
        try:
            vm = get_scatter(val_scalars, m, prefix="val/", multiruns=multiruns)
            data = [tm, vm]
        except:
            data = [tm]

        ax.set_title(m)
        for tm in data:
            x = tm['x']
            y = tm['y']
            if log10:
                y = np.log10(y)

            label = tm['name'].split('/')[0]

            ax.plot(x, y, label=label, alpha=alpha)
            # ax.plot(y, label=label, alpha=alpha)
        ax.set_xlabel(step)
        if log10:
            ax.set_ylabel('log10({m})')

        ax.legend()

    if fn_save is None:
        plt.show()
    else:
        plt.savefig(fn_save)
        plt.close(fig)
        display(FileLink(Path(fn_save)))
        # return Image(filename=fn_animation)
        display(HTML(f"<img src='{fn_save}' />"))


# from kekas.utils
def get_tensorboard_scalars(
    logdir: str, metrics: Optional[List[str]], step: str
) -> Dict[str, List]:
    event_acc = EventAccumulator(str(logdir))
    event_acc.Reload()

    if metrics is not None:
        scalar_names = [
            n for n in event_acc.Tags()["scalars"] if step in n and any(m in n for m in metrics)
        ]
    else:
        scalar_names = [n for n in event_acc.Tags()["scalars"] if step in n]

    scalars = {sn: event_acc.Scalars(sn) for sn in scalar_names}
    return scalars


def get_tensorboard_scalars_multiruns(
    logdir: str, metrics: Optional[List[str]], step: str
) -> Dict[str, List]:

    scalars = get_tensorboard_scalars(logdir, metrics, step)
    # print(scalars)
    return scalars


def get_scatter(scalars: Dict[str, ScalarEvent], name: str, prefix: str, multiruns=False) -> go.Scatter:
    xs = [s.step for s in scalars[name]]
    if multiruns:
        xs = list(range(0, len(xs)))
    ys = [s.value for s in scalars[name]]

    return go.Scatter(x=xs, y=ys, name=prefix + name)
