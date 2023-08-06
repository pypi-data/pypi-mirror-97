"""
Decorator to create a command line argument
"""


class Command:
    """
    Decorator to create a command line argument
    """
    commands = []

    def __new__(cls, method=None, **kwargs):
        # if method is None the decorator has parameters
        if method is not None:
            setattr(method, '__name__', kwargs.pop('method_name', method.__name__))
            setattr(method, 'kwargs', kwargs)
            setattr(method, 'help', kwargs.get('help', None))
            Command.commands.append(method)
            return method
        new = object.__new__(cls)
        new.kwargs = kwargs
        return new

    def __call__(self, *args, **kwargs):
        method = list(args)[0]
        self.kwargs['method'] = method
        self.__new__(Command, **self.kwargs)
        return method
