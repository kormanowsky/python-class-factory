import classfactory.entities

class Factory:

    FILE_PATH = "{}.py"

    Class = entities.Class
    Method = entities.Method
    Property = entities.Property

    @classmethod
    def produce(cls, *args, **kwargs):
        name = args[0]
        entity = cls.Class(name=name)
        for key in kwargs:
            entity.add_member(kwargs[key], key)

        file_name = Factory.FILE_PATH.format(name)
        with open(file_name, "w+") as produce_file:
            for string in entity.get_code():
                produce_file.write("{}\n".format(string))
        mod = __import__(name, fromlist=[name])
        generated_class = getattr(mod, name)
        if args[1] is None:
            return generated_class
        args[1][name] = generated_class
        return args[1]
