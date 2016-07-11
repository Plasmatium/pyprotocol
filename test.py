from protocol import protocol, joint


class CommonClass():

    def func(self):
        return self.args, self.kwargs


baseProtocol = protocol(CommonClass)


@protocol
@joint(baseProtocol)
class ptcA():
    def ptcf(self):
        print('ptcA')

    def ptcA_fun(self):
        print('ptcA_fun')
        return self


@protocol
class ptcX1():
    def ptcf(self):
        print('ptcX1')


@protocol
class ptcX2():
    def ptcf(self):
        print('ptcX2')

    def __init__(self, arg):
        super(ptcX2, self).__init__()
        self.arg = arg


@protocol
class ptcX3():
    def ptcf(self):
        print('ptcX3')

    def __init__(self, arg):
        super(ptcX2, self).__init__()
        self.arg = arg


@joint(ptcA, ptcX1, ptcX2, ptcA, ptcX3)
# There would be no duplicated protocols, because duplicated protocols
# would be applied multiple times with the same effect, and __protocols__
# is a set() without duplicated items
class MidClass():
    x = 0

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    # This func is MidClass.func, not CommonClass.func, because this func
    # is MidClass its own. Class's own function would not be
    # overrided by jointed function.
    def func(self):
        MidClass.x += 1
        print(MidClass.x)
        return hash(str(self.func()))

@joint(protocol(MidClass), ptcX1)
class TargetClass(CommonClass):
    # CommonClass has func, MidClass has func. 'func' in TargetClass is 
    # CommonClass.func because TargetClass inherited from CommonClass, 
    # just like it has its own func (which inherited from CommonClass)
    # so the situation like MidClass, class's own function would not be
    # overrided by jointed function.
    def target(self):
        return hash(self)