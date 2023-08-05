# -*- coding: utf-8 -*-
"""TPU Device Interface."""
from .tpu import cTPUDevice, cTPUInferenceQueue, TPUDeviceException


# pylint: disable=too-few-public-methods
class TPUDevice(cTPUDevice):
    """Python wrapper for cython device implementation."""

    def __new__(cls, *args, **kw):
        """Pass control to Cython implementation."""
        return super().__new__(cls, *args, **kw)


# pylint: disable=too-few-public-methods
class TPUInferenceQueue(cTPUInferenceQueue):
    """Python wrapper for cython device implementation."""

    def __new__(cls, *args, **kw):
        """Pass control to Cython implementation."""
        return super().__new__(cls, *args, **kw)


__all__ = ['TPUDevice', 'TPUInferenceQueue', 'TPUDeviceException']
