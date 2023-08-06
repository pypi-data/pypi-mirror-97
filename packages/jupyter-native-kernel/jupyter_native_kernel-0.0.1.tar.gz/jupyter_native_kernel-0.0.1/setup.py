from setuptools import setup

setup(
      packages=['jupyter_native_kernel'],
      install_requires=[
          'jupyterlab',
      ],
      scripts=['jupyter_native_kernel/install_native_kernel'],
      keywords=['jupyter', 'notebook', 'kernel', 'native'],
      include_package_data=True
      )
