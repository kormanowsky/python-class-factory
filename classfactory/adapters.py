##############################
# ClassFactory adapters file
# You may add your own adapter by calling AdapterManager.add_adapter(class_name, adapter_class)
##############################

from classfactory.functions import *


class BaseAdapter:

    def __init__(self):
        pass

    # This must be overridden in child classes
    def adapter_fn(self, value):
        return str(value)

    def name_getter_fn(self, value):
        raise NotImplementedError()

    def adapt(self, value):
        return self.adapter_fn(value)

    def get_name(self, value):
        return self.name_getter_fn(value)


class AdapterManager:

    def __init__(self):
        self.adapters = {
            "str": StrAdapter(),
            "function": FunctionAdapter(),
            "class": ClassAdapter(),
        }

    def add_adapter(self, value_type, adapter):
        self.adapters[value_type] = adapter

    def get_appropriate_adapter(self, value):
        t = type_str(value)
        adapter = BaseAdapter()
        if t in self.adapters:
            adapter = self.adapters[t]
        return adapter


class StrAdapter(BaseAdapter):

    def adapter_fn(self, value):
        value = value.replace('"', '\\"')
        value = "\"{}\"".format(value)
        return value


class FunctionAdapter(BaseAdapter):

    def adapter_fn(self, value):
        value_lines = inspect.getsourcelines(value)[0]
        indent = 0
        for line_num, line in enumerate(value_lines):
            if line_num == 0:
                indent = line.index("def")
                line = line.replace(line.split("def ")[1].split("(")[0], "__name_placeholder__")
            line = line[indent:]
            line = line.replace("\n", "")
            value_lines[line_num] = line
        return "\n".join(value_lines)

    def name_getter_fn(self, value):
        value_lines = inspect.getsourcelines(value)[0]
        return value_lines[0].split("def ")[1].split("(")[0]


class ClassAdapter(BaseAdapter):

    def adapter_fn(self, value):
        raise NotImplementedError()

    def name_getter_fn(self, value):
        value_lines = inspect.getsourcelines(value)[0]
        return value_lines[0].split("class ")[1].split(":")[0]
