from setuptools import setup, find_packages
from codecs import open
from os import path
try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst').replace("\r", "")
except(IOError, ImportError):
    long_description = open('README.md').read().replace("\r", "")

setup(
    name='unicornhatsimulator',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    version='1.0.1',
    description='Unicorn HAT (HD) simulator - Originally by Jannis Hermanns <jannis@gmail.com>, modified by Mark Pitman <mark.pitman@gmail.com> and then adjusted by Matt Brash <matt@brash.ca>',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    author='Matt Brash',
    author_email='matt@brash.ca',
    url='https://github.com/MisterBrash/unicornhatsimulator',
    download_url='https://github.com/MisterBrash/unicornhatsimulator/raw/main/archives/unicornhatsimulator-1.0.2.tar.gz',
    keywords=['raspberrypi', 'unicorn', 'hat', 'led', 'simulator'],
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3'
    ],
    install_requires=['pygame'],
)
