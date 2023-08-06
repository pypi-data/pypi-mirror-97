from setuptools import setup

ld = """Example
-------
```python
import chainop, argparse

parser = argparse.ArgumentParser()
chop = chainop(parser).add_argument("--arg0")("--arg1")("--foobar")("--arg3", type=int)

foobar_arg:argparse.Action = chop[2] # Get the returned value for the 3rd add_argument call
print(foobar_arg.dest)

chop[3].default = 0

args = parser.parse_args()
```"""

setup(
    name='chainop',
    packages=["chainop"],
    version='1.0.1',
    description="Simple method-chaining tool",
    long_description=ld,
    long_description_content_type="text/markdown",
    author='Perzan',
    author_email='PerzanDevelopment@gmail.com',
    install_requires=["onetrick~=2.1"],
)