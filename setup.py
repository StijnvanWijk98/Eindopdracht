from setuptools import setup, Extension
import pybind11

setup(
    name='actuators',
    version='0.1',
    ext_modules=[
        Extension(
            'actuators',
            ['actuators.cpp'],
            include_dirs=[pybind11.get_include()],
            language='c++',
        ),
    ],
    zip_safe=False,
)