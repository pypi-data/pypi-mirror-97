from athena.patch.statsd_config import DEFAULT_STATSD_CLIENT as STATSD_CLIENT

import torch

import torch.nn as nn
import torch.optim as optim

_Module = nn.Module
_Optimizer = optim.optimizer.Optimizer
_tensor = torch.tensor

def fwd_pre_hook(mod, input):
    mod._athena_timer_fwd = STATSD_CLIENT.timer("pytorch.nn.Module.forward")
    mod._athena_timer_fwd.start()

def fwd_hook(mod, input, output):
    if hasattr(mod, '_athena_timer_fwd'):
        mod._athena_timer_fwd.stop()

def back_hook(mod, grad_input, grad_output):
    mod._athena_timer_back = STATSD_CLIENT.timer("pytorch.nn.Module.backward")
    mod._athena_timer_back.start()

    if hasattr(mod, '_athena_timer_back'):
        mod._athena_timer_back.stop()

class PatchedOptimizer(_Optimizer):
    def zero_grad(self):
        with STATSD_CLIENT.timer("pytorch.optim.Optimizer.zero_grad"):
            return super(PatchedOptimizer, self).zero_grad()
    def step(self, closure):
        with STATSD_CLIENT.timer("pytorch.optim.Optimizer.step"):
            return super(PatchedOptimizer, self).step(closure)


def patched_tensor(*args, **kwargs):
    meta = {}

    if len(args) > 0:
        meta = {"data": args[0]}

    with STATSD_CLIENT.timer("pytorch.Tensor.tensor", meta=meta):
        return _tensor(*args, **kwargs)

class PatchedNNModule(_Module):
    def __init__(self):
        super(PatchedNNModule, self).__init__()

        # Runs after very forward pass
        self.register_forward_hook(fwd_hook)

        # Runs before every forward pass
        self.register_forward_pre_hook(fwd_pre_hook)

        #self.register_backward_hook(back_hook)

    def forward(self, x):
        with STATSD_CLIENT.timer("pytorch.nn.Module.forward"):
            return super(PatchedNNModule, self).forward(x)

    def train(self, mode=True):
        with STATSD_CLIENT.timer("pytorch.nn.Module.train"):
            return super(PatchedNNModule, self).train(mode)

def patch():
    nn.Module = PatchedNNModule
    optim.optimizer.Optimizer = PatchedOptimizer
    torch.tensor = patched_tensor
