import os
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
from distutils.core import Command


class Tests(Command):
    """run tests"""

    description = "runs unittest to execute all tests"

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import unittest

        runner = unittest.runner.TextTestRunner()
        test_loader = unittest.TestLoader()
        test = test_loader.discover("tests")
        runner.run(test)


setup(
    name='mercadopagoCTS',
    version='1.3',
    author="MP SDK <mp_sdk@mercadopago.com>",
    author_email="pedro.tavares@monetizze.com.br",
    keywords="api mercadopago checkout payment ipn sdk integration",
    packages=['mercadopagoCTS'],
    url='https://github.com/toxarai/mercadopago-sdk-python',
    description='Mercadopago SDK module for Payments integration',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires='requests>=2.4.3',
    cmdclass = {'test': Tests},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3.4",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: Freely Distributable",
    ],
)
