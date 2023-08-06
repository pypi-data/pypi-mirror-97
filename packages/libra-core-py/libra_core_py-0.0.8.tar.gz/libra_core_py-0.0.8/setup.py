import os
from setuptools import setup

requirements = [
    "pika==1.1.0",
    "influxdb==5.3.1"
]

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='libra_core_py',
    version='0.0.8',
    packages=[
            "libra_core",
    ],
    license='BSD License',  # example license
    description='libra core',
    install_requires=requirements,
    long_description_content_type="text/markdown",
    url='',
    author='yujianjia',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',  # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.8',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
