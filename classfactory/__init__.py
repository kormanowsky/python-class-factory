import classfactory.entities

class Factory:

    FILE_PATH = "{}.py"

    Class = entities.Class
    Method = entities.Method
    Property = entities.Property

    @classmethod
    def create(cls, __classname__, **kwargs):
        entity = cls.Class(name=__classname__)
        for key in kwargs:
            entity.add_member(kwargs[key], key)

    @classmethod
    def produce(cls, classobject, loc=None, magicmethods=True):
        file_name = Factory.FILE_PATH.format(classobject.name)
        with open(file_name, "w+") as produce_file:
            for string in classobject.get_code():
                produce_file.write("{}\n".format(string))
        mod = __import__(classobject.name, fromlist=[classobject.name])
        generated_class = getattr(mod, classobject.name)
        if loc is None:
            return generated_class
        loc[classobject.name] = generated_class
        return loc

    @classmethod
    def produce_fast(cls, entity_type, name, properties, methods, classes, loc=None, magicmethods=True):
        entity = entity_type(entities.Empty, name)

        return cls.produce(entity, loc, magicmethods)

    @classmethod
    def produce_fast_existing(cls, entity_type, source, name, properties, methods, classes, loc=None, magicmethods=True):
