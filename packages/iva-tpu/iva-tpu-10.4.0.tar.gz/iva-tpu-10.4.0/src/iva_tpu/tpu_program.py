# -*- coding: utf-8 -*-
"""TPU Program Interface."""
import os

from .tpu import cTPUProgram, TPUProgramException, TPUProgramRuntimeException, TPUTensorException


# pylint: disable=too-few-public-methods
class TPUProgram(cTPUProgram):
    """Program implements container for TPU binary and DeviceBuffers for weights, SDP, features and output."""

    def __new__(cls, path: str, *args, **kw):
        """Check program path and pass control to Cython implementation."""
        if not os.path.isfile(path):
            raise FileNotFoundError("Program not found: {}".format(path))

        return super().__new__(cls, path, *args, **kw)

    def __init__(self, path: str):
        """Save program path before creating program instance."""
        self.path = path
        super().__init__()


__all__ = ['TPUProgram', 'TPUProgramException', 'TPUProgramRuntimeException', 'TPUTensorException']
