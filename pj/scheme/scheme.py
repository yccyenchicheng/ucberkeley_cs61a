"""A Scheme interpreter and its read-eval-print loop."""

from scheme_primitives import *
from scheme_reader import *
from ucb import main, trace

##############
# Eval/Apply #
##############

def scheme_eval(expr, env, _=None): # Optional third argument is ignored
    """Evaluate Scheme expression EXPR in environment ENV.

    >>> expr = read_line('(+ 2 2)')
    >>> expr
    Pair('+', Pair(2, Pair(2, nil)))
    >>> scheme_eval(expr, create_global_frame())
    4
    """
    # Evaluate atoms
    if scheme_symbolp(expr):
        return env.lookup(expr)
    elif self_evaluating(expr):
        return expr

    # All non-atomic expressions are lists (combinations)
    if not scheme_listp(expr):
        raise SchemeError('malformed list: {0}'.format(str(expr)))
    first, rest = expr.first, expr.second
    if scheme_symbolp(first) and first in SPECIAL_FORMS:
        return SPECIAL_FORMS[first](rest, env)
    else:
        # BEGIN PROBLEM 5

        # Check if the operator needs to be evaluated first
        # Then carry out the operand into eval_call
        if isinstance(first, Pair):
            operator = scheme_eval(first, env)
            check_procedure(operator)
            return operator.eval_call(rest, env)

        # If first is not in the env, raise SchemeError
        operator = env.lookup(first)

        # Lookup the operator and check the procedure
        operator = scheme_eval(first, env)
        check_procedure(operator)
        return operator.eval_call(rest, env)

        # END PROBLEM 5

def self_evaluating(expr):
    """Return whether EXPR evaluates to itself."""
    return scheme_atomp(expr) or scheme_stringp(expr) or expr is None

def scheme_apply(procedure, args, env):
    """Apply Scheme PROCEDURE to argument values ARGS (a Scheme list) in
    environment ENV."""
    check_procedure(procedure)

    return procedure.apply(args, env)

def eval_all(expressions, env):
    """Evaluate each expression im the Scheme list EXPRESSIONS in
    environment ENV and return the value of the last."""
    # BEGIN PROBLEM 8

    # If it's nil, return None
    if expressions == nil:
        return None

    # The last sub-expression in a begin statement is a tail context
    # And we are at the final expression, return it
    elif expressions.second == nil:
        result = scheme_eval(expressions.first, env, True)
        return result
    else:
        # Evaluate every sub-expressions
        scheme_eval(expressions.first, env)
        return eval_all(expressions.second, env)
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
        self.bindings[symbol] = value
        # END PROBLEM 3

    def lookup(self, symbol):
        """Return the value bound to SYMBOL. Errors if SYMBOL is not found."""
        # BEGIN PROBLEM 3

        # Lookup if the symbol is in the current env
        if symbol in self.bindings:
            return self.bindings[symbol]

        # Or lookup in the parent frame
        elif self.parent:
            return self.parent.lookup(symbol)

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
        child = Frame(self) # Create a new child with self as the parent
        # BEGIN PROBLEM 11
        
        # If the number of argements don't match, raise an error
        if len(formals) != len(vals):
            raise SchemeError('number of argument values does not match with the number of formal parameters')
        else:
            # iterate through the pair and bind them in the child frame
            while formals != nil:
                formal, val = formals.first, vals.first
                child.define(formal, val)
                formals, vals = formals.second, vals.second
        # END PROBLEM 11
        return child

##############
# Procedures #
##############

class Procedure:
    """The supertype of all Scheme procedures."""
    def eval_call(self, operands, env):
        """Standard function-call evaluation on SELF with OPERANDS as the
        unevaluated actual-parameter expressions and ENV as the environment
        in which the operands are to be evaluated."""
        # BEGIN PROBLEM 5

        # Create a helper function that enable us to 
        # pass in 2 paramters for the map method in the Pair class
        def helper_map(expr):
            return scheme_eval(expr, env)

        # If operands is nil, we split into cases
        if operands == nil:

            # Handle Procedure with 0 operand
            if isinstance(self, UserDefinedProcedure):
                return scheme_eval(self.body.first, env)
            # If '+', return 0
            if self.name == '+':
                return 0
            # If '*', return 1
            elif self.name == '*':
                return 1
            # Raise a SchemeError
            else:
                raise SchemeError('invalid input')

        args = Pair.map(operands, helper_map)

        return self.apply(args, env)
        # END PROBLEM 5

def scheme_procedurep(x):
    return isinstance(x, Procedure)

class PrimitiveProcedure(Procedure):
    """A Scheme procedure defined as a Python function."""

    def __init__(self, fn, use_env=False, name='primitive'):
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

        # If true then add the env into the python list
        if self.use_env:
            python_args.append(env)

        # Call fn on all of those arguments    
        try:
            return self.fn(*python_args)

        # If TypeError is raised, raise an SchemeError
        except TypeError:
            raise SchemeError('Wrong number of parameters')

        # END PROBLEM 4

class UserDefinedProcedure(Procedure):
    """A procedure defined by an expression."""

    def apply(self, args, env):
        """Apply SELF to argument values ARGS in environment ENV. Applying a
        user-defined procedure evaluates all expressions in the body."""
        new_env = self.make_call_frame(args, env)
        return eval_all(self.body, new_env)
        
class LambdaProcedure(UserDefinedProcedure):
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

        defined_env = self.env
        # make a call frame that binds formals to args
        call_frame = defined_env.make_child_frame(self.formals, args)
        call_frame.parent = defined_env

        return call_frame
        # END PROBLEM 12

    def __str__(self):
        return str(Pair('lambda', Pair(self.formals, self.body)))

    def __repr__(self):
        return 'LambdaProcedure({0}, {1}, {2})'.format(
            repr(self.formals), repr(self.body), repr(self.env))

class MacroProcedure(LambdaProcedure):
    """A macro: a special form that operates on its unevaluated operands to
    create an expression that is evaluated in place of a call."""

    def eval_call(self, operands, env):
        """Macro call evalution on me with OPERANDS as the unevaluated
        actual-parameter expressions and ENV as the environment in which the
        resulting expanded expression is to be evaluated."""
        # BEGIN Problem 22

        # Create a helper function that enable us to 
        # pass in 2 paramters for the map method in the Pair class
        def helper_map(expr):
            return scheme_eval(expr, env)



        # If operands is nil, we split into cases
        if operands == nil:

            # Handle Procedure with 0 operand
            if isinstance(self, UserDefinedProcedure):
                return scheme_eval(self.body.first, env)
            # If '+', return 0
            if self.name == '+':
                return 0
            # If '*', return 1
            elif self.name == '*':
                return 1
            # Raise a SchemeError
            else:
                raise SchemeError('invalid input')

        args = Pair.map(operands, helper_map) 
        return self.apply(args, env)
        # END Problem 22

def add_primitives(frame, funcs_and_names):
    """Enter bindings in FUNCS_AND_NAMES into FRAME, an environment frame,
    as primitive procedures. Each item in FUNCS_AND_NAMES has the form
    (NAME, PYTHON-FUNCTION, INTERNAL-NAME)."""
    for name, fn, proc_name in funcs_and_names:
        frame.define(name, PrimitiveProcedure(fn, name=proc_name))

#################
# Special Forms #
#################

# Each of the following do_xxx_form functions takes the cdr of a special form as
# its first argument---a Scheme list representing a special form without the
# initial identifying symbol (if, lambda, quote, ...). Its second argument is
# the environment in which the form is to be evaluated.

def do_define_form(expressions, env):
    """Evaluate a define form."""
    check_form(expressions, 2)
    target = expressions.first
    if scheme_symbolp(target):
        check_form(expressions, 2, 2)
        # BEGIN PROBLEM 6
        
        # Binding expressions to the target
        # If the expressions is a Pair, then we evaluate it first
        # Else we bind that value to that symbol
        if isinstance(expressions.second, Pair) == False:
            value = expressions.second.first
            env.define(target, value)
            return target
        else:    
            value = scheme_eval(expressions.second.first, env)
            env.define(target, value)
            return target

        # END PROBLEM 6
    elif isinstance(target, Pair) and scheme_symbolp(target.first):
        # BEGIN PROBLEM 10
        
        # Extract the formals
        formals = target.second

        # Pair the formals with body, which is expressions.second
        expressions = Pair(formals, expressions.second)

        # Bind target.first to Lambda
        symbol, value = target.first, do_lambda_form(expressions, env)
        env.define(symbol, value)
        return symbol
        # END PROBLEM 10
    else:
        bad_target = target.first if isinstance(target, Pair) else target
        raise SchemeError('non-symbol: {0}'.format(bad_target))

def do_quote_form(expressions, env):
    """Evaluate a quote form."""
    check_form(expressions, 1, 1)
    # BEGIN PROBLEM 7
    # Just return the operands
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

    # create a LambdaProcedure with formals, body and environment
    body = expressions.second

    return LambdaProcedure(formals, body, env)
    # END PROBLEM 9

def do_if_form(expressions, env):
    """Evaluate an if form."""
    check_form(expressions, 2, 3)

    # The 2nd and 3rd sub-expression in an if statement is a tail context
    if scheme_truep(scheme_eval(expressions.first, env)):
        return scheme_eval(expressions.second.first, env, True)
    elif len(expressions) == 3:
        return scheme_eval(expressions.second.second.first, env, True)

def do_and_form(expressions, env):
    """Evaluate a (short-circuited) and form."""
    # BEGIN PROBLEM 13
    all_false = [False, 'false', '#f']
    if expressions == nil:
        return True

    # The last sub-expression in and is a tail context
    if expressions.second == nil:
        curr_val = scheme_eval(expressions.first, env, True)
        return curr_val
    else:
        curr_val = scheme_eval(expressions.first, env)
        # Immediately return a value if we evaluate a false value
        if curr_val in all_false and str(curr_val) != '0':
            return curr_val
        else:
            return do_and_form(expressions.second, env)
    # END PROBLEM 13

def do_or_form(expressions, env):
    """Evaluate a (short-circuited) or form."""
    # BEGIN PROBLEM 13
    all_false = [False, 'false', '#f']
    if expressions == nil:
        return False

    # The last sub-expression in and is a tail context
    if expressions.second == nil:
        curr_val = scheme_eval(expressions.first, env, True)
        return curr_val
    else:
        # Immediately return a value if we evaluate a true value
        curr_val = scheme_eval(expressions.first, env)
        if curr_val not in all_false or str(curr_val) == '0':
            return curr_val
        else:
            return do_or_form(expressions.second, env)

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
            if clause.second == nil:
                return test
            else:
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

    # Use check_binding to check the structure of each binding
    check_binding = bindings

    # Flag of first Pair of formals
    first = True 
    while check_binding != nil:
        curr_binding = check_binding.first
        check_form(curr_binding, 2, 2)

        # Put the formals into a Pair
        # Evaluate the value and put them into a Pair
        if first:
            first = False
            formals = Pair(curr_binding.first, nil)
            values = Pair(scheme_eval(curr_binding.second.first, env), nil)

            # Traversed down the pairs
            check_binding = check_binding.second
            curr_formals, curr_values = formals, values

        else:
            curr_formals.second = Pair(curr_binding.first, nil)
            curr_values.second = Pair(scheme_eval(curr_binding.second.first, env), nil)

            check_binding = check_binding.second
            curr_formals, curr_values = curr_formals.second, curr_values.second

    check_formals(formals)

    let_frame = env.make_child_frame(formals, values)
    let_frame.parent = env

    return let_frame
    # END PROBLEM 15

def do_define_macro(expressions, env):
    """Evaluate a define-macro form."""
    # BEGIN Problem 22
    check_form(expressions, 2)
    target = expressions.first
    if scheme_symbolp(target):
        check_form(expressions, 2, 2)
        
        # Binding expressions to the target
        # If the expressions is a Pair, then we evaluate it first
        # Else we bind that value to that symbol
        if isinstance(expressions.second, Pair) == False:
            value = expressions.second.first
            env.define(target, value)
            return target
        else:    
            value = scheme_eval(expressions.second.first, env)
            env.define(target, value)
            return target


    elif isinstance(target, Pair) and scheme_symbolp(target.first):
        
        # Extract the formals
        formals = target.second

        # Pair the formals with body, which is expressions.second
        expressions = Pair(formals, expressions.second)

        # Bind target.first to Lambda
        symbol, value = target.first, do_lambda_form(expressions, env)
        env.define(symbol, value)
        return symbol
    # END Problem 22

def scheme_call_cc(function, env):
    class ContinuationError(Exception):
        """Represents a custom error that can be thrown and caught without
        being confused without other errors. Note: this class is defined inside
        the scheme_call_cc function so a different one is defined for each call
        to call/cc (so they don't interfere with each other).
        """
        def __init__(self, value):
            Exception.__init__(self)
            self.value = value
    # BEGIN PROBLEM 21
    try:

        cont = function.formals
        cont_body = function.body.first # where continuation and x is
        cont_x = cont_body.second.first # where the continuation's param x is

        cont_x = Pair(scheme_eval(cont_x, env), nil)

        cont = ContinuationProcedure(ContinuationError) # represent a continuation as a ContinuationProcedure

        cont.apply(cont_x, '_') # try to applied ContinuationProcedure
    except ContinuationError as e:
        result = e
    return result.value.first
    # END PROBLEM 21

class ContinuationProcedure(Procedure):
    def __init__(self, error_class):
        self.error_class = error_class

    def __str__(self):
        return '#[continuation: %x]' % hash(self.error_class)

    def apply(self, args, _):
        if not scheme_listp(args):
            raise SchemeError('arguments are not in a list: {0}'.format(args))
        if  args.second is not nil:
            raise SchemeError('a continuation takes only one argument')
        # BEGIN PROBLEM 21
        raise self.error_class(args)
        # END PROBLEM 21

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
}

# Utility methods for checking the structure of Scheme programs

def check_form(expr, min, max=float('inf')):
    """Check EXPR is a proper list whose length is at least MIN and no more
    than MAX (default: no maximum). Raises a SchemeError if this is not the
    case.

    >>> check_form(read_line('(a b)'), 2)
    """
    if not scheme_listp(expr):
        raise SchemeError('badly formed expression: ' + str(expr))
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

def check_procedure(procedure):
    """Check that PROCEDURE is a valid Scheme procedure."""
    if not scheme_procedurep(procedure):
        raise SchemeError('{0} is not callable: {1}'.format(
            type(procedure).__name__.lower(), str(procedure)))

#################
# Dynamic Scope #
#################

class MuProcedure(UserDefinedProcedure):
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
    def make_call_frame(self, args, env):
        """ Make call frame but the environment is from where it gets called.
        """

        # make a call frame that binds formals to args
        call_frame = env.make_child_frame(self.formals, args)
        call_frame.parent = env
        return call_frame
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
    # create a MuProcedure with formals, body
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

def complete_eval(val):
    """If VAL is an Thunk, returns the result of evaluating its expression
    part. Otherwise, simply returns VAL."""
    if isinstance(val, Thunk):
        return scheme_eval(val.expr, val.env)
    else:
        return val

def scheme_optimized_eval(expr, env, tail=False):
    """Evaluate Scheme expression EXPR in environment ENV. If TAIL, returns an
    Thunk object containing an expression for further evaluation."""
    # Evaluate atoms
    if scheme_symbolp(expr):
        return env.lookup(expr)
    elif self_evaluating(expr):
        return expr

    if tail:
        # BEGIN PROBLEM 20
        return Thunk(expr, env)
        # END PROBLEM 20
    else:
        result = Thunk(expr, env)

    while isinstance(result, Thunk):
        expr, env = result.expr, result.env
        # All non-atomic expressions are lists (combinations)
        if not scheme_listp(expr):
            raise SchemeError('malformed list: {0}'.format(str(expr)))
        first, rest = expr.first, expr.second
        if (scheme_symbolp(first) and first in SPECIAL_FORMS):
            result = SPECIAL_FORMS[first](rest, env)

        else:
            # BEGIN PROBLEM 20

            if isinstance(first, Pair):
                operator = scheme_eval(first, env)
                result = operator.eval_call(rest, env)
                # Have to check if the result is still a Thunk.
                # If it is, complete_eval it, else just return it
                if isinstance(result, Thunk):
                    return complete_eval(result)
                else:
                    return result

            # If first is not in the env, raise SchemeError
            operator = env.lookup(first)

            # Check the procedure
            operator = scheme_eval(first, env)
            check_procedure(operator)
            result = operator.eval_call(rest, env)

            # END PROBLEM 20

    return result

################################################################
# Uncomment the following line to apply tail call optimization #
################################################################
scheme_eval = scheme_optimized_eval


################
# Input/Output #
################

def read_eval_print_loop(next_line, env, interactive=False, quiet=False,
                         startup=False, load_files=()):
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
                    print(result)
        except (SchemeError, SyntaxError, ValueError, RuntimeError) as err:
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

    read_eval_print_loop(next_line, env, quiet=quiet)

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
               PrimitiveProcedure(scheme_eval, True, 'eval'))
    env.define('apply',
               PrimitiveProcedure(scheme_apply, True, 'apply'))
    env.define('load',
               PrimitiveProcedure(scheme_load, True, 'load'))
    env.define('call/cc',
               PrimitiveProcedure(scheme_call_cc, True, 'call/cc'))
    env.define('procedure?',
               PrimitiveProcedure(scheme_procedurep, False, 'procedure?'))
    env.define('undefined', None)
    add_primitives(env, PRIMITIVES)
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