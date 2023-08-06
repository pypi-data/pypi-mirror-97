# from pathlib import Path
# import numpy as np
import torch
from collections import OrderedDict


params_aliases = [
    {"old_key_starts": 'surfacepred.p1.',
     "new_key_starts": "surfacepred.fcn.block.1."},
    {"old_key_starts": 'surfacepred.p2.',
     "new_key_starts": "surfacepred.fcn.block.2."},
    {"old_key_starts": 'surfacepred.p3.',
     "new_key_starts": "surfacepred.fcn.block.3."},

    {"old_key_starts": 'refinement.0.p1.',
     "new_key_starts": "refinement.0.fcn.block.1."},
    {"old_key_starts": 'refinement.0.p1.',
     "new_key_starts": "refinement.0.fcn.block.1."},
    {"old_key_starts": 'refinement.0.p2.',
     "new_key_starts": "refinement.0.fcn.block.2."},
    {"old_key_starts": 'refinement.0.p3.',
     "new_key_starts": "refinement.0.fcn.block.3."},
    {"old_key_starts": 'refinement.1.p1.',
     "new_key_starts": "refinement.1.fcn.block.1."},
    {"old_key_starts": 'refinement.1.p1.',
     "new_key_starts": "refinement.1.fcn.block.1."},
    {"old_key_starts": 'refinement.1.p2.',
     "new_key_starts": "refinement.1.fcn.block.2."},
    {"old_key_starts": 'refinement.1.p3.',
     "new_key_starts": "refinement.1.fcn.block.3."},
    {"old_key_starts": 'refinement.2.p1.',
     "new_key_starts": "refinement.2.fcn.block.1."},
    {"old_key_starts": 'refinement.2.p1.',
     "new_key_starts": "refinement.2.fcn.block.1."},
    {"old_key_starts": 'refinement.2.p2.',
     "new_key_starts": "refinement.2.fcn.block.2."},
    {"old_key_starts": 'refinement.2.p3.',
     "new_key_starts": "refinement.2.fcn.block.3."},
]


def model_load_state_dict(model, model_path=None, state=None):
    if model_path is not None:
        state = torch.load(model_path)
    state = replace_aliases(state, params_aliases=params_aliases)
    model.load_state_dict(state)
    return model


def replace_aliases(state, params_aliases=params_aliases):
    res = OrderedDict()
    for key in state.keys():
        a = get_alias(key, params_aliases)
        if a is not None:
            v = state[key]
            res[a['new_key']] = v
        else:
            res[key] = state[key]
    return res


def get_alias(key, params_aliases):
    res = None
    for a in params_aliases:
        if key.startswith(a['old_key_starts']):
            res = a.copy()
            res['new_key'] = key.replace(a['old_key_starts'], a['new_key_starts'])
            break
        elif key.startswith('model.' + a['old_key_starts']):
            res = a.copy()
            res['new_key'] = key.replace('model.' + a['old_key_starts'], 'model.' + a['new_key_starts'])
            break
    return res


def load_model_variants(pl_model, model, model_path):
    d = torch.load(model_path)
    if len(d.keys()) == 3:
        # original, author's weights, or running original authors code
        d = torch.load(model_path)
        print(d.keys())
        print()
        for k in ['epoch']:
            s = f'{k}:'
            print(f'{s:<30} {d.get(k, None)}')
        print()
        state = replace_aliases(d['state_dict'], params_aliases=params_aliases)
        model.load_state_dict(state)
        # del d
    elif model_path.suffix == '.ckpt':
        # pytorch-lightning
        d = torch.load(model_path)
        print(d.keys())
        for k in ['epoch', 'global_step', 'pytorch-lightning_version', 'checkpoint_callback_best_model_score', 'checkpoint_callback_best_model_path',
                  'hparams_name', 'hparams_type']:
            s = f'{k}:'
            print(f'{s:<30} {d.get(k, None)}')
        print()

        # log('state_dict files', d['state_dict']['model.encoder.process_sparse.0.p1.weight'])
        # pl_model.model.load_state_dict(d['state_dict'])

        state = replace_aliases(d['state_dict'], params_aliases=params_aliases)

        pl_model.load_state_dict(state)

        # pl_model = pl_model.load_from_checkpoint(str(model_path))
        # model = pl_model.model
        # log('state_dict after', pl_model.model.state_dict()['encoder.process_sparse.0.p1.weight'])
        # log('state_dict after2',model2.state_dict()['model.encoder.process_sparse.0.p1.weight'])

        del d
    else:
        # pure model dict_state
        state = torch.load(model_path)
        model.load_state_dict(state)

    return pl_model, model


def count_params(model):
    return sum(p.numel() for p in model.parameters())


def sparse_to_tensors(sparse):
    """SparseConvNetTensor --> (locs/coords, features, spatial_size)"""
    return sparse.get_spatial_locations(), sparse.features, sparse.spatial_size
