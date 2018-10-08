""" Optional questions for Lab 05 """

from lab05 import *
#from lib import random
# Shakespeare and Dictionaries
def build_successors_table(tokens):
    """Return a dictionary: keys are words; values are lists of successors.

    >>> text = ['We', 'came', 'to', 'investigate', ',', 'catch', 'bad', 'guys', 'and', 'to', 'eat', 'pie', '.']
    >>> table = build_successors_table(text)
    >>> sorted(table)
    [',', '.', 'We', 'and', 'bad', 'came', 'catch', 'eat', 'guys', 'investigate', 'pie', 'to']
    >>> table['to']
    ['investigate', 'eat']
    >>> table['pie']
    ['.']
    >>> table['.']
    ['We']
    """
    table = {}
    prev = '.'
    for word in tokens:
        if prev not in table: #prev就是key
            "*** YOUR CODE HERE ***"
            #length=len(tokens)
            table[prev]=[]     
        flag=1
        for i in table[prev]:
          if(i==word):
            flag=0
            break       
        if(flag):
          table[prev].append(word)            
        "*** YOUR CODE HERE ***"
        prev = word
    return table

def construct_sent(word, table):
    """Prints a random sentence starting with word, sampling from
    table.

    >>> table = {'Wow': ['!'], 'Sentences': ['are'], 'are': ['cool'], 'cool': ['.']}
    >>> construct_sent('Wow', table)
    'Wow!'
    >>> construct_sent('Sentences', table)
    'Sentences are cool.'
    """
    import random
    result = ''
    while word not in ['.', '!', '?']:
        "*** YOUR CODE HERE ***"
        result=result+word+" "
        list_table=table[word]        
        ran = random.choice(list_table)
        word=ran        
    return result.strip() + word

def shakespeare_tokens(path='shakespeare.txt', url='http://composingprograms.com/shakespeare.txt'):
    """Return the words of Shakespeare's plays as a list."""
    import os
    from urllib.request import urlopen
    if os.path.exists(path):
        return open('shakespeare.txt', encoding='ascii').read().split()
    else:
        shakespeare = urlopen(url)
        return shakespeare.read().decode(encoding='ascii').split()

# Uncomment the following two lines
#tokens = shakespeare_tokens()
#table = build_successors_table(tokens)

def random_sent():
    import random
    return construct_sent(random.choice(table['.']), table)

# Q6
def sprout_leaves(t, vals):
    """Sprout new leaves containing the data in vals at each leaf in
    the original tree t and return the resulting tree.

    >>> t1 = tree(1, [tree(2), tree(3)])
    >>> print_tree(t1)
    1
      2
      3
    >>> new1 = sprout_leaves(t1, [4, 5])
    >>> print_tree(new1)
    1
      2
        4
        5
      3
        4
        5

    >>> t2 = tree(1, [tree(2, [tree(3)])])
    >>> print_tree(t2)
    1
      2
        3
    >>> new2 = sprout_leaves(t2, [6, 1, 2])
    >>> print_tree(new2)
    1
      2
        3
          6
          1
          2
    """
    "*** YOUR CODE HERE ***"
    #我的实现并不优美，直接删除再添加，但是确实没问题
    #因为每次都会删除和添加，导致顺序其实没变
    if(is_leaf(t)):        
        return tree(label(t),[tree(i,[]) for i in vals])
    else:
        new_tree=copy_tree(t)
        for i in branches(t):
            new_tree.remove(i)
            #branches(new_tree)[i]=sprout_leaves(branches(t)[i], vals)             
            i= sprout_leaves(i,vals)
            new_tree.append(i)
        return new_tree
# Q7
def add_trees(t1, t2):
    """
    >>> numbers = tree(1,
    ...                [tree(2,
    ...                      [tree(3),
    ...                       tree(4)]),
    ...                 tree(5,
    ...                      [tree(6,
    ...                            [tree(7)]),
    ...                       tree(8)])])
    >>> print_tree(add_trees(numbers, numbers))
    2
      4
        6
        8
      10
        12
          14
        16
    >>> print_tree(add_trees(tree(2), tree(3, [tree(4), tree(5)])))
    5
      4
      5
    >>> print_tree(add_trees(tree(2, [tree(3)]), tree(2, [tree(3), tree(4)])))
    4
      6
      4
    >>> print_tree(add_trees(tree(2, [tree(3, [tree(4), tree(5)])]), \
    tree(2, [tree(3, [tree(4)]), tree(5)])))
    4
      6
        8
        5
      5
    """
    "*** YOUR CODE HERE ***"
    branches_t1=branches(t1)
    branches_t2=branches(t2)
    length_t1=len(branches_t1)
    length_t2=len(branches_t2)
    label_sum=label(t1)+label(t2)
    #之前出现了一个问题，因为我每次remove掉一个子节点，再把修改后的加进来
    #因此当，new_tree是子节点较多的那个树时，会造成旧节点依旧在，子节点的顺序乱了
    #一旦删除一个节点，必须要紧接着加到队尾去，一个更好的办法应该是直接对应下标更改
    if(length_t1<length_t2):
      new_tree=copy_tree(t1)
    else:
      new_tree=copy_tree(t2)
    new_tree[0]=label_sum
    zipped_branches=zip(branches_t1,branches_t2)

    for i,j in zipped_branches:
      """这是可行的但是耗时O(N2)的方法
      new_tree.remove(i)
      new_branch=add_trees(i,j) 
      new_tree.append(new_branch)
      """
      #新的方法直接修改对应下标，应该是O(N)解决问题
      index=new_tree.index(i)
      new_tree[index]=add_trees(i,j)

    if(length_t1 > length_t2):
      for i in range(length_t2,length_t1):
        new_tree.append(branches_t1[i])      
    elif(length_t1 < length_t2):
      for i in range(length_t1,length_t2):
        new_tree.append(branches_t2[i])    

    return new_tree
#print_tree(add_trees(tree(2, [tree(3)]), tree(2, [tree(3), tree(4)])))    
print_tree(add_trees(tree(2, [tree(3, [tree(4), tree(5)])]),     tree(2, [tree(3, [tree(4)]), tree(5)])))
numbers = tree(1,
                [tree(2,
                      [tree(3),
                       tree(4)]),
                 tree(5,
                      [tree(6,
                            [tree(7)]),
                       tree(8)])])
print(add_trees(numbers,numbers))
