
# (1) create a mechanism for binding variables
_bindings_ = {}

def err(message):
    print "ERROR:", message
def var(name, value):
    _bindings_[name] = value
def val(name):
    if name not in _bindings_:
        err("%s not bound"%name)
    else:
        return _bindings_[name]
# (1) - END

# (2) - interpret the list
def interp(prog):
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
        else:
        # (3) - END
        # (2)
            prog2 = [interp(x) for x in prog]
            return apply(prog2[0], prog2[1:])

    elif isinstance(prog, int):
        return prog
    else:
        return val(prog)


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
        elif c != ' ':
           name += c

    return stack[0][0]
# (3) - END

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
    _bindings_ = {} # reset bindings
    print interp(parse('(bind a 1) (bind b (if a 0 2)) (add 2 (add a b))'))
    # it's returning none! --> progn
    # (5) 
    print interp(parse('(progn (bind a 1) (bind b (if a 0 2)) (add 2 (add a b)))'))
    # (6)

if __name__ == "__main__":
    test()
