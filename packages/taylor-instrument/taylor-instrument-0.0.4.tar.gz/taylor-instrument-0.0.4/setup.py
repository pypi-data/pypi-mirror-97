"""
Pip.Services Instrument
"""

from setuptools import find_packages
from setuptools import setup

try:
    readme = open('README.md').read()
except:
    readme = __doc__

setup(
    name='taylor-instrument',
    version='0.0.4',
    url='',
    license='',
    description='Instrument service for logs and metrics',
    author='',
    author_email='',
    long_description=readme,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=True,
    platforms='any',
    install_requires=[
        'pip_services3_commons',
        'pip_services3_components',
        'pip_services3_rpc',
        'pip_services3_elasticsearch',
        'pip_services3_prometheus'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
