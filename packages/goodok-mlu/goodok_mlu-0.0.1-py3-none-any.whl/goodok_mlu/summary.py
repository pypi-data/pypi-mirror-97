import numpy as np
import pandas as pd
import humanize
from collections import OrderedDict
from IPython.display import display
import torch
import torch.nn as nn


def print_trainable_parameters2(model, max_rows=400, max_colwidth=100, with_class=False):

    d = get_trainable_parameters(model, with_class=with_class)
    print('Total:', humanize.intcomma(d['total_number']))
    with pd.option_context("display.max_rows", max_rows, 'max_colwidth', max_colwidth):
        display(d['df_params'])


def get_trainable_parameters(model, with_class=False):
    params = []
    total_number = 0
    if with_class:
        gen = named_parameters2(model)
    else:
        gen = model.named_parameters()
    for name, p, module in gen:
        if with_class:
            name, class_name = name

        if p.requires_grad:
            shape = " x ".join([str(i) for i in list(p.shape)])
            number = p.numel()
            d = {'name': name, 'shape': shape, 'number': number}
            if with_class:
                d['class'] = class_name
            params.append(d)
            total_number += number
    df_params = pd.DataFrame(params)
    return {'df_params': df_params, 'total_number': total_number}


def named_parameters2(self, prefix='', recurse=True):
    r"""Returns an iterator over module parameters, yielding both the
    name of the parameter as well as the parameter itself.

    Args:
        prefix (str): prefix to prepend to all parameter names.
        recurse (bool): if True, then yields parameters of this module
            and all submodules. Otherwise, yields only parameters that
            are direct members of this module.

    Yields:
        (string, Parameter): Tuple containing the name and parameter

    Example::

        >>> for name, param in self.named_parameters():
        >>>    if name in ['bias']:
        >>>        print(param.size())

    """
    gen = _named_members2(
        self,
        lambda module: module._parameters.items(),
        prefix=prefix, recurse=recurse)
    for elem in gen:
        yield elem


def _named_members2(self, get_members_fn, prefix='', recurse=True):
    r"""Helper method for yielding various names + members of modules."""
    memo = set()
    modules = self.named_modules(prefix=prefix) if recurse else [(prefix, self)]
    for module_prefix, module in modules:
        members = get_members_fn(module)
        for k, v in members:
            if v is None or v in memo:
                continue
            memo.add(v)
            name = module_prefix + ('.' if module_prefix else '') + k
            class_name = fullname(module)
            class_name = module.__class__.__name__
            yield (name, class_name), v, module


def fullname(o):
    # o.__module__ + "." + o.__class__.__qualname__ is an example in
    # this context of H.L. Mencken's "neat, plausible, and wrong."
    # Python makes no guarantees as to whether the __module__ special
    # attribute is defined, so we take a more circumspect approach.
    # Alas, the module name is explicitly excluded from __qualname__
    # in Python 3.

    module = o.__class__.__module__
    if module is None or module == str.__class__.__module__:
        return o.__class__.__name__  # Avoid reporting __builtin__
    else:
        return module + '.' + o.__class__.__name__


def attach_names_to_modules(model):
    for a in named_parameters2(model):
        pname = a[0][0]
        # class_name = a[0][1]
        # param  = a[1]
        module = a[2]

        module_name = '.'.join(pname.split('.')[:-1])
        module.__name = module_name


def get_object_size(o):
    res = [None]
    if hasattr(o, 'get_spatial_locations'):
        res = [list(o.features.size()),
               list(o.get_spatial_locations().size()),
               list(o.spatial_size.numpy())]
    elif hasattr(o, 'size'):
        res = list(o.size())
    return res


def summary(model, xb=None, input_size=None, batch_size=-1, device="cuda", verbose=0, return_string=False, return_data=False):
    # https://github.com/sksq96/pytorch-summary/blob/master/torchsummary/torchsummary.py
    if xb is None:
        assert input_size is not None
    if input_size is None:
        assert xb is not None

    attach_names_to_modules(model)

    def register_hook(module):

        def hook(module, input, output):
            class_name = str(module.__class__).split(".")[-1].split("'")[0]
            full_class_name = fullname(module)
            module_idx = len(summary)

            if verbose:
                print(type(module))
                print('module:', full_class_name)
                print('output:', fullname(output))

            m_key = "%s-%i" % (class_name, module_idx + 1)
            summary[m_key] = OrderedDict()

            summary[m_key]['class_name'] = class_name
            summary[m_key]['idx'] = module_idx + 1
            summary[m_key]['name'] = getattr(module, '__name', '')

            if full_class_name == 'sparseconvnet.ioLayers.InputLayer':
                # coords and features
                cf = input[0]
                summary[m_key]["input_shape"] = list(cf[0].size()), list(cf[1].size())
            elif isinstance(input[0], dict):
                cf = input[0]
                summary[m_key]["input_shape"] = [list(v.size()) for key, v in cf.items() if isinstance(v, torch.Tensor)]
            # elif full_class_name.startswith('sparseconvnet.') or  full_class_name.startswith('SCN_architectures'):
            elif hasattr(input[0], 'get_spatial_locations'):
                summary[m_key]["input_shape"] = (list(input[0].features.size()),
                                                 list(input[0].get_spatial_locations().size()),
                                                 list(input[0].spatial_size.numpy()))
            elif isinstance(input[0], (list, tuple)):
                summary[m_key]["input_shape"] = [get_object_size(o) for o in input[0]]
            else:
                if verbose > 1:
                    print(full_class_name, input[0])
                summary[m_key]["input_shape"] = list(input[0].size())
                # summary[m_key]["input_shape"][0] = batch_size

            if isinstance(output, (list, tuple)):
                summary[m_key]["output_shape"] = [
                    [-1] + get_object_size(o)[1:] for o in output
                ]
            else:
                # if fullname(output) in ['sparseconvnet.sparseConvNetTensor.SparseConvNetTensor', 'sparseconvnet.ioLayers.InputLayer']:
                if hasattr(output, 'get_spatial_locations'):
                    summary[m_key]["output_shape"] = (list(output.get_spatial_locations().size()),
                                                      list(output.features.size()),
                                                      list(output.spatial_size.numpy()))
                else:
                    summary[m_key]["output_shape"] = list(output.size())
                    # summary[m_key]["output_shape"][0] = batch_size

            params = 0
            if hasattr(module, "weight") and hasattr(module.weight, "size"):
                weight_size = list(module.weight.size())
                summary[m_key]["weight_size"] = weight_size
                params += torch.prod(torch.LongTensor(weight_size))
                summary[m_key]["trainable"] = module.weight.requires_grad
            if hasattr(module, "bias") and hasattr(module.bias, "size"):
                bias_size = list(module.bias.size())
                summary[m_key]["bias_size"] = bias_size
                params += torch.prod(torch.LongTensor(bias_size))
            summary[m_key]["nb_params"] = params
        # print("module", module)
        # print(isinstance(module, nn.Sequential))
        # print(module == model)
        if not isinstance(module, nn.Sequential) \
                and not isinstance(module, nn.ModuleList):
            # and not (module == model)
            hooks.append(module.register_forward_hook(hook))

    device = device.lower()
    assert device in [
        "cuda",
        "cpu",
    ], "Input device is not valid, please specify 'cuda' or 'cpu'"

    if device == "cuda" and torch.cuda.is_available():
        dtype = torch.cuda.FloatTensor
    else:
        dtype = torch.FloatTensor

    # multiple inputs to the network
    if isinstance(input_size, tuple):
        input_size = [input_size]

    # batch_size of 2 for batchnorm
    if xb is None:
        x = [torch.rand(2, *in_size).type(dtype) for in_size in input_size]
    # print(type(x[0]))

    # create properties
    summary = OrderedDict()
    hooks = []

    # register hook
    model.apply(register_hook)

    try:
        # make a forward pass
        # print(x.shape)
        if xb is None:
            model(*x)
        elif isinstance(xb, dict):
            model(xb)
        else:
            model(*xb)

    finally:
        # remove these hooks
        for h in hooks:
            h.remove()

    lines = []

    def add_line(line):
        lines.append(line)

    add_line("-" * 90)
    line_new = "{:>30}  {:>35} {:>15}".format("Layer (type)", "Output Shape", "Param #")
    add_line(line_new)
    line_new = "{:>30}  {:>35} {:>15}".format("", "coords   features  spatial_size", "")
    add_line(line_new)
    add_line("=" * 90)
    total_params = 0
    total_output = 0
    trainable_params = 0
    # print(summary.keys())
    for layer in summary:
        # input_shape, output_shape, trainable, nb_params
        line_new = "{:>30}  {:<30} {:>35} {:>15}".format(
            layer,
            str(summary[layer]["name"]),
            str(summary[layer]["output_shape"]),
            "{0:,}".format(summary[layer]["nb_params"]),
        )
        total_params += summary[layer]["nb_params"]
        try:
            # TODO:
            total_output += np.prod(summary[layer]["output_shape"])
        except:
            pass
        if "trainable" in summary[layer]:
            if summary[layer]["trainable"] is True:
                trainable_params += summary[layer]["nb_params"]
        add_line(line_new)

    # assume 4 bytes/number (float on cuda).
    # total_input_size = abs(np.prod(input_size) * batch_size * 4. / (1024 ** 2.))
    # total_output_size = abs(2. * total_output * 4. / (1024 ** 2.))  # x2 for gradients
    # total_params_size = abs(total_params.numpy() * 4. / (1024 ** 2.))
    # total_size = total_params_size + total_output_size + total_input_size

    add_line("=" * 90)
    add_line("Total params: {0:,}".format(total_params))
    add_line("Trainable params: {0:,}".format(trainable_params))
    add_line("Non-trainable params: {0:,}".format(total_params - trainable_params))
    add_line("-" * 90)
    # print("Input size (MB): %0.2f" % total_input_size)
    # print("Forward/backward pass size (MB): %0.2f" % total_output_size)
    # print("Params size (MB): %0.2f" % total_params_size)
    # print("Estimated Total Size (MB): %0.2f" % total_size)
    # print("----------------------------------------------------------------")
    # return summary
    s = '\n'.join(lines)
    if return_string:
        return s
    if return_data:
        return list(summary.values())
    else:
        print(s)
