#Write a generator function gen_all_items that takes a list of iterators and yields
#items from all of them in order.
def gen_all_items(lst):
    """
    >>> nums = [[1, 2], [3, 4], [[5, 6]]]
    >>> num_iters = [iter(l) for l in nums]
    >>> list(gen_all_items(num_iters))
    [1, 2, 3, 4, [5, 6]]
    """
    """
    for i in lst:
        yield from i
    """
    for it in lst:
        yield from it

class MyToys:
    name='old toy'
    def __init__(self, name=name):
        self.name=name
    def __add__(self, other_toy):
        assert(type(other_toy)==MyToys)
        return self.name+other_toy.name
    def __str__(self):
        return str(self.name)
    def __radd__(self, other_toy):
        return other_toy.name + self.name

class SuperToy(MyToys):
    super_genius="I'm a genius"
    def __add__(self, other_toy):
        return self.name + other_toy.name
    def __radd__(self, other_toy):
        return other_toy.name + self.name