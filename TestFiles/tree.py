def branches(t):
    return t[1:]
def is_tree(tree_1):
    return not branches(tree_1)

def tree(label,branches=[]):
    #for branch in branches:
    #    assert is_tree(branch)
    return [label]+list(branches)

def label(tree):
    return tree[0]

def is_leaf(t):
    return not branches(t)

def tree_max(t):
    if(is_leaf(t)):
        return t[0]
    return max(label(t),max((tree_max(i) for i in t[1:])) )

def find_path(t,x):
    if(label(t)==x):
        return [x]
    else:
        for i in branches(t):
            path=find_path(i,x)
            if(path):       #找到了这条路
                return [label(t)]+path
        

def count_tree(t):
    if(is_leaf(t)):
        return 1
    else:
        sum=1
        for i in branches(t):
            sum+=count_tree(i)
        return sum

def print_fib_tree(t):
    print(label(t))
    if(not is_leaf(t)):        
        print_fib_tree(branches(t)[0])
    else:   
        return

def list_leaf(t):
    if(is_leaf(t)):
        return [label(t)]
    else:
        return [list_leaf(i) for i in branches(t)]

def all_increment(t,n):
    if(is_leaf(t)):
        return tree(label(t)+n,[])
    else:
        return tree( label(t)+n,  [all_increment(i,n) for i in branches(t) ] )
     

t=tree(1,
    [tree(3,
        [tree(4),
         tree(5),
         tree(6)]),
        tree(2)])
tree_max(t)

def fib_tree(n):
    assert(n>=0)
    if(n==0):
        return tree(1,[])
    elif(n==1):
        return tree(1,[])
    else:
        left,right=fib_tree(n-1),fib_tree(n-2)
        return tree(label(left)+label(right),[left,right])
print(list_leaf(t))
s=all_increment(t,10)
print(list_leaf(s))