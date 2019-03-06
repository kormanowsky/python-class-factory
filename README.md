# Python Class Factory 
A factory for automatic generation of Python classes.
## HOW TO USE:
### 1. Import the library: 
from classfactory import Factory
### 2. Create Factory.Class instance: 
wrapper = Factory.Class(name="ClassName")
### 3. Add classes, methods, properties: 
- wrapper.add_class(class, name)
- wrapper.add_method(method, name)
- wrapper.add_property(value, name)
### 4. Save your class: 
wrapper.save()
### 5. Now use your generated class: 
obj = ClassName()


# Changelog: 
### v0.0.1 (06.03.2019)
- First release

