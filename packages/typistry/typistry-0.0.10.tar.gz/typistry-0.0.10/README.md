# Typistry

Typistry simply takes a `yaml` file, and `json schema` representing a `python dataclass`, and allows you to validate that the yaml file conforms the json schema and then return an instance of the dataclass with attributes populated from the yaml.

For example, typistry allows you to take:

`test_class.py`
```python
from dataclasses import dataclass
from typistry.protos.proto_object import ProtoObject
from typistry.test.support.types.test_class import TestClass

@dataclass
class TestClass:
    test: str
```
`validations/test_class/schema.json`:

```json
{
  "$schema": "http://json-schema.org/draft-04/schema#",
  "title": "TestClassSchema",
  "properties": {
    "type": {
      "type": "string" ,
      "enum": ["test_class"]
    },
    "test": { "type": "string" }
  }, "required": ["type", "test"]
}
```
along with `test.yaml`:

```yaml
type: "test_class"
test: "string"
```

to produce

```python
from typistry.validators.base import validate_files

objects: List[Union[Any, InvalidObject]] = validate_files("test.yaml")
objects >>
[TestClass(test='string')]
```

Note that in this mode it assumes that the `test_class` and `TestClass` are named consistently.

Typistry also provides convenience methods for filtering out specific types to make the signature more strongly typed so it can be used with static type checking tools like `mypy`:

```python
test_classes: List[TestClass] = filter_type(objects, TestClass) 
>> [TestClass(test='string'), TestClass(test='other_string')]

invalid: List[InvalidObject] = filter_type(objects, InvalidObject)
>> [
     InvalidObject(message="Schema error : 'bad_type' is not of type 'integer'"), 
     InvalidObject(message='Schema not found: test_bad_class'), 
     InvalidObject(message='Error building class, check json schema matches class definition'), 
     InvalidObject(message="Invalid YAML {file}: {yaml_load}.  Parsed object must contain 'type'")
]
```

In addition to the above interface, typistry allows you to pass a data class directly into the validation method to return more strongly typed objects without a proto object or filtering:


```python
test_classes: List[Union[TestClass, InvalidObject]] = validate_files("test.yaml", "validations/", to_class = TestClass)
```

You can also override or specify the ProtoClass or build funciton that typistry uses to build the object:

`/validations/other_class/__init__.py`
```python
from typistry.protos.proto_object import ProtoObject
from typistry.test.support.types.other_class import OtherClass

class OtherClassProto(ProtoObject):

    def build_class(self):
        return OtherClass

    def build(self):
        return OtherClass(self.dict.attributes()["test"] + 10)
```

# Purpose
For those that come from a type driven background like Scala, typistry aims (eventually) to become a similar to https://circe.github.io/circe/ to allow you to get a tighter control on type validation decoding/encoding in python in spite of its dynamic nature.  Therefore typistry is assumed to be used with tools like `mypy` for static type validation.  You can see the `mypy.ini` for reference, typistry leverages dry-python returns along with its mypy plugins.

# Why not cls(**attributes)

An alternative implementation would simply try something like:
```python
try:
    cls(**attributes)
except Exception as e:
    return InvalidObject()
```
but by tieing validation in with json-schema you get a much richer interface for validating that the parsed attributes confirm to expectations, including things like nested class and with proto objects you get the ability to overwrite the building of the cls by passing in a builder object.

# TODO

This library while small is in very early development.   Two possible future directions to take it are:

- [ ] Remove the need for a proto class (security concerns require it currently)
- [ ] Remove the need to specify schema.json and simply generate it based upon the dataclass (including nested classes)
- [ ] Support Union types
- [ ] Supported Nested Objects


