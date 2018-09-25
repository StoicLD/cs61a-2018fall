#逆转树形输出序列
def f_then_g(f,g,n):
    if(n):
        f(n)
        g(n)
grow=lambda n: f_then_g(grow,print,n//10)
down=lambda n: f_then_g(print,down,n//10)

def inverse(n):    
    grow(n)
    print(n)
    down(n)
inverse(12345)


