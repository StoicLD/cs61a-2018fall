class C:
    def f(self):
        return 2
    def g(self):
        return 3
    def b(self, number):
        return number
    def c(self):
        return self.f()
    def s(self):
        return self.b(13)
class A:
    def f(self):
        return 2
    def g(self, obj, x):
        if x == 0:
            return A.f(obj)
        return obj.f() + self.g(self, x - 1)
class B(A):
    def f(self):
        return 4




