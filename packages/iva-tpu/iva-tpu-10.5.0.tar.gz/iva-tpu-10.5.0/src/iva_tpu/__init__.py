# -*- coding: utf-8 -*-
"""IVA TPU Platform classes."""

from .tpu_device import TPUDevice, TPUInferenceQueue, TPUDeviceException
from .tpu_program import TPUProgram, TPUProgramException, TPUProgramRuntimeException, TPUTensorException


def open_device() -> TPUDevice:
    """Build platform tpu device."""
    return TPUDevice()


__all__ = ['TPUDevice', 'TPUProgram', 'open_device', 'TPUInferenceQueue',
           'TPUDeviceException', 'TPUProgramException', 'TPUProgramRuntimeException', 'TPUTensorException']
