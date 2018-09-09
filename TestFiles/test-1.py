def order(n,base,x):
    """
    >>>a=lambda x:x+1
    >>>b=lambda x:x*2
    >>>c=lambda x:x
    >>>apply_n(2,)
    """
    def take(f):
        return order(n-1,lambda x:f(base(x)),x)
    if(n==0):
        return base(x)
    else:
        return take
a=lambda x:x+1
b=lambda x:x*2
c=lambda x:x+5
print(order(2,a,3)(c)(b))