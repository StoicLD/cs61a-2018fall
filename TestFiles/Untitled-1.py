def f(x):
    x=4
    def g(y):
        def h(z):
            nonlocal x
            x=x+1
            return x+y+z
        return h
    return g

a=f(1)

def oski(bear):
    def cal(berk):
        nonlocal bear
        if(bear(berk)==0):
            return [berk+1,berk-1]
        bear=lambda key: berk-key
        return [berk,cal(berk)]
    return cal(2)
print(oski(abs))