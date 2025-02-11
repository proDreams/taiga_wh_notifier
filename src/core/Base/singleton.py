class Singleton:
    """
    Ensures that only one instance of the class `Singleton` is created and provides access to it globally.
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
