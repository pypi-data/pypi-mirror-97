class EnumMeta(type):

    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)
        vals = set()
        for k, v in attrs.items():
            if k.startswith("__"):
                continue
            if v in vals:
                raise Exception("value [%s] duplicated" % v)
            vals.add(v)
        cls.__vals = vals

    def __call__(cls, *args, **kwargs):
        raise Exception("can not construct Enum instance")

    def __contains__(cls, x):
        return x in cls.__vals

    def __iter__(cls):
        return iter(cls.__vals)
