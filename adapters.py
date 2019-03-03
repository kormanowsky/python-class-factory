from factory import type_str


class BaseAdapter:

    def __init__(self, adapter_type):
        self.adapter_type = adapter_type

    # This must be overridden in child classes
    def adapter_fn(self, value):
        return str(value)

    def adapt(self, value):
        if not type_str(value) == self.adapter_type:
            raise ValueError("value must be a {} object".format(self.adapter_type))
        return self.adapter_fn(value)


class StrAdapter(BaseAdapter):

    def __init__(self):
        super(StrAdapter, self).__init__('str')

    def adapter_fn(self, value):
        print(value)
        return ""

