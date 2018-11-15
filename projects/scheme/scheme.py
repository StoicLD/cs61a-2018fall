"""A Scheme interpreter and its read-eval-print loop."""

from scheme_builtins import *
from scheme_reader import *
from ucb import main, trace

##############
# Eval/Apply #
##############
#根据给的环境env和expression（表现为Pair的形式）计算结果
def scheme_eval(expr, env, _=None): # Optional third argument is ignored
    """Evaluate Scheme expression EXPR in environment ENV.
    
    >>> expr = read_line('(+ 2 2)')
    >>> expr
    Pair('+', Pair(2, Pair(2, nil)))
    >>> scheme_eval(expr, create_global_frame())
    4
    """
    # Evaluate atoms
    #这里判断如1,3 这种常数或者x，y符号，或者nil等原子性操作
    if scheme_symbolp(expr):
        return env.lookup(expr)
    elif self_evaluating(expr):
        return expr

    # All non-atomic expressions are lists (combinations)
    #python的Pair就是scheme的list
    if not scheme_listp(expr):
        raise SchemeError('malformed list: {0}'.format(repl_str(expr)))
    first, rest = expr.first, expr.second
    if scheme_symbolp(first) and first in SPECIAL_FORMS:
        return SPECIAL_FORMS[first](rest, env)
    else:
        # BEGIN PROBLEM 5
        "*** YOUR CODE HERE ***"
        #expr是Pair的形式
        scheme_operator = scheme_eval(first, env)
        check_procedure(scheme_operator)
        #如果是macro，不计算直接apply
        if(isinstance(scheme_operator, MacroProcedure)):
            return scheme_eval(scheme_operator.apply_macro(rest, env), env)

        #关于我的疑惑，(+ 1 (+ 2 3) 4)这个形式出去operator'+'只有三个元素其中(+ 2 3)是单独的一个
        #Pair,所以不会出现我想的rest重叠的情况
        #rest = Pair(1, Pair(Pair('+', Pair(2, Pair(3, nil))), Pair(4, nil)))
        eval_lambda = lambda x: scheme_eval(x, env)

        rest = rest.map(eval_lambda)

        return scheme_apply(scheme_operator, rest, env)
        # END PROBLEM 5


def self_evaluating(expr):
    """Return whether EXPR evaluates to itself."""
    return (scheme_atomp(expr) and not scheme_symbolp(expr)) or expr is None

def scheme_apply(procedure, args, env):
    """Apply Scheme PROCEDURE to argument values ARGS (a Scheme list) in
    environment ENV."""
    check_procedure(procedure)
    if isinstance(procedure, BuiltinProcedure):
        return procedure.apply(args, env)
    else:
    #不是builtin的需要继续eval全部的
        new_env = procedure.make_call_frame(args, env)
        return eval_all(procedure.body, new_env)

def eval_all(expressions, env):
    """Evaluate each expression im the Scheme list EXPRESSIONS in
    environment ENV and return the value of the last."""
    # BEGIN PROBLEM 8
    #这里我又给自己挖了一个坑。。。应该要返回的是scheme中代表的空值nil
    #但是eval_all(nil, env) # return None (meaning undefined)要返回None
    #而不是nil
    #因此当第一个是nil的时候直接返回None，而如果是一个Pair(nil, nil)这样的形式
    #还是会返回nil的
    if(expressions == nil):
        return None
    current_value = nil
    #当second时nil的时候，标志着结束，但是还是要计算第一个
    while(expressions.second != nil):
        #print(expressions.second)
        #我的担忧是对此一举，在Q5中每个sub-expression都是Pair中的第一个元素而且是一个Pair类型
        current_value = scheme_eval(expressions.first, env)
        expressions = expressions.second

    #最后一个应该是处于tail context里面的,这里顺带着处理了lambda的body最后一个
    #式子，就是tail context
    return scheme_eval(expressions.first, env, True)
    # END PROBLEM 8

################
# Environments #
################

class Frame:
    """An environment frame binds Scheme symbols to Scheme values."""

    def __init__(self, parent):
        """An empty frame with parent frame PARENT (which may be None)."""
        self.bindings = {}
        self.parent = parent

    def __repr__(self):
        if self.parent is None:
            return '<Global Frame>'
        s = sorted(['{0}: {1}'.format(k, v) for k, v in self.bindings.items()])
        return '<{{{0}}} -> {1}>'.format(', '.join(s), repr(self.parent))

    def define(self, symbol, value):
        """Define Scheme SYMBOL to have VALUE."""
        # BEGIN PROBLEM 3
        "*** YOUR CODE HERE ***"
        self.bindings[symbol] = value
        
        # END PROBLEM 3

    def lookup(self, symbol):
        """Return the value bound to SYMBOL. Errors if SYMBOL is not found."""
        # BEGIN PROBLEM 3
        "*** YOUR CODE HERE ***"
        current_frame = self
        while(current_frame):
            obj_value = current_frame.bindings.get(symbol)
            #找不到对应的值返回的就是None，没有问题
            #但是
            if(obj_value != None):
                return obj_value
            current_frame = current_frame.parent        
        # END PROBLEM 3
        raise SchemeError('unknown identifier: {0}'.format(symbol))


    def make_child_frame(self, formals, vals):
        """Return a new local frame whose parent is SELF, in which the symbols
        in a Scheme list of formal parameters FORMALS are bound to the Scheme
        values in the Scheme list VALS. Raise an error if too many or too few
        vals are given.

        >>> env = create_global_frame()
        >>> formals, expressions = read_line('(a b c)'), read_line('(1 2 3)')
        >>> env.make_child_frame(formals, expressions)
        <{a: 1, b: 2, c: 3} -> <Global Frame>>
        """
        # BEGIN PROBLEM 11
        "*** YOUR CODE HERE ***"
        if(len(formals) != len(vals)):
            raise SchemeError('the number of parameters are not the same as values!')
        check_formals(formals)
        #check_formals(vals)
        child_frame = Frame(self)

        while(formals != nil and vals != nil):
            para = formals.first
            val = vals.first
            child_frame.bindings[para] = val
            formals = formals.second
            vals = vals.second
        return child_frame
        # END PROBLEM 11

##############
# Procedures #
##############

class Procedure:
    """The supertype of all Scheme procedures."""

def scheme_procedurep(x):
    return isinstance(x, Procedure)

#将一个已有函数覆给一个新的变量
class BuiltinProcedure(Procedure):
    """A Scheme procedure defined as a Python function."""

    def __init__(self, fn, use_env=False, name='builtin'):
        self.name = name
        self.fn = fn
        self.use_env = use_env

    def __str__(self):
        return '#[{0}]'.format(self.name)

    def apply(self, args, env):
        """Apply SELF to ARGS in ENV, where ARGS is a Scheme list.

        >>> env = create_global_frame()
        >>> plus = env.bindings['+']
        >>> twos = Pair(2, Pair(2, nil))
        >>> plus.apply(twos, env)
        4
        """
        if not scheme_listp(args):
            raise SchemeError('arguments are not in a list: {0}'.format(args))
        # Convert a Scheme list to a Python list
        python_args = []
        while args is not nil:
            python_args.append(args.first)
            args = args.second
        # BEGIN PROBLEM 4
        "*** YOUR CODE HERE ***"
        if self.use_env:
            python_args.append(env)
        try:
            # extra print
            # print("自身的函数是:",self.fn)
            # print("自身的参数是",python_args)

            result = self.fn(*python_args)

            # print("result 是：",result)
            return result
        except TypeError as e:
            raise SchemeError('argument error!: {0}'.format(args))
        # END PROBLEM 4

class LambdaProcedure(Procedure):
    """A procedure defined by a lambda expression or a define form."""

    def __init__(self, formals, body, env):
        """A procedure with formal parameter list FORMALS (a Scheme list),
        whose body is the Scheme list BODY, and whose parent environment
        starts with Frame ENV."""
        self.formals = formals
        self.body = body
        self.env = env

    def make_call_frame(self, args, env):
        """Make a frame that binds my formal parameters to ARGS, a Scheme list
        of values, for a lexically-scoped call evaluated in environment ENV."""
        # BEGIN PROBLEM 12
        "*** YOUR CODE HERE ***"
        #(define (out x y) (define (in x z) (+ x z y)) (in x y))
        #这里需要注意，new_frame的parent是self.env而不是env
        new_frame = self.env.make_child_frame(self.formals, args)
        return new_frame
        # END PROBLEM 12

    def __str__(self):
        return str(Pair('lambda', Pair(self.formals, self.body)))

    def __repr__(self):
        return 'LambdaProcedure({0}, {1}, {2})'.format(
            repr(self.formals), repr(self.body), repr(self.env))

class MacroProcedure(LambdaProcedure):
    """A macro: a special form that operates on its unevaluated operands to
    create an expression that is evaluated in place of a call."""

    def apply_macro(self, operands, env):
        """Apply this macro to the operand expressions."""
        return complete_apply(self, operands, env)

def add_builtins(frame, funcs_and_names):
    """Enter bindings in FUNCS_AND_NAMES into FRAME, an environment frame,
    as built-in procedures. Each item in FUNCS_AND_NAMES has the form
    (NAME, PYTHON-FUNCTION, INTERNAL-NAME)."""
    for name, fn, proc_name in funcs_and_names:
        frame.define(name, BuiltinProcedure(fn, name=proc_name))

#################
# Special Forms #
#################

# Each of the following do_xxx_form functions takes the cdr of a special form as
# its first argument---a Scheme list representing a special form without the
# initial identifying symbol (if, lambda, quote, ...). Its second argument is
# the environment in which the form is to be evaluated.

#(define x 3) (define y (+ 1 2))
def do_define_form(expressions, env):
    """Evaluate a define form."""
    check_form(expressions, 2)
    target = expressions.first
    #(define x 3) 这种单一强开
    if scheme_symbolp(target):
        check_form(expressions, 2, 2)
        # BEGIN PROBLEM 6
        "*** YOUR CODE HERE ***"
        # print(expressions)
        # print('分割线')
        # print(expressions.second)
        # print('分割线')
        # print(scheme_eval(expressions.second.first, env))
        #错误在于，如果直接将expression.second传入,传入的是Pair(1, nil)
        #相当于(1),然而1不是callable的，因此报错，如果是一个(define x (+ 1 2))这样的形式
        #还是和第五问一样，因为expression.second.first 是 Pair('+', Pair(1, Pair(2, nil)))
        #是一个pair所以不会有问题

        env.define(target, scheme_eval(expressions.second.first, env))
        return target
        # END PROBLEM 6
    #(define (f x y) (+ x y)) 这种要转换为lambda函数的情况
    elif isinstance(target, Pair) and scheme_symbolp(target.first):
        # BEGIN PROBLEM 10
        "*** YOUR CODE HERE ***"
        # 在这个式子中target就是(f x y) (define (f x y) (+ x y))
        func_symbol = target.first
        formals = target.second
        body = expressions.second
        #不知道check_formals 有没有判断是不是nil的情况，先用了再说
        #更新，确实nil不是string类型，check的时候会报错没问题
        check_formals(formals)
        env.define(func_symbol, do_lambda_form(Pair(formals, body), env))
        return func_symbol
        # END PROBLEM 10
    else:
        bad_target = target.first if isinstance(target, Pair) else target
        raise SchemeError('non-symbol: {0}'.format(bad_target))

def do_quote_form(expressions, env):
    """Evaluate a quote form."""
    #根据测试例子，出去'quote'符号之后，后面跟的参数只有一个，所以要么就是一整个Pair
    check_form(expressions, 1, 1)
    # BEGIN PROBLEM 7
    "*** YOUR CODE HERE ***"
    # if(isinstance(expressions.first, Pair)):
    #     return Pair('quote', do_quote_form(expressions.first, env))
    # else:
    return expressions.first
    # END PROBLEM 7

def do_begin_form(expressions, env):
    """Evaluate a begin form."""
    check_form(expressions, 1)
    return eval_all(expressions, env)

def do_lambda_form(expressions, env):
    """Evaluate a lambda form."""
    check_form(expressions, 2)
    formals = expressions.first
    check_formals(formals)
    # BEGIN PROBLEM 9
    "*** YOUR CODE HERE ***"
    body = expressions.second
    check_form(body, 1)
    return LambdaProcedure(formals, body, env)
    # END PROBLEM 9

#实验一，if的除了判定语句外的sub句子都是tail context
def do_if_form(expressions, env):
    """Evaluate an if form."""
    check_form(expressions, 2, 3)
    if scheme_truep(scheme_eval(expressions.first, env)):
        #这里我加入了True
        return scheme_eval(expressions.second.first, env, True)
    elif len(expressions) == 3:
        # 这里我加入了True
        return scheme_eval(expressions.second.second.first, env, True)

def do_and_form(expressions, env):
    """Evaluate a (short-circuited) and form."""
    # BEGIN PROBLEM 13
    "*** YOUR CODE HERE ***"
    # value = True
    # while(expressions != nil):
    #     value = scheme_eval(expressions.first, env)
    #     #python中0与False等价！！！
    #     if(value == False and isinstance(value, bool)):
    #         break
    #     expressions = expressions.second
    # return value
    # (and) 直接返回True
    if expressions == nil:
        return True
    #last one,最后一个需要加入tail = True
    elif expressions.second is nil:
        return scheme_eval(expressions.first,env, True)
    else:
        while expressions.second is not nil:
            # if scheme_falsep(scheme_eval(expressions.first, env)):
            if scheme_eval(expressions.first,env) is False:
                return False
            expressions = expressions.second
        return scheme_eval(expressions.first,env, True)
    # END PROBLEM 13

def do_or_form(expressions, env):
    """Evaluate a (short-circuited) or form."""
    # BEGIN PROBLEM 13
    "*** YOUR CODE HERE ***"
    # value = False
    # while(expressions != nil):
    #     value = scheme_eval(expressions.first, env)
    #     #python中0与False等价！！！
    #     if(not isinstance(value, bool) or value == True):
    #         break
    #     expressions = expressions.second
    # return value
    if expressions is nil:
        return False
    elif expressions.second is nil:  # 尾递归的情形
        return scheme_eval(expressions.first, env, True)
    else:
        first_expr = scheme_eval(expressions.first, env)
        if first_expr is False:  # The first expression is False
            return do_or_form(expressions.second, env)
        else:  # The first expression is True
            return first_expr
    # END PROBLEM 13

def do_cond_form(expressions, env):
    """Evaluate a cond form."""
    while expressions is not nil:
        clause = expressions.first
        check_form(clause, 1)
        if clause.first == 'else':
            test = True
            if expressions.second != nil:
                raise SchemeError('else must be last')
        else:
            test = scheme_eval(clause.first, env)
        if scheme_truep(test):
            # BEGIN PROBLEM 14
            "*** YOUR CODE HERE ***"
            #问题出在这里！！！！！
            #之前(cond (True nil)) 这种情况下回返回True，而不是nil导致后面出错！！1
            # result = eval_all(clause.second, env)
            # if(not result):
            #     return test
            # return result
            if clause.second is nil:  # When the true predicate does not have a corresponding result sub-expression, return the predicate value
                return test
            return eval_all(clause.second, env)

            # END PROBLEM 14
        expressions = expressions.second

def do_let_form(expressions, env):
    """Evaluate a let form."""
    check_form(expressions, 2)
    let_env = make_let_frame(expressions.first, env)
    return eval_all(expressions.second, let_env)

def make_let_frame(bindings, env):
    """Create a child frame of ENV that contains the definitions given in
    BINDINGS. The Scheme list BINDINGS must have the form of a proper bindings
    list in a let expression: each item must be a list containing a symbol
    and a Scheme expression."""
    if not scheme_listp(bindings):
        raise SchemeError('bad bindings list in let form')
    # BEGIN PROBLEM 15
    "*** YOUR CODE HERE ***"
    #Pair(Pair(x, Pair(3, nil)), Pair(Pair(y, Pair(4)), nil))
    # it = bindings
    # while(it != nil):
    #     check_form(it.first, 2, 2)
    #     it = it.second

    # formals = bindings.map(lambda x: x.first)
    # vals = bindings.map(lambda x: x.second)

    # check_formals(formals)
    # eval (x (+1 2)) 这些bindling中带有expression的
    # eval_with_env = lambda x: scheme_eval(x, env)
    # vals = vals.map(eval_with_env)
    # child_frame = env.make_child_frame(formals, vals)
    # return child_frame

    #Pair(Pair(x, Pair(3, nil)), Pair(Pair(y, Pair(4)), nil))
    formals = nil
    vals = nil
    #逆转序列
    while (bindings !=nil):
        key_value = bindings.first
        check_form(key_value, 2, 2)
        #逆转构造序列
        formals = Pair(key_value.first, formals)
        #需要求值，针对 (let ((x (+ 2 3)) (y (* 2 4))  (+ x y) )) 这样的情况
        vals = Pair(scheme_eval(key_value.second.first, env), vals)
        bindings = bindings.second

    check_formals(formals)
    return env.make_child_frame(formals, vals)

    # END PROBLEM 15

def do_define_macro(expressions, env):
    """Evaluate a define-macro form."""
    # BEGIN Problem 21
    "*** YOUR CODE HERE ***"
    check_form(expressions, 2, 2)
    target = expressions.first
    check_form(target, 1)

    macro_symbol = target.first
    if(not scheme_symbolp(macro_symbol)):
        raise SchemeError('{0} need to be a symbol!'.format(macro_symbol))
    formals = target.second
    check_formals(formals)
    body = expressions.second
    env.define(macro_symbol, MacroProcedure(formals, body, env))

    return macro_symbol
    # END Problem 21


def do_quasiquote_form(expressions, env):
    """Evaluate a quasiquote form with parameters EXPRESSIONS in
    environment ENV."""
    def quasiquote_item(val, env, level):
        """Evaluate Scheme expression VAL that is nested at depth LEVEL in
        a quasiquote form in environment ENV."""
        if not scheme_pairp(val):
            return val
        if val.first == 'unquote':
            level -= 1
            if level == 0:
                expressions = val.second
                check_form(expressions, 1, 1)
                return scheme_eval(expressions.first, env)
        elif val.first == 'quasiquote':
            level += 1
        first = quasiquote_item(val.first, env, level)
        second = quasiquote_item(val.second, env, level)
        return Pair(first, second)

    check_form(expressions, 1, 1)
    return quasiquote_item(expressions.first, env, 1)

def do_unquote(expressions, env):
    raise SchemeError('unquote outside of quasiquote')


SPECIAL_FORMS = {
    'and': do_and_form,
    'begin': do_begin_form,
    'cond': do_cond_form,
    'define': do_define_form,
    'if': do_if_form,
    'lambda': do_lambda_form,
    'let': do_let_form,
    'or': do_or_form,
    'quote': do_quote_form,
    'define-macro': do_define_macro,
    'quasiquote': do_quasiquote_form,
    'unquote': do_unquote,
}

# Utility methods for checking the structure of Scheme programs

def check_form(expr, min, max=float('inf')):
    """Check EXPR is a proper list whose length is at least MIN and no more
    than MAX (default: no maximum). Raises a SchemeError if this is not the
    case.

    >>> check_form(read_line('(a b)'), 2)
    """
    if not scheme_listp(expr):
        raise SchemeError('badly formed expression: ' + repl_str(expr))
    length = len(expr)
    if length < min:
        raise SchemeError('too few operands in form')
    elif length > max:
        raise SchemeError('too many operands in form')

def check_formals(formals):
    """Check that FORMALS is a valid parameter list, a Scheme list of symbols
    in which each symbol is distinct. Raise a SchemeError if the list of
    formals is not a well-formed list of symbols or if any symbol is repeated.

    >>> check_formals(read_line('(a b c)'))
    """
    symbols = set()
    def check_and_add(symbol):
        if not scheme_symbolp(symbol):
            raise SchemeError('non-symbol: {0}'.format(symbol))
        if symbol in symbols:
            raise SchemeError('duplicate symbol: {0}'.format(symbol))
        symbols.add(symbol)

    while isinstance(formals, Pair):
        check_and_add(formals.first)
        formals = formals.second

    if formals != nil:
        check_and_add(formals)

def check_procedure(procedure):
    """Check that PROCEDURE is a valid Scheme procedure."""
    if not scheme_procedurep(procedure):
        raise SchemeError('{0} is not callable: {1}'.format(
            type(procedure).__name__.lower(), repl_str(procedure)))

#################
# Dynamic Scope #
#################

class MuProcedure(Procedure):
    """A procedure defined by a mu expression, which has dynamic scope.
     _________________
    < Scheme is cool! >
     -----------------
            \   ^__^
             \  (oo)\_______
                (__)\       )\/\
                    ||----w |
                    ||     ||
    """

    def __init__(self, formals, body):
        """A procedure with formal parameter list FORMALS (a Scheme list) and
        Scheme list BODY as its definition."""
        self.formals = formals
        self.body = body

    # BEGIN PROBLEM 16
    "*** YOUR CODE HERE ***"
    def make_call_frame(self, args, env):
        #(define (out x y) (define (in x z) (+ x z y)) (in x y))
        #这里需要注意，new_frame的parent是self.env而不是env
        new_frame = env.make_child_frame(self.formals, args)
        return new_frame

    # END PROBLEM 16

    def __str__(self):
        return str(Pair('mu', Pair(self.formals, self.body)))

    def __repr__(self):
        return 'MuProcedure({0}, {1})'.format(
            repr(self.formals), repr(self.body))

def do_mu_form(expressions, env):
    """Evaluate a mu form."""
    check_form(expressions, 2)
    formals = expressions.first
    check_formals(formals)
    # BEGIN PROBLEM 16
    "*** YOUR CODE HERE ***"
    body = expressions.second
    return MuProcedure(formals, body)
    # END PROBLEM 16

SPECIAL_FORMS['mu'] = do_mu_form

###########
# Streams #
###########

class Promise:
    """A promise."""
    def __init__(self, expression, env):
        self.expression = expression
        self.env = env

    def evaluate(self):
        if self.expression is not None:
            self.value = scheme_eval(self.expression, self.env.make_child_frame(nil, nil))
            self.expression = None
        return self.value

    def __str__(self):
        return '#[promise ({0}forced)]'.format(
                'not ' if self.expression is not None else '')

def do_delay_form(expressions, env):
    """Evaluates a delay form."""
    check_form(expressions, 1, 1)
    return Promise(expressions.first, env)

def do_cons_stream_form(expressions, env):
    """Evaluate a cons-stream form."""
    check_form(expressions, 2, 2)
    return Pair(scheme_eval(expressions.first, env),
                do_delay_form(expressions.second, env))

SPECIAL_FORMS['cons-stream'] = do_cons_stream_form
SPECIAL_FORMS['delay'] = do_delay_form

##################
# Tail Recursion #
##################

class Thunk:
    """An expression EXPR to be evaluated in environment ENV."""
    def __init__(self, expr, env):
        self.expr = expr
        self.env = env

def complete_apply(procedure, args, env):
    """Apply procedure to args in env; ensure the result is not a Thunk."""
    val = scheme_apply(procedure, args, env)
    if isinstance(val, Thunk):
        return scheme_eval(val.expr, val.env)
    else:
        return val

def optimize_tail_calls(original_scheme_eval):
    """Return a properly tail recursive version of an eval function."""
    def optimized_eval(expr, env, tail=False):
        """Evaluate Scheme expression EXPR in environment ENV. If TAIL,
        return a Thunk containing an expression for further evaluation.
        """
        #Thunk包含了当前的环境，因此不需要再次打开一个新的frame
        #这里是
        if tail and not scheme_symbolp(expr) and not self_evaluating(expr):
            #return eval_all(expr, env)
            #相当于一层一层的深入下去，直到到达一个tail时，注意此时的env和expr都被更新了，那么这次返回
            #将直接返回到最上层，也就是函数栈展开的其实位置，将这个包裹的Thunk返回，这样我们就得到了想要计算的环境
            #以及对应的变量，此时在最外层，env还是 global的，但是result.env是我们返回的结果，对于(sum 1001 0)
            #的第二层来说，result.env就变成了 n = 1000, total = 1001
            return Thunk(expr, env)

        result = Thunk(expr, env)
        # BEGIN
        "*** YOUR CODE HERE ***"
        while(isinstance(result, Thunk)):
            #expr, env = result.expr, result.env
            result = original_scheme_eval(result.expr, result.env)
            #tail = True
        return result
        # END
    return optimized_eval






################################################################
# Uncomment the following line to apply tail call optimization #
################################################################
scheme_eval = optimize_tail_calls(scheme_eval)






####################
# Extra Procedures #
####################

def scheme_map(fn, s, env):
    check_type(fn, scheme_procedurep, 0, 'map')
    check_type(s, scheme_listp, 1, 'map')
    return s.map(lambda x: complete_apply(fn, Pair(x, nil), env))

def scheme_filter(fn, s, env):
    check_type(fn, scheme_procedurep, 0, 'filter')
    check_type(s, scheme_listp, 1, 'filter')
    head, current = nil, nil
    while s is not nil:
        item, s = s.first, s.second
        if complete_apply(fn, Pair(item, nil), env):
            if head is nil:
                head = Pair(item, nil)
                current = head
            else:
                current.second = Pair(item, nil)
                current = current.second
    return head

def scheme_reduce(fn, s, env):
    check_type(fn, scheme_procedurep, 0, 'reduce')
    check_type(s, lambda x: x is not nil, 1, 'reduce')
    check_type(s, scheme_listp, 1, 'reduce')
    value, s = s.first, s.second
    while s is not nil:
        value = complete_apply(fn, scheme_list(value, s.first), env)
        s = s.second
    return value

################
# Input/Output #
################

def read_eval_print_loop(next_line, env, interactive=False, quiet=False,
                         startup=False, load_files=(), report_errors=False):
    """Read and evaluate input until an end of file or keyboard interrupt."""
    if startup:
        for filename in load_files:
            scheme_load(filename, True, env)
    while True:
        try:
            src = next_line()
            while src.more_on_line:
                expression = scheme_read(src)
                result = scheme_eval(expression, env)
                if not quiet and result is not None:
                    print(repl_str(result))
        except (SchemeError, SyntaxError, ValueError, RuntimeError) as err:
            if report_errors:
                if isinstance(err, SyntaxError):
                    err = SchemeError(err)
                    raise err
            if (isinstance(err, RuntimeError) and
                'maximum recursion depth exceeded' not in getattr(err, 'args')[0]):
                raise
            elif isinstance(err, RuntimeError):
                print('Error: maximum recursion depth exceeded')
            else:
                print('Error:', err)
        except KeyboardInterrupt:  # <Control>-C
            if not startup:
                raise
            print()
            print('KeyboardInterrupt')
            if not interactive:
                return
        except EOFError:  # <Control>-D, etc.
            print()
            return

def scheme_load(*args):
    """Load a Scheme source file. ARGS should be of the form (SYM, ENV) or
    (SYM, QUIET, ENV). The file named SYM is loaded into environment ENV,
    with verbosity determined by QUIET (default true)."""
    if not (2 <= len(args) <= 3):
        expressions = args[:-1]
        raise SchemeError('"load" given incorrect number of arguments: '
                          '{0}'.format(len(expressions)))
    sym = args[0]
    quiet = args[1] if len(args) > 2 else True
    env = args[-1]
    if (scheme_stringp(sym)):
        sym = eval(sym)
    check_type(sym, scheme_symbolp, 0, 'load')
    with scheme_open(sym) as infile:
        lines = infile.readlines()
    args = (lines, None) if quiet else (lines,)
    def next_line():
        return buffer_lines(*args)

    read_eval_print_loop(next_line, env, quiet=quiet, report_errors=True)

def scheme_open(filename):
    """If either FILENAME or FILENAME.scm is the name of a valid file,
    return a Python file opened to it. Otherwise, raise an error."""
    try:
        return open(filename)
    except IOError as exc:
        if filename.endswith('.scm'):
            raise SchemeError(str(exc))
    try:
        return open(filename + '.scm')
    except IOError as exc:
        raise SchemeError(str(exc))

def create_global_frame():
    """Initialize and return a single-frame environment with built-in names."""
    env = Frame(None)
    env.define('eval',
               BuiltinProcedure(scheme_eval, True, 'eval'))
    env.define('apply',
               BuiltinProcedure(complete_apply, True, 'apply'))
    env.define('load',
               BuiltinProcedure(scheme_load, True, 'load'))
    env.define('procedure?',
               BuiltinProcedure(scheme_procedurep, False, 'procedure?'))
    env.define('map',
               BuiltinProcedure(scheme_map, True, 'map'))
    env.define('filter',
               BuiltinProcedure(scheme_filter, True, 'filter'))
    env.define('reduce',
               BuiltinProcedure(scheme_reduce, True, 'reduce'))
    env.define('undefined', None)
    add_builtins(env, BUILTINS)
    return env

@main
def run(*argv):
    import argparse
    parser = argparse.ArgumentParser(description='CS 61A Scheme Interpreter')
    parser.add_argument('-load', '-i', action='store_true',
                       help='run file interactively')
    parser.add_argument('file', nargs='?',
                        type=argparse.FileType('r'), default=None,
                        help='Scheme file to run')
    args = parser.parse_args()

    next_line = buffer_input
    interactive = True
    load_files = []

    if args.file is not None:
        if args.load:
            load_files.append(getattr(args.file, 'name'))
        else:
            lines = args.file.readlines()
            def next_line():
                return buffer_lines(lines)
            interactive = False

    read_eval_print_loop(next_line, create_global_frame(), startup=True,
                         interactive=interactive, load_files=load_files)
    tscheme_exitonclick()