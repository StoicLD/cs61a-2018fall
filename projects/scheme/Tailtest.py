def test(x):
    return 1 + x
def Supertest(origin_test):
    def inner():
        x = 10 + origin_test(2)
        return x
    return inner

test = Supertest(test)

print(test())
