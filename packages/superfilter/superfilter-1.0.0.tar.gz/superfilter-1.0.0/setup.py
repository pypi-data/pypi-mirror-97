from setuptools import setup

ld = """Recommended example usage
-------------------------
```python
import superfilter
from argskwargs import argskwargs

@superfilter
def myfilter():
    return argskwargs(foo="foobar", message="Hello World!")

@myfilter
def myfunction(foo, message):
    print(message)
    return foo

myfunction() # Arguments are supplied by 'myfilter'
```
Usage with other decorators
---------------------------
```python
import superfilter
from argskwargs import argskwargs

@superfilter
def myfilter(cls):
    return argskwargs(cls, foo="foobar", message="Hello World!")

class MyClass:
    @classmethod
    @myfilter # Decorate with myfilter first
    def myfunction(cls, foo, message):
        print(message)
        return foo

MyClass.myfunction()
```"""

setup(
    name='superfilter',
    version='1.0.0',
    description="Compute implied arguments for your functions",
    long_description=ld,
    long_description_content_type="text/markdown",
    author='Perzan',
    packages=["superfilter"],
    author_email='PerzanDevelopment@gmail.com',
    install_requires=["argskwargs~=2.0", "onetrick~=2.1"],
    python_requires="~=3.5"
)