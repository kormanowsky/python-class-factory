import classfactory.entities
import inspect


class Factory:

    FILE_PATH = "{}.py"

    Class = entities.Class
    Method = entities.Method
    Property = entities.Property

    classes = {}

    @classmethod
    def generate(cls, *args, **kwargs):
        return cls.generate_existing(cls.__newentity(*args, **kwargs), *args)

    @classmethod
    def generate_existing(cls, entity, *args):
        cls.classes[entity.name] = entity
        generated_class = cls.__write(entity)
        if args[1] is not None:
            args[1][args[0]] = generated_class
        return generated_class

    @classmethod
    def __newentity(cls, *args, **kwargs):
        name = args[0]
        entity = cls.Class(name=name)
        for key in kwargs:
            entity.add_member(kwargs[key], key)
        return entity

    @classmethod
    def __entity(cls, source_class):
        return cls.Class(source=source_class)

    @classmethod
    def __addtoclass(cls, source, name=None, type=Method):
        class_to_add = inspect.stack()[1][0].f_locals['self']
        if class_to_add.__name__ not in cls.classes:
            raise ValueError("We cannot alter that class. "
                             "You must create class using Factory.generate() and then alter it.")
        entity = cls.__entity(class_to_add)
        if type == cls.Method:
            entity.add_method(source, name)
        elif type == cls.Class:
            entity.add_class(source, name)
        else:
            entity.add_property(source, name)
        return cls.generate_existing(entity)

    @classmethod
    def __setinclass(cls, source, name=None):
        class_to_add = inspect.stack()[1][0].f_locals['self']
        if class_to_add.__name__ not in cls.classes:
            raise ValueError("We cannot alter that class. "
                             "You must create class using Factory.generate() and then alter it.")
        entity = cls.__entity(class_to_add)
        if type == cls.Method:
            entity.set_method(source, name)
        elif type == cls.Class:
            entity.set_class(source, name)
        else:
            entity.set_property(source, name)
        return cls.generate_existing(entity)

    @classmethod
    def __delfromclass(cls, source, name=None):
        class_to_add = inspect.stack()[1][0].f_locals['self']
        if class_to_add.__name__ not in cls.classes:
            raise ValueError("We cannot alter that class. "
                             "You must create class using Factory.generate() and then alter it.")
        entity = cls.__entity(class_to_add)
        if type == cls.Method:
            entity.del_method(name)
        elif type == cls.Class:
            entity.del_class(name)
        else:
            entity.del_property(name)
        return cls.generate_existing(entity)

    @classmethod
    def __write(cls, entity):
        file_name = Factory.FILE_PATH.format(entity.name)
        with open(file_name, "w+") as produce_file:
            for string in entity.get_code():
                produce_file.write("{}\n".format(string))
        mod = __import__(entity.name, fromlist=[entity.name])
        generated_class = getattr(mod, entity.name)
        return generated_class

