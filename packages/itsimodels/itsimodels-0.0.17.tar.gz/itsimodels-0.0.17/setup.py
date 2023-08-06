import setuptools

from itsimodels import __version__


setuptools.setup(
    name='itsimodels',
    version=__version__,
    author='Splunk, Inc.',
    description='Model Definitions for Splunk IT Service Intelligence',
    url='https://github.com/splunk/itsi-models',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=2.7',
)
