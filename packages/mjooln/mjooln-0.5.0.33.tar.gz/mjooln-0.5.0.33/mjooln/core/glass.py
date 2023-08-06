class Glass:
    @classmethod
    def glass(cls, *args, **kwargs):
        """
        If input is a class instance, return instance. If not, call
        constructor with same input arguments
        """
        if args and len(args) == 1 and not kwargs and isinstance(args[0], cls):
            return args[0]
        else:
            return cls(*args, **kwargs)