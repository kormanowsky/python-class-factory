from classfactory.adapters import AdapterManager
from classfactory.functions import *


class Empty:
    pass


class Entity:

    def __init__(self, entity_class, source, name=None):
        self.adapter = AdapterManager().get_appropriate_adapter(source)
        if entity_class not in [Class, Method, Property]:
            raise ValueError("Entity class must be either "
                             "Class, Method or Property")
        if name is None:
            name = self.adapter.get_name(source)
        if not entity_class.check_name(name):
            raise ValueError("Entity name is not valid.")
        self.name = str(name)
        if not entity_class.check_source(source):
            raise ValueError("Entity source is not valid.")
        self.source = source

    def get_code(self):
        raise NotImplementedError()


class Class(Entity):

    def __init__(self, source=Empty, name=None):
        super(Class, self).__init__(Class, source, name)
        self.classes = {}
        self.methods = {}
        self.properties = {}
        if source != Empty:
            for t in [Class, Method, Property]:
                members = inspect.getmembers(source, t.check_source)
                for member in members:
                    mem_name, mem_source = member
                    self.add_member(mem_name, mem_source)

    @classmethod
    def check_name(self, name):
        # Todo
        return True

    @classmethod
    def check_source(cls, source):
        return type_str(source) == "class"

    def add_member(self, source, name=None):
        # Do not add __MEMBER__ methods and mro method
        if type_str(name) == "str" and (name[:2] == "__" or name == "mro"):
            return
        if Class.check_source(source):
            self.add_class(source, name)
        elif Method.check_source(source):
            self.add_method(source, name)
        else:
            self.add_property(source, name)

    def add_class(self, source=Empty, name=None):
        if name in self.classes:
            raise ValueError("{} is already in class {}".format(name, self.name))
        self.classes[name] = Class(source, name)

    def add_method(self, source, name=None):
        if name in self.methods:
            raise ValueError("{} is already in class {}".format(name, self.name))
        self.methods[name] = Method(source, name)

    def add_property(self, source, name):
        if name in self.properties:
            raise ValueError("{} is already in class {}".format(name, self.name))
        self.properties[name] = Property(source, name)

    def set_class(self, source=Empty, name=None):
        if name not in self.classes:
            raise ValueError("{} is not in class {}".format(name, self.name))
        self.classes[name] = Class(source, name)

    def set_method(self, source=Empty, name=None):
        if name not in self.methods:
            raise ValueError("{} is not in class {}".format(name, self.name))
        self.methods[name] = Method(source, name)

    def set_property(self, source=Empty, name=None):
        if name not in self.properties:
            raise ValueError("{} is not in class {}".format(name, self.name))
        self.properties[name] = Property(source, name)

    def del_class(self, name):
        if name not in self.classes:
            raise ValueError("{} is not in class {}".format(name, self.name))
        del self.classes[name]

    def del_method(self, name):
        if name not in self.methods:
            raise ValueError("{} is not in class {}".format(name, self.name))
        del self.methods[name]

    def del_property(self, name):
        if name not in self.properties:
            raise ValueError("{} is not in class {}".format(name, self.name))
        del self.properties[name]

    def get_code(self):
        strings = [
            "# Class {} generated by ClassFactory v0.0.1".format(self.name),
            "class {}:".format(self.name),
        ]
        for c in self.classes:
            strings.append("")
            c_code = c.get_code()
            for c_string in c_code[:-1]:
                strings.append("    {}".format(c_string))
        if len(self.classes):
            strings.append("")

        for p in self.properties:
            strings.append("    {}".format(p.get_code()))
        if len(self.properties):
            strings.append("")

        for m in self.methods:
            strings.append("")
            for m_string in m.get_code():
                strings.append("    {}".format(m_string))
        if len(self.methods):
            strings.append("")

        if len(strings) == 2:
            strings.append("    pass")
            strings.append("")
        return strings


class Method(Entity):

    METHOD_NAME_PLACEHOLDER = "__name_placeholder__"

    def __init__(self, source, name=None):
        super(Method, self).__init__(Method, source, name)

    @classmethod
    def check_name(self, name):
        # Todo
        return True

    @classmethod
    def check_source(cls, source):
        return type_str(source) == "function"

    def get_code(self):
        return self.adapter.adapt(self.source).replace(self.METHOD_NAME_PLACEHOLDER, self.name).split("\n")


class Property(Entity):

    def __init__(self, source, name):
        if callable(source):
            raise ValueError("Source for Property is callable. Use Method for that source instead.")

        super(Property, self).__init__(Property, source, name)

    @classmethod
    def check_name(self, name):
        # Todo
        return True

    @classmethod
    def check_source(cls, source):
        return not type_str(source) in ["class", "function"]

    def get_code(self):
        return "{} = {}".format(self.name, self.adapter.adapt(self.source))
