
# (1) create a mechanism for binding variables
_bindings_ = {}

def err(message):
    print "ERROR:", message
def var(name, value):
    global _bindings_
    _bindings_[name] = value
def val(name):
    global _bindings_
    if name not in _bindings_:
        err("%s not bound"%name)
    else:
        return _bindings_[name]
def reset():
    global _bindings_
    _bindings_ = {}
def print_bindings():
    global _bindings_
    print [(k, "func" if callable(v) else v) for k,v in _bindings_.iteritems()]

# (1) - END

# (2) - interpret the list
def interp(prog):
    print_bindings()
    print prog
    if isinstance(prog, list):
        # (3) - special form
        if prog[0] == 'if':
            if interp(prog[1]):
                return interp(prog[2])
            else:
                return interp(prog[3])
        # (4) - variable binding
        elif prog[0] == 'bind':
            var(prog[1], interp(prog[2]))
        # (5) - progn
        elif prog[0] == 'progn':
            progn = [interp(x) for x in prog[1:]]
            return progn[-1]
        # (6) - lambda
        elif prog[0] == 'lambda':
            return lambda : interp(prog[1])
        else:
        # (2)
            prog2 = [interp(x) for x in prog]
            return apply(prog2[0], prog2[1:])

    elif isinstance(prog, int):
        return prog
    else:
        return val(prog)

# (7) - we can now create functions but we still can't create functions that
# actually take arguments.
# We must introduce scope and variable binding within a scope
def getv(name, env):
   for frame in env[::-1]:
      if name in frame:
         return frame[name]
   err("binding for %s not found"%name)

def setv(name, value, env):
   for frame in env[::-1]: # reverse order
      if name in frame:
         frame[name] = value
         return
   # introduce a new binding
   env[-1][name] = value

def print_env(env):
    for frame in env:
        print [(k, "func" if callable(v) else v) for k,v in frame.iteritems()]

# Adding let means that we now have the concept of scope in our language
# Before we only had global scope now we have a new scope created in out let.
def interp_let(prog, env):
    print_env(env)
    print '>', prog
    if isinstance(prog, list):
        if prog[0] == 'if':
            if interp_let(prog[1], env):
                return interp_let(prog[2], env)
            else:
                return interp_let(prog[3], env)
        elif prog[0] == 'let': # fundamental decision - moving from a bind statement to a let
            # compound means that we no longer have any way to set a variable
            # once it's created - we've created a functional language
            new_scope_bindings = dict([(x[0], interp_let(x[1], env)) for x in prog[1]])
            return interp_let(prog[2], env + [new_scope_bindings])
        elif prog[0] == 'progn': # now progn is obsolete because we've removed the only operation with a side effect
            progn = [interp_let(x, env) for x in prog[1:]]
            return progn[-1]
        elif prog[0] == 'sub':
            return lambda new_env: interp_let(prog[1], env + new_env)
        # (8) - lambda with arguments
        elif prog[0] == 'lambda':
            return lambda new_env, *args: interp_let(prog[2], new_env + [dict(zip(prog[1], args))])
        # (10) - quote - don't evaluate
        elif prog[0] == 'quote':
            return prog[1] 
        else:
            prog2 = [interp_let(x, env) for x in prog]
            print ">>", prog[0], ', '.join([str(x) for x in prog2[1:]])
            return apply(prog2[0], [env] + prog2[1:])

    elif isinstance(prog, int):
        return prog
    else:
        return getv(prog, env)

# (3) - not interesting
def parse(prog):
    name = ''
    stack = [[]]
    for c in prog:
        if c in '() ' and name != '':
            try:
                stack[-1].append(int(name))
            except:
                stack[-1].append(name)
            name = ''

        if c == '(':
           stack.append([])
        elif c == ')':
           stack[-2].append(stack.pop())
        elif c not in ' \n':
           name += c

    return stack[0][0]
# (3) - END

def repl():
   line = ''
   while True:
      line += raw_input('repl> ' if line == '' else '   > ')
      if line.count('(') == line.count(')'):
         print interp_let(parse(line), initial_bindings())
         line = ''


def define(env, name, value):
    env[0][name] = value

def initial_bindings():
    return [{'add': lambda env,x,y: x+y,
            'eq': lambda env,x,y: x == y,
            'fst': lambda env,lst: lst[0],
            'rst': lambda env,lst: lst[1:],
            'lst': lambda env,*args: list(args),
            'nil?': lambda env,lst: lst == [],

            # (10) - also needs quote
            'define': define,
            }]

def test():
    # (1)
    print '-----1-----'
    var("a", 1)
    print val("a")
    print val("b")
    #(2)
    print '-----2-----'
    var("add", lambda x,y: x+y)
    print interp(["add", 2, ["add", "a", "a"]])
    # (3)
    print '-----3-----'
    print parse('(add 2 (if 0 (add a a) 5))')
    print interp(parse('(add 2 (if 1 (add a a) 5))'))
    # (4)
    print '-----4-----'
    print interp(parse('(bind b 10) (add 2 (if b (add a a) 5))'))
    reset()
    var("add", lambda x,y: x+y)
    print interp(parse('(bind a 1) (bind b (if a 0 2)) (add 2 (add a b))'))
    # it's returning none! --> progn
    # (5) 
    print '-----5-----'
    reset()
    var("add", lambda x,y: x+y)
    print interp(parse('(progn (bind a 1) (bind b (if a 0 2)) (add 2 (add a b)))'))
    # (6)
    print '-----6-----'
    reset()
    var("add", lambda x,y: x+y)
    print interp(parse('(progn (bind fn (lambda (add a b))) (bind a 1) (bind b (if a 0 2)) (add 2 (fn)))'))
    print '-----7-----'
    reset()
    var("add", lambda env,x,y: x+y)
    with open("test7.lisp", "r") as f:
       print interp_let(parse(f.read()), [_bindings_])
    print '-----8-----'
    reset()
    var("add", lambda env,x,y: x+y)
    with open("test8.lisp", "r") as f:
       print interp_let(parse(f.read()), [_bindings_])
    print '-----9-----'
    with open("test9.lisp", "r") as f:
       print interp_let(parse(f.read()), initial_bindings())
    print '-----10----'
    with open("test10.lisp", "r") as f:
       print interp_let(parse(f.read()), initial_bindings())
if __name__ == "__main__":
    test()
