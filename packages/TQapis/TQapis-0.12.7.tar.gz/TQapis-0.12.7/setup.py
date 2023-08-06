from setuptools import setup
setup(name='TQapis',
version='0.12.7',
description="Python package providing a simple interface to support TreasuryQuants.com's http protocols",
url='https://github.com/treasuryquants/TQPython',
author='Shahram Alavian',
author_email='contact@treasuryquants.com',
maintainer='Tanmay Jain',
maintainer_email='tanmayjain.cs@gmail.com',
license='MIT', # if you want you can use "LICENSE.txt"
packages=['TQapis'],
zip_safe=False,
long_description=open('README.MD').read(),
long_description_content_type='text/markdown',
keywords =["Treasury", "Quant", "TreasuryQuants", "Swap", "Valuations", "Quantitative Finance"],
install_requires=["requests"])
