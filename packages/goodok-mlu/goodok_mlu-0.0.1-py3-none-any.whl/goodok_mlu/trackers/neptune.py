import inspect
import warnings
from pathlib import Path


def send_model_code(model, model_config, logdir, NEPTUNE_ON=False, exp=None):
    model_init = None
    model_forward = None
    model_config_s = None
    try:
        model_init = inspect.getsource(model.__init__)
    except Exception as e:
        warnings.warn(f"Can't save model_init: {e}", UserWarning)
    try:
        model_forward = inspect.getsource(model.forward)
    except Exception as e:
        warnings.warn(f"Can't save model_forward: {e}", UserWarning)

    try:
        model_config_s = str(model_config)
    except Exception as e:
        warnings.warn(f"Can't save model_config: {e}", UserWarning)

    def save_and_send(src, fnbase):
        if src is not None:
            fn = Path(logdir) / fnbase
            with open(fn, 'w') as f:
                f.write(src)
            if NEPTUNE_ON and exp is not None:
                exp.send_artifact(fn)

    save_and_send(model_init, 'model_init.py')
    save_and_send(model_forward, 'model_forward.py')
    save_and_send(model_config_s, 'model_config.txt')


def log_and_send_string(value, name='example.txt', logdir=None, NEPTUNE_ON=False, exp=None):

    def save_and_send(src, fnbase):
        if src is not None:
            fn = Path(logdir) / fnbase
            with open(fn, 'w') as f:
                f.write(src)
            if NEPTUNE_ON and exp is not None:
                exp.send_artifact(fn)

    save_and_send(value, name)
