import inspect


class BaseAdapter:

    def __init__(self):
        pass

    # This must be overridden in child classes
    def adapter_fn(self, value):
        return str(value)

    def adapt(self, value):
        return self.adapter_fn(value)


class StrAdapter(BaseAdapter):

    def adapter_fn(self, value):
        value = value.replace('"', '\\"')
        value = "\"{}\"".format(value)
        return value


class FunctionAdapter(BaseAdapter):

    def adapter_fn(self, value):
        print(value)
        value_lines = [""] + inspect.getsourcelines(value)[0]
        for line_num, line in enumerate(value_lines):
            if line_num == 1:
                line = line.replace(line.split(" ")[1].split("(")[0], "__name_placeholder__")
            line = line.replace("\n", "")
            value_lines[line_num] = line
        return "\n".join(value_lines)