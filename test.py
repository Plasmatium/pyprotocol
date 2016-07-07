from protocol import protocol, joint


class CommonClass():

    def func(self):
        return self.args, self.kwargs


baseProtocol = protocol(CommonClass)


@protocol
@joint(baseProtocol)
class ptcA():

    def ptcA_fun(self):
        print('ptcA_fun')
        return self


@joint(ptcA)
class TargetClass():

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def funcx(self):
        return hash(str(self.func()))
