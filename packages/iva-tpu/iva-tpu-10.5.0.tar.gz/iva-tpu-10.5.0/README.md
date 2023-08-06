# IVA TPU Python API
## Main entities
### TPUDevice
TPUDevice is a device handle

### TPUProgram
TPUProgram contains TPU instructions and weigths data

## Example
```python
import numpy as np
from iva_tpu import TPUDevice, TPUProgram

from iva_applications.resnet50 import image_to_tensor
from iva_applications.imagenet import tpu_tensor_to_classes
from PIL import Image

image = Image.open('ILSVRC2012_val_00000045.JPEG')
tensor = image_to_tensor(image)

device = TPUDevice()
program = TPUProgram("resnet50.tpu")
device.load(program)  # now device is ready to make inference

output = device.run([tensor], dtype=np.float32)
tpu_tensor_to_classes(output[0], top=1)

from timeit import timeit
timeit(lambda: device.run([tensor]), number=100)

```

## TPU Raw buffer examples
```
from iva_tpu import TPUDevice, TPUProgram
program = TPUProgram("omega_program_dnn_quant_3.0.0.tpu")
device = TPUDevice()
device.load(program)

with open("f.bin", "rb") as f:
    buf=f.read()

device.set_input_buffer(buf, 0)
device.run_inference()

for i in range(3):
  o = device.get_output_buffer(i)
  with open(f"o{i}.bin", "wb") as f:
    f.write(o)
```
