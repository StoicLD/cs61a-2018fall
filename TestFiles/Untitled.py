
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
        return list(x)
    else:
        for i in branches(t):
            path=find_path(i,x)
            if(path):       #找到了这条路
                return [label(i)]+path
t=tree(1,
    [tree(3,
        [tree(4),
         tree(5),
         tree(6)]),
        tree(2)])
tree_max(t)