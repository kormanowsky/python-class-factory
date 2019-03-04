class Factory:

    FILE_PATH = "{}.py"

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
