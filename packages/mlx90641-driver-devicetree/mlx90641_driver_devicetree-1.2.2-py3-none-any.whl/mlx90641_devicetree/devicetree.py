import os
import ctypes
from mlx90641 import *


def load_driver():
    dev = MLX90641()

    cfp = os.path.dirname(os.path.realpath(__file__))
    machine = 'windows'
    shared_lib_file = 'mlx90641_driver_devicetree.dll'
    if os.environ.get('OS','') != 'Windows_NT':
        import platform
        machine = platform.machine()
        shared_lib_file = 'libmlx90641_driver_devicetree.so'

    lib = ctypes.CDLL(os.path.join(cfp, 'libs', machine, shared_lib_file), mode=ctypes.RTLD_GLOBAL)

    # struct MLX90641DriverRegister_t *MLX90641_get_register_devicetree(void);
    _get_register_devicetree = lib.MLX90641_get_register_devicetree
    _get_register_devicetree.restype = ctypes.POINTER(ctypes.c_uint16)
    _get_register_devicetree.argtypes = []
    dev._register_driver(_get_register_devicetree())



