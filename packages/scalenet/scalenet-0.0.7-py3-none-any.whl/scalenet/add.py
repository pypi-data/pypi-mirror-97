import torch

class Add(torch.nn.Module):
    def __init__(self):
        super().__init__()

    def forward(self, x, y, *kargs, **kwargs):
        if x is None:
            return y
        elif y is None:
            return x
        else:
            return x + y
