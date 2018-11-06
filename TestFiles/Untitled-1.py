class A():
    def __init__(self, name):
        self.name = name

class B(A):
    def __init__(self, name, power):
        A.__init__(self, name)
        self.power = power

a = A('yes')
b = B('no',33)
c = B(a,21)
print(a.name)
print(b.name)
print(c.name)