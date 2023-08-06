from pathlib import Path
import numpy as np
import torch
import json


path_root = DIR_THIS = Path('.').absolute()


def full_path(fn, path=None):
    if path is None:
        return Path(fn)
    else:
        return Path(path) / fn


def load_tensor(fn, to_cuda=False, path=None):
    fn = full_path(fn, path)
    fn = fn.with_suffix('.npy')
    res = np.load(fn)
    res = torch.from_numpy(res)
    if to_cuda:
        res = res.cuda()
    return res


def load_tensor_list(fn, to_cuda=False, path=None, n=4):
    fn = full_path(fn, path)
    res = []
    for i in range(n):
        fn_i = fn.with_suffix(f'.{i}.npy')
        v = np.load(fn_i)
        v = torch.from_numpy(v)
        if to_cuda:
            v = v.cuda()
        res.append(v)
    return res


def load_coords_features(fn, features_to_device=False, path=None):
    fn = full_path(fn, path)
    fn1 = fn.with_suffix('.coords.npy')
    fn2 = fn.with_suffix('.features.npy')

    coords = torch.from_numpy(np.load(fn1))
    features = torch.from_numpy(np.load(fn2))
    if features_to_device:
        features = features.cuda()

    return [coords, features]


def save_tensor(fn, x, from_cuda=False, path=None, verbose=False):
    fn = full_path(fn, path)
    fn = fn.with_suffix('.npy')
    if from_cuda:
        x = x.cpu().detach().numpy()
    np.save(fn, x)
    if verbose:
        print(f'{fn} saved')


def save_tensor_list(fn, x, from_cuda=False, path=None, verbose=False):
    fn = full_path(fn, path)
    for i, v in enumerate(x):
        fn_i = fn.with_suffix(f'.{i}.npy')
        if from_cuda:
            v = v.cpu().detach().numpy()
        np.save(fn_i, v)

        if verbose:
            print(f'{fn_i} saved')


def save_coords_features(fn, coords_features, spatial_size=None, path=None, verbose=False):
    fn = full_path(fn, path)
    fn1 = fn.with_suffix('.coords.npy')
    fn2 = fn.with_suffix('.features.npy')

    np.save(fn1, coords_features[0].cpu().detach())
    np.save(fn2, coords_features[1].cpu().detach())

    if verbose:
        print(f'{fn1} saved')
        print(f'{fn2} saved')

    if spatial_size is not None:
        fn3 = fn.with_suffix('.size.npy')
        np.save(fn3, spatial_size)
        if verbose:
            print(f'{fn3} saved')


def save_json(fn, x, path=None, verbose=False):
    fn = full_path(fn, path)
    fn = fn.with_suffix('.json')
    with open(fn, "w") as f:
        json.dump(x, f)
    if verbose:
        print(f'{fn} saved')
