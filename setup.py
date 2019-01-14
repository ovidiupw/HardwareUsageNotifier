# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

# The documentation related to each setup keyword can be found here:
# https://setuptools.readthedocs.io/en/latest/setuptools.html#options

setup(
    name='HardwareUsageNotifier',
    version='0.1.0',
    author='Ovidiu Pricop',
    author_email='ovidiu.pricop@gmail.com',
    packages=find_packages(exclude=('tests')),
    description='A service that lets the user set thresholds for hardware usage and get notified when those thresholds are exceeded.',
    long_description=open('README.md').read(),
    entry_points='''
        [console_scripts]
        hardware_usage_notifier=hardware_usage_notifier.cli.hardware_usage_notifier:cli
    ''',
    # pytest-env as install_requires in order for CLI-run tests to have environment variable support
    install_requires=['click', 'jsonschema', 'click_log', 'pytest-env'],
    # pytest-env also in tests_require in order for IDE-run tests to have environment variable support
    tests_require=['pytest', 'pytest-cov', 'pytest-env']
    # url='http://pypi.python.org/pypi/TowelStuff/', Currently the URL is omitted because the package is not vended
    # license='LICENSE.txt', Currently the package is not licensed, but it will be in the near future
)
