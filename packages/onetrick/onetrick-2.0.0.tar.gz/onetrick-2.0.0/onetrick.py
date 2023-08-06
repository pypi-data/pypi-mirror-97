def pony(function):
    from types import ModuleType
    from sys import modules

    class OneTrickModule(ModuleType):
        def __call__(self, *args, **kwargs):
            return function(*args, **kwargs)

    def pony(modulename:str):
        module = modules[modulename]
        module.__class__ = OneTrickModule

    function.onetrick = pony
    return function

# ~pony ~pony ~onetrick ~name (it sort of rhymes)
pony(pony).onetrick(__name__)