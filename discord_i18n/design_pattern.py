class Singleton:
    # Maybe we should check about __init__ parameters?
    __instance__: 'Singleton' = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance__ is None:
            cls.__instance__ = super().__new__(cls)

        return cls.__instance__
