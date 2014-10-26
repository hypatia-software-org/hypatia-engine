"""Meta-class test"""

class Test(object):

    def __init__(self, test):
        test(self)


def debug(self):
    self.north = True


derp = Test(debug)
print derp.north
print type(derp)
