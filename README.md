# Python Class Factory 
A factory for automatic generation of Python classes.
## HOW TO USE:
1. Create factory.Class instance: o = factory.Class('name')
2. Add classes, methods, properties: o.add_method('methodname', methodfunc)
3. Produce your class: O = factory.Factory.produce(o)
4. Now use your generated class: O().methodname()

# Todos:
1. factory.Class(Class)
2. factory.Method(Method)
3. Set/remove
4. Magic methods: __addclass__, __addmethod__, __addproperty__, __setclass__, __setmethod__, __setproperty__, __removeclass__, __removemethod__, __removeproperty__
5. Static methods

# Changelog: 
- v0.0.1 - First release, I am now writing it.
