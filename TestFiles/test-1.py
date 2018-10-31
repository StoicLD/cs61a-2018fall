class P:
        k = 1
        def __init__(self):
                self.k = P.k
                P.k += 1

class F(P):
        def call(self):
                print(self.k)
                s