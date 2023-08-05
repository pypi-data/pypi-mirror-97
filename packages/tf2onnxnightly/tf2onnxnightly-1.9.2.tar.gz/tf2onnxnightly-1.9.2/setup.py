# SPDX-License-Identifier: Apache-2.0


from setuptools import setup, find_packages

setup(
    name="tf2onnxnightly",
    version="1.9.2",
    description='Tensorflow to ONNX converter',
    setup_requires=['pytest-runner'],
    tests_require=['graphviz', 'parameterized', 'pytest', 'pytest-cov', 'pyyaml'],
    packages=find_packages(),
    license='Apache License v2.0',
    author='onnx@microsoft.com',
    author_email='onnx@microsoft.com',
    url='https://github.com/tensorleap/tensorflow-onnx',
    download_url='https://github.com/tensorleap/tensorflow-onnx/archive/v1.9.1-nightly-build.tar.gz',
    install_requires=['numpy>=1.14.1', 'onnx>=1.4.1', 'requests', 'six', 'flatbuffers']
)
