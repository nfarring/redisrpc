class Calculator(object):
    """A simple, mutable calculator used for testing."""

    def __init__(self):
        self.acc = 0.0

    def __str__(self):
        return '%s' % self.acc
    
    def clr(self):
        self.acc = 0.0

    def add(self,number):
        self.acc += number
        return self.acc

    def div(self,number):
        self.acc /= number
        return self.acc

    def mul(self,number):
        self.acc *= number
        return self.acc

    def sub(self,number):
        self.acc -= number
        return self.acc

    def val(self):
        return self.acc
