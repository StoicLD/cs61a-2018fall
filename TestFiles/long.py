
def long(lst):
    #从当前位置开始找递增序列
    def helper(lst):
        if(lst == None):
            return None
        elif(len(lst) == 1):
            return lst
        else:
            y = lst[0]
            t = []
            for i in range(len(lst)):
                if(y <= i):
                    t.append(i)
                    y = i       
            return t
    s = helper(lst)
    z =[]
    for i in range(len(lst)):
        z = []
        for j in range(i,len(lst[i:])):
            s = helper(lst[j:])
            if(lst[i] <= s[0]):
                s.insert(0,lst[i])
            if(len(s) > len(z)):
                z = s[:]
        
    return z
s = [7.1,7.2,8,9,5,1,4,6,7,8]
t = [1,3,1,4,5,2,6,7,9,1,11]
test = long(s)
print(test)