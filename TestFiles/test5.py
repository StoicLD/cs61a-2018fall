class Link:
    empty = ()
    def __init__(self, first, rest=empty):
        assert rest is Link.empty or isinstance(rest, Link)
        self.first = first
        self.rest = rest
    @property
    def second(self):
        return self.rest.first
    @second.setter
    def second(self, value):
        self.rest.first = value
    def __repr__(self):
        if self.rest is not Link.empty:
            rest_repr = ', ' + repr(self.rest)
        else:
            rest_repr = ''
        return 'Link(' + repr(self.first) + rest_repr + ')'
    def __str__(self):
        string = '<'
        while self.rest is not Link.empty:
            string += str(self.first) + ' '
            self = self.rest
        return string + str(self.first) + '>'

class Tree:
    def __init__(self, label, branches=[]):
        for b in branches:
            assert isinstance(b, Tree)
        self.label = label
        self.branches = list(branches)
    def is_leaf(self):
        return not self.branches
    def map(self, fn):
        self.label = fn(self.label)
        for b in self.branches:
            b.map(fn)
    def __contains__(self, e):
        if self.label == e:
            return True
        for b in self.branches:
            if e in b:
                return True
        return False
    def __repr__(self):
        if self.branches:
            branch_str = ', ' + repr(self.branches)
        else:
            branch_str = ''
        return 'Tree({0}{1})'.format(self.label, branch_str)
    def __str__(self):
        def print_tree(t, indent=0):
            tree_str = '  ' * indent + str(t.label) + "\n"
            for b in t.branches:
                tree_str += print_tree(b, indent + 1)
            return tree_str
        return print_tree(self).rstrip()

def multiLink(list_of_links):
    product = 1
    for lnk in list_of_links:
        if(lnk is Link.empty ):
            return Link.empty
        product *= lnk.first
    list_of_rest_links = [link.rest for link in list_of_links]
    return Link(product, multiLink(list_of_rest_links))

def remove_dup(lnk):
    dup = [lnk.first]
    it = lnk.rest
    begin = lnk
    while(it is not Link.empty):
        if(it.first in dup):
            lnk.rest = it.rest 
            it = lnk.rest
        else:
            dup.append(it.first)
            lnk = lnk.rest  
            it = lnk.rest
    return begin

def red_tree(t, f):
    t.label = f(t.label)
    new_f = lambda y: f(f(y))
    for i in t.branches:
        red_tree(i, new_f)

class BTree(Tree):
    def __init__(self,label, left = [], right = []):
        Tree.__init__(label, [left, right])
        self.left = left
        self.right = right

def ss(s, re):
    if(s is not Link.empty):
        for i in range(re):
            s.rest = Link(s.first, s.rest)
            s = s.rest
        ss(s.rest, re+1)

def pile(t):
    assert(type(t) == Tree)
    p = {}
    def gather(u, path):
        if(u.is_leaf()):
            return {u.label: path}
        else:
            for b in u.branches:
                nonlocal p
                p = gather(b, (u.label, path))
    gather(t, ())
    return p
t = Tree(5, [Tree(3, [Tree(1), Tree(2)]), Tree(6, [Tree(7)]) ])
print(t)
print(pile(t))