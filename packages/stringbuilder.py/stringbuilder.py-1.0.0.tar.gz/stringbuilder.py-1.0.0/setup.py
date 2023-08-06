from setuptools import setup

ld="""Example
-------
```python
import stringbuilder

@stringbuilder
def mystring():
    yield "foo"
    yield 1234
    yield '\n'
    yield object()
    yield '\n'
    yield "bar"

print(mystring)
## foo1234
## <object object at 0xdeadbeefcafe>
## bar
```"""

setup(
    name='stringbuilder.py',
    packages=["stringbuilder"],
    description="Functional String Building",
    long_description=ld,
    long_description_content_type="text/markdown",
    version='1.0.0',
    author='Perzan',
    author_email='PerzanDevelopment@gmail.com',
    install_requires=["onetrick~=2.1"]
)