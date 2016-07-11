'''
    protocol lib for python
    usage:
    >>>
    >>> @protocol
    ... class protocol_1():
    ...     def get_class_name(self):
    ...         return self.__class__.__name__
    ...
    >>> @joint(protocol_1)
    ... class MyClass():
    ...     pass
    ...
    >>> a = MyClass()
    >>> a.get_class_name()
    'MyClass'

    >>>
    >>> from hashlib import MD5
    >>> from time import ctime
    >>>
    >>> @protocol
    ... class protocol_2(ParentClass):
    ...     def func(self, *args, **kwargs):
    ...         pass
    ...

    You can create protocol by inherit, but protocol could not be inherited.
    One protocol can also contain other protocols, which means one protocol 
    can be created under other protocols, but protocol itself can not be inherited.

'''
import inspect
from warnings import warn
from IPython.core.debugger import Tracer
set_trace = Tracer()


def get_callables(cls):
    methods = dir(cls)
    return (getattr(cls, m) for m in methods if not m.startswith(
        '_') and callable(getattr(cls, m)))


def tuplize(obj):
    ''' Make obj a tuple if it's not a tuple, otherwise just return obj.'''
    return obj if isinstance(obj, tuple) else (obj,)


def listize(obj):
    ''' Make obj a list if it's not a tuple, otherwise just return obj.'''
    return obj if isinstance(obj, list) else [obj, ]


def add_metaclass(metaclass):
    """Class decorator for creating a class with a metaclass."""
    def wrapper(cls):
        orig_vars = cls.__dict__.copy()
        slots = orig_vars.get('__slots__')
        if slots is not None:
            if isinstance(slots, str):
                slots = [slots]
            for slots_var in slots:
                orig_vars.pop(slots_var)
        orig_vars.pop('__dict__', None)
        orig_vars.pop('__weakref__', None)
        return metaclass(cls.__name__, cls.__bases__, orig_vars)
    return wrapper


def protocol(cls):
    p = add_metaclass(ProtocolMeta)(cls)
    p._isprotocol = True
    return p

xxx = None


def joint(*protocols):
    joint.warning = False
    def wrapper(cls):
        cls.__protocols__ = set()
        
        for protocol in protocols:
            # Only protocols could be jointed
            if not isinstance(protocol, ProtocolMeta):
                raise TypeError('%s is %s, not a protocol' %
                                (protocol, type(protocol)))

            # attach protocol's __protocols__
            cls.__protocols__.update(getattr(protocol, '__protocols__', set()))

            # Here protocol interface could be overrided by other
            # protocols behind, but cls method with same __name__
            # as one of protocol's interface would not be overrided.
            # See detials in test.py
            for method in protocol.__interface__:
                if method.__name__ not in dir(cls):
                    setattr(cls, method.__name__, method)
                    cls.__protocols__.update({protocol})
                else:
                    if not joint.warning:
                        continue

                    exist_method = getattr(cls, method.__name__)
                    warning_string = '''
                    In jointing %s, conflict function name:
                    "%s" with "%s"
                    using the second one above.
                    '''%(cls, method, exist_method)
                    warn(warning_string)

        return cls
    return wrapper


class InheritException(Exception):

    ''' Could not be inherited.'''


class InstantiationException(Exception):

    ''' Protocols Could not be instantiated.'''


class DuplicateProtocolException(Exception):
    ''' No reason to joint duplicated protocols'''


class ProtocolMeta(type):

    def trimExtended(self):
        ''' trim protocol hierarchy'''
        assert(not hasattr(self, '_isprotocol'))
        print(self)
        print('trimExtended')

    def get_protocol_hierarchy(self):
        assert(not hasattr(self, '_isprotocol'))

        for p in self.__protocols__:
            print(p)
            for i in p.__interface__:
                print(i)
            print()

    def __new__(cls, name, bases, dct):
        for base in bases:
            if isinstance(base, cls):
                raise InheritException('Could not be inherited from %s' % base)

        name = name if name.startswith('ptl') else ''.join(('ptc', name))
        newclass = super().__new__(cls, name, bases, dct)
        # Maybe the class to create is jointing a protocol
        newclass._isprotocol = False
        # TODO 1:
        newclass.get_protocol_hierarchy = cls.get_protocol_hierarchy
        newclass.__interface__ = get_callables(newclass)

        return newclass

    def __call__(self, *args, **kwargs):
        if self._isprotocol is True:
            raise InstantiationException(
                'Protocols Could not be instantiated.')
        else:
            return super().__call__(*args, **kwargs)
