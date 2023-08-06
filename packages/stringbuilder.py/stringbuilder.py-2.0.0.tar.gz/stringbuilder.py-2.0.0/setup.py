from setuptools import setup

ld="""Example #1
----------
```python
import stringbuilder

@stringbuilder
def buildstring():
    yield "foo"
    yield 1234
    yield object()
    yield "bar"

mystring = buildstring(delim='\n')

print(mystring)
```
Output:
```
foo
1234
<object object at 0xdeadbeefcafe>
bar
```
Example #2
----------

```python
@stringbuilder.build(delim='\n')
def mystring():
    yield "foo"
    yield 1234
    yield object()
    yield "bar"

print(mystring)
```
Output:
```
foo
1234
<object object at 0xdeadbeefcafe>
bar
```"""

setup(
    name='stringbuilder.py',
    packages=["stringbuilder"],
    description="Functional String Building",
    long_description=ld,
    long_description_content_type="text/markdown",
    version='2.0.0',
    author='Perzan',
    author_email='PerzanDevelopment@gmail.com',
    install_requires=["onetrick~=2.1"]
)