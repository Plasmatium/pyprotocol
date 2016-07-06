'''
    protocol lib for python
    usage:
    >>>
    >>> @protocol
    ... class protocol_1():
    ...     def get_class_name(self):
    ...         return self.__class__.__name__
    ...
    >>> @extension(protocol_1)
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


class InheritException(Exception):

    '''Could not be inherited.'''

class InstantiationException(Exception):
    '''Protocols Could not be instantiated.'''


class ProtocolMeta(type):

    def __new__(cls, name, bases, dct):
        for base in bases:
            if isinstance(base, cls):
                raise InheritException('Could not be inherited from %s' % base)

        return super().__new__(cls, name, bases, dct)

    def __call__(self, *args, **kwargs):
        raise InstantiationException('Protocols Could not be instantiated.')