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
from ipdb import set_trace


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


def joint(classes):
    def wrapper(cls):
        protocols = classes if isinstance(classes, tuple) else (classes,)
        for protocol in protocols:
            if not isinstance(protocol, ProtocolMeta):
                raise TypeError('%s is %s, not a protocol' %
                                (protocol, type(protocol)))

            for m in protocol.__interface__:
                setattr(cls, m.__name__, m)

        return cls
    return wrapper


class InheritException(Exception):

    '''Could not be inherited.'''


class InstantiationException(Exception):

    '''Protocols Could not be instantiated.'''


class ProtocolMeta(type):

    def __new__(cls, name, bases, dct):
        for base in bases:
            if isinstance(base, cls):
                raise InheritException('Could not be inherited from %s' % base)

        newclass = super().__new__(cls, name, bases, dct)
        # Maybe the class to create is jointing a protocol
        newclass._isprotocol = False
        newclass.__interface__ = [getattr(
            newclass, m) for m in dir(newclass) if not m.startswith(
            '__') and callable(getattr(newclass, m))]

        return newclass

    def __call__(self, *args, **kwargs):
        if self._isprotocol is True:
            raise InstantiationException(
                'Protocols Could not be instantiated.')
        else:
            return super().__call__(*args, **kwargs)
