from posix.types cimport off_t
from libc.stdint cimport uint8_t, uint16_t, uint32_t, uint64_t

cdef extern from "tpu.h" nogil:

    cdef struct TPUTensor:
        int dtype
        int shape[8]
        size_t shape_len
        void *data
        size_t size


    cdef struct TPUProgramHardwareParameters:
        pass


    cdef struct TPUProgramLUTActivationParameters:
        pass


    cdef struct tpu_inference_entry:
        pass


    cdef struct TPUInference:
        pass


    cdef struct pipe_dump:
        pass


    cdef enum TPUDeviceErrorSource:
        TPU_DEVICE_SYSTEM_ERROR = 0
        TPU_DEVICE_SYSTEM_COMPAT_ERROR = 1
        TPU_DEVICE_SET_MODE_ERROR = 2
        TPU_DEVICE_QUEUE_ERROR = 3


    cdef struct TPUDeviceError:
        TPUDeviceErrorSource source
        int code
        int pipe_count
        pipe_dump pipes[64]
        char message[1024]


    cdef struct TPUDevice:
        pass

    cdef struct TPUProgramZipLoader:
        pass


    cdef enum TPUProgramErrorReason:
        TPU_PROGRAM_LOAD_ERROR = 0


    cdef struct TPUProgramError:
        TPUProgramErrorReason source
        int code
        char message[1024]


    cdef struct TPUProgram:
        pass


    cdef struct TPUProgramError:
        pass


    cdef struct TPUInferenceError:
        pass


    cdef struct int_pair:
        int first
        int second


    cdef struct TPUIONode:
        unsigned long address
        double *scale
        size_t scale_len

        int user_shape[8]
        char user_order[8]

        size_t user_shape_len
        int_pair padding[8]

        int tpu_shape[8]
        char tpu_order[8]
        size_t tpu_shape_len
        int dtype

        const char *anchor
        const char *layer_name
        unsigned long size

    # Loader definitions
    TPUProgramZipLoader *tpu_program_zip_loader_open(const char *path)
    void tpu_program_zip_loader_close(TPUProgramZipLoader *loader)
    off_t tpu_program_zip_loader_get_object_size(const TPUProgramZipLoader *loader, const char *path)
    int tpu_program_zip_loader_get_object(const TPUProgramZipLoader *loader, const char *path, void *data, size_t size)

    # Device definitions
    TPUDevice *tpu_device_open(const char *path, TPUDeviceError *error)
    TPUDevice *tpu_device_build(TPUDeviceError *error)

    void tpu_device_close(TPUDevice *device)
    int tpu_inference_submit(TPUDevice *device, TPUInference *inference, TPUInferenceError *error)
    int tpu_inference_wait(TPUDevice* device, uint32_t *counter, TPUDeviceError *error)

    # Program definitions
    TPUProgram *tpu_program_open(const TPUProgramZipLoader* loader)
    void tpu_program_close(TPUProgram *program)
    int tpu_program_load(TPUDevice *device, TPUProgram *program, TPUProgramError *error)
    int tpu_program_check_hardware_parameters(const TPUDevice* device, const TPUProgram *program, TPUProgramError *error)

    TPUInference *tpu_inference_create(TPUProgram *program)
    void tpu_inference_free(TPUInference *io_descriptor)

    int tpu_program_set_input_buffer(TPUInference* inference, size_t index, void* buffer, size_t size)
    int tpu_program_set_input_tensor(TPUProgram *program, TPUInference *inference, const TPUTensor *input,
                                     size_t index)
    int tpu_program_get_input_buffer_size(const TPUProgram *program, size_t index)
    void* tpu_inference_get_output_buffer(TPUInference* inference, size_t index)

    int tpu_inference_copy_output_buffer(TPUInference* inference, size_t index, void* buffer, size_t size)
    int tpu_program_get_output_buffer_size(const TPUProgram *program, size_t index)
    void *tpu_inference_get_output_buffer(TPUInference *inference, size_t index)
    int tpu_program_get_output_tensor(TPUProgram *program, const TPUInference *inference, TPUTensor *output,
                                      size_t index)

    size_t tpu_program_get_inputs_count(TPUProgram *program)
    size_t tpu_program_get_outputs_count(TPUProgram *program)

    const TPUIONode *tpu_program_get_input_node(TPUProgram* program, size_t index)
    const TPUIONode *tpu_program_get_output_node(TPUProgram* program, size_t index)

    int tpu_program_get_input_index_by_name(const TPUProgram* program, const char *feature_name)
    int tpu_program_get_output_index_by_name(const TPUProgram* program, const char *result_name)

    const char *tpu_program_get_input_name_by_index(const TPUProgram* program, size_t index)
    const char *tpu_program_get_output_name_by_index(const TPUProgram* program, size_t index)

    TPUTensor tpu_program_make_input_tpu_tensor(const TPUProgram* program, size_t index)
    TPUTensor tpu_program_make_input_user_tensor(const TPUProgram* program, size_t index)

    TPUTensor tpu_program_make_output_tpu_tensor(const TPUProgram* program, size_t index)
    TPUTensor tpu_program_make_output_user_tensor(const TPUProgram* program, size_t index)

    ssize_t tpu_tensor_get_size(const TPUTensor* tensor)

    # Program hardware parameters
    const TPUProgramHardwareParameters* tpu_program_get_hardware_parameters(const TPUProgram* program)
    const TPUProgramLUTActivationParameters *tpu_program_hardware_parameters_get_lut_parameters(const TPUProgramHardwareParameters *hw_params)

    unsigned int tpu_program_hardware_parameters_get_lut_input_bit_width(const TPUProgramLUTActivationParameters* lut_params)
    unsigned int tpu_program_hardware_parameters_get_lut_data_bit_width(const TPUProgramLUTActivationParameters* lut_params)
    unsigned int tpu_program_hardware_parameters_get_lut_address_bit_width(const TPUProgramLUTActivationParameters* lut_params)
    unsigned int tpu_program_hardware_parameters_get_lut_output_bit_width(const TPUProgramLUTActivationParameters* lut_params)

    # Device definitions
    uint64_t tpu_get_total_mem(TPUDevice *device, TPUDeviceError *error)
    int tpu_get_error_cnt(TPUDevice *device, TPUDeviceError *error)
    int tpu_get_success_cnt(TPUDevice *device, TPUDeviceError *error)
    uint32_t tpu_get_hardware_id(const TPUDevice *device)
    uint32_t tpu_get_control_unit_version(const TPUDevice *device)
    uint32_t tpu_get_ewp_channels_count(const TPUDevice *device)
    uint32_t tpu_get_ewp_banks_count(const TPUDevice *device)
    uint32_t tpu_get_ewp_bank_size(const TPUDevice *device)
    uint32_t tpu_get_psp_buffer_size(const TPUDevice *device)
    uint32_t tpu_get_sdp_buffer_size(const TPUDevice *device)
    uint32_t tpu_get_bias_buffer_size(const TPUDevice *device)

    uint32_t tpu_get_dws_channel_bit_width(const TPUDevice *device)
    uint32_t tpu_get_dws_data_block_bit_width(const TPUDevice *device)
    uint32_t tpu_get_dws_channels_count(const TPUDevice *device)
    uint32_t tpu_get_dws_optimal_window_size(const TPUDevice *device)
    uint32_t tpu_get_dws_max_window_size(const TPUDevice *device)

    uint32_t tpu_get_axi_address_width(const TPUDevice *device)
    uint32_t tpu_get_dma_channels_count(const TPUDevice *device)

    uint32_t tpu_get_ddr_banks_count(const TPUDevice *device)
    uint64_t tpu_get_ddr_bank_size(const TPUDevice *device)
    uint32_t tpu_get_axi_word_length(const TPUDevice *device)
    uint32_t tpu_get_cache_word_length(const TPUDevice *device)
    uint32_t tpu_get_cache_bank_size(const TPUDevice *device)
    uint16_t tpu_get_cache_banks_count(const TPUDevice *device)
    int_pair tpu_get_systolic_array_size(const TPUDevice *device)

    unsigned tpu_get_me_data_bit_width(const TPUDevice* device)
    unsigned tpu_get_frequency(const TPUDevice* device)

    const char *tpu_get_ip_version(const TPUDevice *device)
    const char *tpu_get_driver_version(const TPUDevice *device)
    const char *tpu_program_get_ip_version(const TPUProgram *program)
    const char *tpu_program_get_driver_version(const TPUProgram *program)
