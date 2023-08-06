from ipykernel.kernelapp import IPKernelApp
from .kernel import NativeKernel
IPKernelApp.launch_instance(kernel_class=NativeKernel)
