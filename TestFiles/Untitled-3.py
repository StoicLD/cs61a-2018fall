def genger(n):
    init_c=[n[0]]
    whole=[]
    if(n[0]==1):
        yield init_c
    else:
        for i in n[1:]:
                yield init_c+genger(i)
next(genger([3, [ [2,[1]]   ] ,  [2, [1] ] ] ))