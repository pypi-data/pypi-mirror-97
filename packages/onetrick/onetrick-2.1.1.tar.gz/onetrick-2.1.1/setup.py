from setuptools import setup

ld = """If your project exposes a module 
--------------------------------
`mymodule.py`:
```python
import onetrick

@onetrick(__name__)
def myfunction():
    print("Hello world!")
```
Then it can be called from elsewhere:
```python
import mymodule

#Either like this
mymodule() # (Hello world!)

#Or like this
mymodule.myfunction() # (Hello world!)
```

If your project exposes a package
---------------------------------
```
.
+-- mypackage
|   +-- __init__.py
|   +-- mymodule.py
```
`mymodule.py`:
```python
import onetrick

@onetrick
def myfunction():
    print("Hello world!")
```
`__init__.py`:
```python
from .mymodule import myfunction

myfunction.onetrick(__name__)
```
Then it can be called from elsewhere:
```python
import mypackage

#Either like this
mypackage() # (Hello world!)

#Or like this
mypackage.myfunction() # (Hello world!)
```"""

setup(
    name='onetrick',
    version='2.1.1',
    description="one module, one call",
    long_description=ld,
    long_description_content_type="text/markdown",
    author='Perzan',
    author_email='PerzanDevelopment@gmail.com',
    python_requires="~=3.5",
    py_modules=["onetrick"]
)