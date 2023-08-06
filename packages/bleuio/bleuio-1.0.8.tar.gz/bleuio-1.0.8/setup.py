from setuptools import find_packages, setup

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='bleuio',
    version='1.0.8',
    packages=find_packages(include=['bleuio_lib','bleuio_tests']),
    url='https://smart-sensor-devices-ab.github.io/ssd005-manual/',
    install_requires=['pyserial'],
    python_requires='>=3.6',
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Smart Sensor Devices',
    author_email='smartzenzor@gmail.com',
    description='Library for using the bleuio dongle.'
)
