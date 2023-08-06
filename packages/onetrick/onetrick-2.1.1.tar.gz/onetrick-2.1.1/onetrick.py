def pony(arg):
    from types import ModuleType
    from sys import modules

    def onetrick(function):
        class OneTrickModule(ModuleType):
            def __call__(self, *args, **kwargs):
                return function(*args, **kwargs)

        def pony(modulename:str):
            module = modules[modulename]
            module.__class__ = OneTrickModule
        
        return pony
    
    if callable(arg):
        function = arg
        function.onetrick = onetrick(function)
    elif isinstance(arg, str):
        modulename:str = arg
        def pony(function):
            onetrick(function)(modulename)
            return function
        return pony

    return arg

pony(__name__)(pony)