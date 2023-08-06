import torch
import sys
from typing import Union

__all__ = ['Allocator']



class Allocator(object):
    def __init__(self, main_device: Union[torch.device, str, int], dataparallel: bool):

        try:
            main_device = torch.device(main_device)
        except Exception as ex:
            raise type(ex)(
                str(
                    ex) + "Main:_device should be cpu 'cpu' \
                           or an integer but  %s found" % main_device).with_traceback(
                sys.exc_info()[2])
        self.main_device = main_device
        self.dataparallel = dataparallel

    @property
    def main_device(self):
        return self._main_device

    @main_device.setter
    def main_device(self, value):
        self._main_device = torch.device(value)

    def _allocate_iterable(self, x, device):
        for i in x:
            if isinstance(i, (list, tuple)):
                yield self._allocate(i, device)
            elif isinstance(i, dict):
                for key, value in i.items():
                    i[key] = self._allocate(value, device)
                yield i
            elif isinstance(i, torch.Tensor):
                yield i.to(device)
            else:
                yield i

    def _allocate(self, x, device):
        if isinstance(x, list):
            return list(self._allocate_iterable(x, device))
        elif isinstance(x, tuple):
            return tuple(self._allocate_iterable(x, device))
        elif isinstance(x, dict):
            for key, value in x.items():
                x[key] = self._allocate(value, device)
            return x
        elif isinstance(x, torch.Tensor):
            return x.to(device)
        else:
            return x

    def allocate(self, x, device=None):
        if device is None:
            device = self.main_device
        else:
            device = torch.device(device)
        if self.dataparallel:
            return x
        else:
            return self._allocate(x, device)

    def __call__(self, item, device=None):
        return self.allocate(item, device)
