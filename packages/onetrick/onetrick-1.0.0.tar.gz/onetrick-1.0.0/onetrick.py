def pony(arg):
    from inspect import ismodule
    from types import ModuleType
    from sys import modules

    def pony(module, func):
        class OneTrickModule(ModuleType):
            def __call__(self, *args, **kwargs):
                return func(*args, **kwargs)
            
        module.__class__ = OneTrickModule
    
    if ismodule(arg):
        module = arg
        def onetrick(func):
            pony(module, func)
            return arg
        return onetrick
    elif callable(arg):
        func = arg
        module = modules[func.__module__]
        pony(module, func)
    
    return arg

pony(pony)