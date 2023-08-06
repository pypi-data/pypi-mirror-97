import atexit
import queue
import threading
from collections import deque
from concurrent.futures import Future, wait, ThreadPoolExecutor
import logging

from typing import List, Dict, Any, Union

from libc.stdint cimport uint32_t
from cpython.mem cimport PyMem_Malloc, PyMem_Free

import numpy as np
from . cimport c_tpu


LOGGER = logging.getLogger("iva_tpu")

_shutdown = False


def _python_exit():
    global _shutdown
    _shutdown = True


atexit.register(_python_exit)

np_to_tpu_type = {np.dtype('int8'): 0,
                  np.dtype('float32'): 1,
                  np.dtype('float16'): 2,
                  np.dtype('float64'): 3}

tpu_type_to_dtype = {v: k for k, v in np_to_tpu_type.items()}


cdef class TPUPlaceholder:
    cdef const c_tpu.TPUIONode *_ptr


cpdef parse_placeholder_description(placeholder: TPUPlaceholder):
    """Parses metadata description to Python dictionary"""
    cdef const c_tpu.TPUIONode *desc = placeholder._ptr
    result = dict()
    result['address'] = desc.address
    result['scale'] = [scale for scale in desc.scale[:desc.scale_len]]

    user_shape_intermediate = <const int *>desc.user_shape
    result['user_shape'] = [axis for axis in user_shape_intermediate[:desc.user_shape_len]]
    result['user_shape_len'] = desc.user_shape_len
    result['user_order'] = desc.user_order

    padding_intermediate = <const c_tpu.int_pair *>desc.padding
    result['padding'] = [tuple(dic.values()) for dic in padding_intermediate[:desc.user_shape_len]]

    tpu_shape_intermediate = <const int *>desc.tpu_shape
    result['tpu_shape'] = [axis for axis in tpu_shape_intermediate[:desc.tpu_shape_len]]
    result['tpu_order'] = desc.tpu_order
    result['tpu_shape_len'] = desc.tpu_shape_len
    result['dtype'] = desc.dtype
    result['layer_name'] = desc.anchor.decode('utf-8') if desc.anchor else desc.layer_name.decode('utf-8')
    result['size'] = desc.size
    return result


class TPUProgramException(Exception):
    pass


class TPUProgramRuntimeException(TPUProgramException):
    pass


class TPUTensorException(TPUProgramRuntimeException):
    pass


cdef class TPUDeviceException(Exception):
    cdef c_tpu.TPUDeviceError deviceError

    @property
    def error(self):
        return self.error.message


class NOTPUDeviceException(TPUDeviceException):
    pass


cdef class TPUProgram:
    cdef c_tpu.TPUProgram* c_tpu_program

    def __cinit__(self, path: str):
        self.path = path
        self.c_tpu_program = NULL

        cdef b_path = path.encode("utf-8")
        cdef char *c_path = b_path

        cdef c_tpu.TPUProgramZipLoader *c_loader = c_tpu.tpu_program_zip_loader_open(c_path)
        if not c_loader:
            raise TPUProgramException("Failed to open program file %s" % path)

        self.c_tpu_program = c_tpu.tpu_program_open(c_loader)
        c_tpu.tpu_program_zip_loader_close(c_loader)

        if not self.c_tpu_program:
            raise TPUProgramException("Failed to open TPU program")

        self.device = None

    def __dealloc__(self):
        if self.c_tpu_program:
            c_tpu.tpu_program_close(self.c_tpu_program)
            self.c_tpu_program = NULL

    @property
    def inputs_count(self):
        return <int>c_tpu.tpu_program_get_inputs_count(self.c_tpu_program)

    @property
    def outputs_count(self):
        return <int>c_tpu.tpu_program_get_outputs_count(self.c_tpu_program)

    @property
    def inputs(self):
        """Returns verbose description of input parameters"""
        return [self.get_input_description(i) for i in range(self.inputs_count)]

    @property
    def outputs(self):
        """Returns verbose description of output parameters"""
        return [self.get_output_description(i) for i in range(self.outputs_count)]

    def get_input_name(self, index):
        py_byte_str = c_tpu.tpu_program_get_input_name_by_index(self.c_tpu_program, index)
        return py_byte_str.decode('utf-8')

    def get_input_index(self, name: str):
        py_bytes = name.encode('utf-8')
        index = c_tpu.tpu_program_get_input_index_by_name(self.c_tpu_program, <char *>py_bytes)
        if index < 0:
            raise TPUProgramException(f"input layer name {name} not found")
        return index

    def get_input_size(self, index):
        return <int>c_tpu.tpu_program_get_input_buffer_size(self.c_tpu_program, index)

    def get_input_type(self, index):
        cdef const c_tpu.TPUIONode *node = c_tpu.tpu_program_get_input_node(self.c_tpu_program, index)
        if not node:
            raise IndexError("input node {} not found".format(index))
        return tpu_type_to_dtype[node.dtype]

    def get_output_name(self, index: int):
        py_byte_str = c_tpu.tpu_program_get_output_name_by_index(self.c_tpu_program, index)
        return py_byte_str.decode('utf-8')

    def get_output_index(self, name: str):
        py_bytes = name.encode('utf-8')
        index = c_tpu.tpu_program_get_output_index_by_name(self.c_tpu_program, <char *>py_bytes)
        if index < 0:
            raise TPUProgramException(f"output layer name {name} not found")
        return index

    def get_output_size(self, index):
        return <int>c_tpu.tpu_program_get_output_buffer_size(self.c_tpu_program, index)

    def get_output_type(self, index):
        cdef const c_tpu.TPUIONode *node = c_tpu.tpu_program_get_output_node(self.c_tpu_program, index)
        if not node:
            raise IndexError("output node {} not found".format(index))
        return tpu_type_to_dtype[node.dtype]

    def get_input_description(self, index):
        """Returns verbose description of network input"""
        cdef TPUPlaceholder wrapper = TPUPlaceholder.__new__(TPUPlaceholder)
        wrapper._ptr = c_tpu.tpu_program_get_input_node(self.c_tpu_program, index)
        return parse_placeholder_description(wrapper)

    def get_output_description(self, index):
        """Returns verbose description of network output"""
        cdef TPUPlaceholder wrapper = TPUPlaceholder.__new__(TPUPlaceholder)
        wrapper._ptr = c_tpu.tpu_program_get_output_node(self.c_tpu_program, index)
        return parse_placeholder_description(wrapper)

    cdef c_tpu.TPUTensor new_output_tensor(self, dtype, int i):
        cdef c_tpu.TPUTensor tensor = c_tpu.tpu_program_make_output_user_tensor(self.c_tpu_program, i)
        tensor.dtype = np_to_tpu_type[np.dtype(dtype)]
        tensor.size = c_tpu.tpu_tensor_get_size(&tensor)
        tensor.data = <char *>PyMem_Malloc(tensor.size)
        if not tensor.data:
            raise MemoryError
        return tensor

    cdef c_tpu.TPUTensor make_input_tensor(self, i):
        return c_tpu.tpu_program_make_input_user_tensor(self.c_tpu_program, i)

    cdef free_tensor(self, c_tpu.TPUTensor *tensor):
        PyMem_Free(tensor.data)

    def set_loaded_device(self, device: TPUDevice):
        assert self.device is None, "Program already loaded"
        self.device = device

    cdef const c_tpu.TPUProgramLUTActivationParameters *program_lut_params(self):
        cdef const c_tpu.TPUProgramHardwareParameters* hw_params = c_tpu.tpu_program_get_hardware_parameters(self.c_tpu_program)
        return c_tpu.tpu_program_hardware_parameters_get_lut_parameters(hw_params)

    @property
    def lut_input_bit_width(self):
        return c_tpu.tpu_program_hardware_parameters_get_lut_input_bit_width(self.program_lut_params())

    @property
    def lut_data_bit_width(self):
        return c_tpu.tpu_program_hardware_parameters_get_lut_data_bit_width(self.program_lut_params())

    @property
    def lut_address_bit_width(self):
        return c_tpu.tpu_program_hardware_parameters_get_lut_address_bit_width(self.program_lut_params())

    @property
    def lut_output_bit_width(self):
        return c_tpu.tpu_program_hardware_parameters_get_lut_output_bit_width(self.program_lut_params())

    @property
    def driver_version(self):
        py_byte_str = c_tpu.tpu_program_get_driver_version(self.c_tpu_program)
        if py_byte_str:
            return py_byte_str.decode('utf-8')

    @property
    def ip_version(self):
        py_byte_str = c_tpu.tpu_program_get_ip_version(self.c_tpu_program)
        if py_byte_str:
            return py_byte_str.decode('utf-8')

    @property
    def is_loaded(self):
        return self.device is not None


MAX_TENSORS = 32
MAX_IO_DESCRIPTORS = 64


class TPUWorkItem:
    def __init__(self, io_descriptor: TPUIODescriptor, as_dict: bool):
        self.inference = io_descriptor
        self.as_dict = as_dict

    def get_io_descriptor(self) -> TPUIODescriptor:
        return self.inference

    def process_result(self) -> Union[List[bytes], Dict[str, bytes]]:
        return self.inference.get_raw_results(self.as_dict)



class TPUWorkItemTensors(TPUWorkItem):
    def __init__(self, io_descriptor: TPUIODescriptor, as_dict: bool, result_dtypes=None):
        super().__init__(io_descriptor, as_dict)
        self.dtypes = result_dtypes

    def process_result(self) -> Union[List[np.ndarray], Dict[str, np.ndarray]]:
        return self.inference.get_results(self.dtypes, self.as_dict)


cdef tpu_tensor_to_ndarray(c_tpu.TPUTensor *tensor):
    shape = []
    for j in range(tensor.shape_len):
        shape.append(tensor.shape[j])
    c_buffer = <char *> tensor.data
    buffer = c_buffer[:tensor.size]
    arr = np.frombuffer(buffer, dtype=tpu_type_to_dtype[tensor.dtype]).reshape(shape)
    return arr


cdef class TPUIODescriptor:
    cdef c_tpu.TPUProgram* c_tpu_program
    cdef c_tpu.TPUInference* inference
    cdef TPUProgram program

    def __init__(self, program: TPUProgram):
        self.program = program
        self.c_tpu_program = program.c_tpu_program
        self.inference = NULL

    def allocate(self):
        self.inference = c_tpu.tpu_inference_create(self.c_tpu_program)
        if not self.inference:
            raise RuntimeError("IO Descriptor Allocation Failure")

    def deallocate(self):
        c_tpu.tpu_inference_free(self.inference)
        self.inference = NULL

    def get_input_from_dict(self, features: Dict[str, np.ndarray or bytes]):
        for name, tensor in features.items():
            index = self.program.get_input_index(name)
            yield index, tensor

    def get_input_from_list(self, features: List[np.ndarray or bytes]):
        for index, tensor in enumerate(features):
            yield index, tensor

    def get_features_iterator(self, features):
        features_count = len(features)
        assert features_count == self.program.inputs_count
        getter = None
        if type(features) == dict:
            getter = self.get_input_from_dict(features)
        elif type(features) == list:
            getter = self.get_input_from_list(features)
        if getter is None:
            raise TPUProgramException("Expected dict or list as features")
        return getter

    @staticmethod
    cdef check_tensor_shape(tpu_tensor: c_tpu.TPUTensor, tensor: np.ndarray):
        user_shape_intermediate = <const int *> tpu_tensor.shape
        shape = [dim for dim in user_shape_intermediate[:tpu_tensor.shape_len]]

        if len(tensor.shape) == 3:  # 1, H, W, C
            tensor = np.expand_dims(tensor, axis=0)

        if shape != list(tensor.shape):
            raise TPUTensorException("Tensor shape mismatch: source shape {}, destination shape {}".format(shape, tensor.shape))

    def set_input_tensor(self, tensor: np.ndarray, index: int):
        """
        Set input tensor by index
        """
        allowed_types = (np.int8, np.float16, np.float32, np.float64)
        if tensor.dtype not in allowed_types:
            raise TPUProgramException("unexpected tensor type %s. Expected %s" % (tensor.dtype, allowed_types))

        cdef c_tpu.TPUTensor tpu_tensor = self.program.make_input_tensor(index)

        # check shape
        TPUIODescriptor.check_tensor_shape(tpu_tensor, tensor)

        input_bytes = tensor.tobytes()
        tpu_tensor.data = <char *>input_bytes
        tpu_tensor.size = len(input_bytes)
        tpu_tensor.dtype = np_to_tpu_type[tensor.dtype]

        rc = c_tpu.tpu_program_set_input_tensor(self.c_tpu_program, self.inference, &tpu_tensor, index)
        if rc != 0:
            raise TPUProgramException(f"can't set input tensor {index}")

    def set_features(self, features: List[np.ndarray] or Dict[str, np.ndarray]):
        feature_getter = self.get_features_iterator(features)

        for index, tensor in feature_getter:
            self.set_input_tensor(tensor, index)

    cdef set_input_buffer(self, buffer: bytes, index: int):
        """
        Set input buffer by index
        """
        cdef char* c_buffer = <char *>buffer
        if c_tpu.tpu_program_get_input_buffer_size(self.c_tpu_program, index) != len(buffer):
            raise IndexError
        c_tpu.tpu_program_set_input_buffer(self.inference, index, c_buffer, len(buffer))

    def set_buffers(self, features: List[bytes] or Dict[str, bytes]):
        feature_getter = self.get_features_iterator(features)

        for index, buffer in feature_getter:
            self.set_input_buffer(buffer, index)

    def get_output_buffer(self, index: int) -> bytes:
        """
        Get output buffer by index
        """
        cdef char *buffer = <char *>c_tpu.tpu_inference_get_output_buffer(self.inference, index)
        cdef bytes b = buffer[:self.program.get_output_size(index)]
        return b

    def get_raw_results(self, as_dict=False):
        outputs_count = self.program.outputs_count
        result = [self.get_output_buffer(i) for i in range(outputs_count)]
        if as_dict:
            node_names = [self.program.get_output_name(i) for i in range(outputs_count)]
            result = dict(zip(node_names, result))
        return result

    def get_output_tensor(self, index: int, dtype: np.dtype):
        cdef c_tpu.TPUTensor tensor = self.program.new_output_tensor(dtype, index)
        rc = c_tpu.tpu_program_get_output_tensor(self.c_tpu_program, self.inference, &tensor, index)
        if rc != 0:
            raise TPUProgramException(f"can't get output tensor {index}")
        try:
            np_tensor = tpu_tensor_to_ndarray(&tensor)
            return np_tensor
        finally:
            self.program.free_tensor(&tensor)

    def get_results(self, result_dtypes=None, as_dict=False):
        outputs_count = self.program.outputs_count

        result = [self.get_output_tensor(i, self.get_result_dtype(result_dtypes, i)) for i in range(outputs_count)]
        if as_dict:
            node_names = [self.program.get_output_name(i) for i in range(outputs_count)]
            result = dict(zip(node_names, result))
        return result

    def get_result_dtype(self, result_dtypes, i):
        if result_dtypes is None:
            return self.program.get_output_type(i)
        elif type(result_dtypes) == list:
            return result_dtypes[i]
        elif type(result_dtypes) == dict:
            node_name = self.program.get_output_name(i)
            return result_dtypes[node_name]
        elif type(result_dtypes) == np.dtype:
            return result_dtypes
        elif issubclass(result_dtypes, np.number):
            return np.dtype(result_dtypes)
        else:
            raise RuntimeError("unexpected result dtype: " + str(result_dtypes))

    def __del__(self):
        if self.inference:
            self.deallocate()


cdef class TPUDevice:
    cdef c_tpu.TPUDevice* c_tpu_device
    cdef c_tpu.TPUProgram* c_tpu_program

    def __cinit__(self):
        cdef TPUDeviceException e = NOTPUDeviceException()
        self.c_tpu_device = c_tpu.tpu_device_build(&e.deviceError)

        if not self.c_tpu_device:
            raise e

        self.c_tpu_program = NULL
        self.program = None
        self.inference_queue = None

    def __init__(self, queue_len=16):
        assert queue_len <= 64
        self.program = None
        self.inference_queue = None

    def __dealloc__(self):
        if self.c_tpu_device:
            c_tpu.tpu_device_close(self.c_tpu_device)

    def load(self, program: TPUProgram):
        if c_tpu.tpu_program_check_hardware_parameters(self.c_tpu_device, program.c_tpu_program, NULL) != 0:
            raise TPUProgramException("Program compiled for different device")

        cdef c_tpu.TPUProgramError error
        rc = c_tpu.tpu_program_load(self.c_tpu_device, program.c_tpu_program, &error)
        if rc != 0:
            raise TPUProgramException("Failed to load program {}".format(error.message))

        self.program = program
        self.program.set_loaded_device(self)
        self.inference_queue = TPUInferenceQueue(self)

    def run(self, features: List[np.ndarray] or Dict[str, np.ndarray], dtype=None):
        with self.inference_queue as inference:
            future = inference.submit_tensors(features, result_dtypes=dtype)
            wait([future])
            return future.result()

    def run_raw(self, features: Dict[str, bytes] or List[bytes]):
        with self.inference_queue as inference:
            future = inference.submit_buffers(features)
            wait([future])
            return future.result()

    cdef submit_inference(self, io_descriptor: TPUIODescriptor):
        cdef c_tpu.TPUInferenceError error
        rc = c_tpu.tpu_inference_submit(self.c_tpu_device, io_descriptor.inference, &error)
        if rc != 0:
            raise TPUProgramException("Failed to submit inference")

    def wait_inference(self):
        cdef uint32_t counter
        error = TPUDeviceException()

        with nogil:
            rc = c_tpu.tpu_inference_wait(self.c_tpu_device, &counter, &error.deviceError)

        if rc != 0:
            raise error

        return counter

    @property
    def hardware_id(self):
        return <int>c_tpu.tpu_get_hardware_id(self.c_tpu_device)

    @property
    def total_mem(self):
        cdef c_tpu.TPUDeviceError error
        rc = c_tpu.tpu_get_total_mem(self.c_tpu_device, &error)
        if rc < 0:
            raise TPUProgramException("Failed to get total mem {}".format(error.message))
        return <unsigned long int>rc

    @property
    def success_cnt(self):
        cdef c_tpu.TPUDeviceError error
        rc = c_tpu.tpu_get_success_cnt(self.c_tpu_device, &error)
        if rc < 0:
            raise TPUProgramException("Failed to get success counter {}".format(error.message))
        return <int>rc

    @property
    def error_cnt(self):
        cdef c_tpu.TPUDeviceError error
        rc = c_tpu.tpu_get_error_cnt(self.c_tpu_device, &error)
        if rc < 0:
            raise TPUProgramException("Failed to get error counter {}".format(error.message))
        return <int>rc

    @property
    def control_unit_version(self):
        return <int>c_tpu.tpu_get_control_unit_version(self.c_tpu_device)

    @property
    def ewp_banks_count(self):
        return <int>c_tpu.tpu_get_ewp_banks_count(self.c_tpu_device)

    @property
    def ewp_bank_size(self):
        return <int>c_tpu.tpu_get_ewp_bank_size(self.c_tpu_device)

    @property
    def ewp_channels_count(self):
        return <int>c_tpu.tpu_get_ewp_channels_count(self.c_tpu_device)

    @property
    def psp_buffer_size(self):
        return <int>c_tpu.tpu_get_psp_buffer_size(self.c_tpu_device)

    @property
    def sdp_buffer_size(self):
        return <int>c_tpu.tpu_get_sdp_buffer_size(self.c_tpu_device)

    @property
    def bias_buffer_size(self):
        return <int>c_tpu.tpu_get_bias_buffer_size(self.c_tpu_device)

    @property
    def dws_channel_bit_width(self):
        return <int>c_tpu.tpu_get_dws_data_block_bit_width(self.c_tpu_device)

    @property
    def dws_data_block_bit_width(self):
        return <int>c_tpu.tpu_get_dws_data_block_bit_width(self.c_tpu_device)

    @property
    def dws_channels_count(self):
        return <int>c_tpu.tpu_get_dws_channels_count(self.c_tpu_device)

    @property
    def dws_optimal_window_size(self):
        return <int>c_tpu.tpu_get_dws_optimal_window_size(self.c_tpu_device)

    @property
    def dws_max_window_size(self):
        return <int>c_tpu.tpu_get_dws_max_window_size(self.c_tpu_device)

    @property
    def ddr_banks_count(self):
        return <int>c_tpu.tpu_get_ddr_banks_count(self.c_tpu_device)

    @property
    def ddr_bank_size(self):
        return <int>c_tpu.tpu_get_ddr_bank_size(self.c_tpu_device)

    @property
    def axi_address_width(self):
        return <int>c_tpu.tpu_get_axi_address_width(self.c_tpu_device)

    @property
    def axi_word_length(self):
        return <int>c_tpu.tpu_get_axi_word_length(self.c_tpu_device)

    @property
    def dma_channels_count(self):
        return <int>c_tpu.tpu_get_dma_channels_count(self.c_tpu_device)

    @property
    def cache_word_length(self):
        return <int>c_tpu.tpu_get_cache_word_length(self.c_tpu_device)

    @property
    def cache_bank_size(self):
        return <int>c_tpu.tpu_get_cache_bank_size(self.c_tpu_device)

    @property
    def cache_banks_count(self):
        return <int>c_tpu.tpu_get_cache_banks_count(self.c_tpu_device)

    @property
    def systolic_array_size(self):
        cdef c_tpu.int_pair p = c_tpu.tpu_get_systolic_array_size(self.c_tpu_device)
        return <int>p.first, <int>p.second

    @property
    def matrix_engine_data_bit_width(self):
        return <int> c_tpu.tpu_get_me_data_bit_width(self.c_tpu_device)

    @property
    def frequency(self):
        return <int> c_tpu.tpu_get_frequency(self.c_tpu_device)

    @property
    def driver_version(self):
        py_byte_str = c_tpu.tpu_get_driver_version(self.c_tpu_device)
        if py_byte_str:
            return py_byte_str.decode('utf-8')

    @property
    def ip_version(self):
        py_byte_str = c_tpu.tpu_get_ip_version(self.c_tpu_device)
        if py_byte_str:
            return py_byte_str.decode('utf-8')


def _worker(work_item: TPUWorkItem, inference_queue: queue.Queue):
    counter = inference_queue.wait()  # got inference results
    result = inference_queue.inference_processed(work_item)
    del work_item
    return result


cdef class TPUInferenceQueue:
    cdef dict __dict__
    cdef uint32_t inference_count
    cdef TPUProgram program
    cdef TPUDevice device

    def __init__(self, device: TPUDevice, queue_len: int = 8):
        self.device = device
        self.program = device.program
        self._queue_len = queue_len
        self._executor = None
        self.queued_inferences = 0
        self._processed_inferences = 0
        self.inference_count = 0
        self.io_descriptors = deque(maxlen=self._queue_len  + 1)
        self.queued_inferences = 0
        self.io_descriptors_count = self._queue_len + 1
        for i in range(self.io_descriptors_count):
            io_descriptor = TPUIODescriptor(self.program)
            io_descriptor.allocate()
            self.io_descriptors.append(io_descriptor)

    def __enter__(self):
        self._start_worker()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._stop_worker()


    def __del__(self):
        for i in range(self.io_descriptors_count):
            self.io_descriptors[i].deallocate()
        self.io_descriptors.clear()

    def wait(self):
        return self.device.wait_inference()

    def get_next_io_descriptor(self) -> TPUIODescriptor:
        """
        Get next usable IO descriptor from queue
        """
        if self.queued_inferences - self._processed_inferences < self._queue_len:
            io_descriptor = self.io_descriptors[
            self.queued_inferences % self.io_descriptors_count]
            self.queued_inferences += 1
            return io_descriptor
        return None

    def submit_buffers(self, features: List[bytes] or Dict[str, bytes]) -> Future:
        io_descriptor = self.get_next_io_descriptor()
        assert io_descriptor is not None
        io_descriptor.set_buffers(features)

        as_dict = type(features) == dict
        work_item = TPUWorkItem(io_descriptor, as_dict=as_dict)
        return self.submit(work_item)

    def submit_tensors(self, features: List[np.ndarray] or Dict[str, np.ndarray],
               result_dtypes=np.int8) -> Future:
        io_descriptor = self.get_next_io_descriptor()
        assert io_descriptor is not None

        as_dict = type(features) == dict
        io_descriptor.set_features(features)
        work_item = TPUWorkItemTensors(io_descriptor, as_dict=as_dict, result_dtypes=result_dtypes)
        return self.submit(work_item)

    def submit(self, work_item: TPUWorkItem) -> Future:
        f = self._executor.submit(_worker, work_item, self)
        self.device.submit_inference(work_item.get_io_descriptor())
        return f

    def inference_processed(self, work_item: TPUWorkItem):
        self._processed_inferences += 1
        return work_item.process_result()

    @property
    def processed_inferences(self):
        return self._processed_inferences

    def _start_worker(self):
        if self._executor is None:
            self._executor = ThreadPoolExecutor(max_workers=1)

    def _stop_worker(self):
        self._executor.shutdown()
        self._executor = None
