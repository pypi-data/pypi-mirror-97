class SingletonMeta(type):

    def __init__(cls, name, bases, attrs):
        cls.__instance = None
        super().__init__(name, bases, attrs)

    def __call__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__call__(*args, **kwargs)
        return cls.__instance

