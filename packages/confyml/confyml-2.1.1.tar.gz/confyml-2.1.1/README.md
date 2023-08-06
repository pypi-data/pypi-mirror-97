# confyml
Project to allow easy application of config to python methods and functions.

The package allows the user to provide keyword arguments to any decorated function/method. If keyword arguments are 
passed to the function/method directly in the code this will overwrite any configured behaviour. By having this, one can
easily support configurability in applications without the need for code changes 
or unwieldy config classes that also require code change to alter.

## install
Install like any other python package, from pypi
```shell
pip install confyml
```

## usage

At the definition of classes, methods and functions, import `confyml` and apply the decorator to allow the function to
become configurable.
```python
# example_module.py
from confyml import confyml


config = confyml.get_config()


class ExampleClass:
    
    @config.apply
    def __init__(self, kwarg=None):
        self.kwarg = kwarg
    
    @config.apply
    def example_method(self, arg1, kwarg_2=None):
        return arg1, self.kwarg, kwarg_2


@config.apply()
def example_function(arg2, kwarg_3=None):
    return arg2, kwarg_3
```
Create a `yaml` file to hold the definition. Default mode for `confyml` is `mcf`: modules, classes and functions; where
the yaml file has a structure like the one below.
```yaml
# example.yaml
example_module:
  ExampleClass:
    kwarg: 'class_kwarg'
    example_method:
      kwarg_2: 'method_kwarg'
  example_function:
    kwarg_3: 'function_kwarg'
```
In the calling script, the application that uses the classes and functions, set the config file to follow.
```python
# main.py
from confyml import confyml
import example_module

confyml.set_config('example.yaml')

e = example_module.ExampleClass()

print(e.example_method('arg1'))
print(example_module.example_function('arg2'))
```
```
$ python main.py
arg1 class_kwarg method_kwarg
arg2 function_kwarg
```

The use should be one config per application. 

Keyword arguments provided to the function/method directly will overwrite the config file's behaviour.

```python
# main.py
from confyml import confyml
import example_module

confyml.set_config('example.yaml')

e = example_module.ExampleClass(kwarg='direct_kwarg')

print(e.example_method('arg1'))
print(example_module.example_function('arg2', 'direct_func_kwarg'))
```
```
$ python main.py
arg1 direct_kwarg method_kwarg
arg2 direct_func_kwarg
```
## modes

The config can also be provided with a `mode` argument, 
```python
# main.py
from confyml import confyml


confyml.set_config('<yaml_filepath>', mode='<mode>')
```
to set the level
of the config. By default the mode is `mcf`, which supports a yaml structure of 
```yaml
module:
  Class:
    <defined_kwargs>
    method:
      <defined_kwargs>
  function:
    <defined_kwargs>
```
mode `cf` - classes and methods and/or functions
```yaml
Class:
  <defined_kwargs>
  method:
    <defined_kwargs>
function:
  <defined_kwargs>
```
mode `mf` - modules and functions
```yaml
module:
  function:
    <defined_kwargs>
```
and finally mode `f` - functions only
```yaml
function:
  <defined_kwargs>
```

Use the mode that best suits your application. 

