"""
math.py
Paul's main Math module. This is still in its infancy, and is very buggy and limited. Use with caution. 
Author: Aaron Stockdill
"""

import paul

pi = 3.141592653589793
e = 2.718281828459045

class Node(object):
    
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
    
    def __str__(self):
        if self.left is None and self.right is None:
            return str(self.value)
        if (self.right.is_terminal() 
           and type(self.right.value) == int
           and self.right.value < 0 
           and self.value == "+"):
            v = "-"
            r = -1*self.right.value
        else:
            v = self.value
            r = self.right
        s =" ".join([str(item) for item in [self.left, v, r]
                      if item is not None])
        return "({})".format(s)
    
    def __repr__(self):
        return self.__str__()
    
    def __eq__(self, other):
        if type(other) != Node:
            return False
        if self.is_terminal() and other.is_terminal():
            return self.value == other.value
        else:
            l = self.left == other.left
            r = self.right == other.right
            t = self.value == other.value
            return l and r and t
    
    def replace(self, new_val, left=None, right=None):
        self.value = new_val
        self.left = left
        self.right = right
    
    def is_terminal(self):
        if self.left is None and self.right is None:
            return True
        return False


class Equation(object):
    
    def __init__(self, expression):
        ''' Initialize the tree with a string that is the equation '''
        self.original = expression
        self.head = Node("=")
        self.treeify(expression)
        self.simplify()
    
    
    def __str__(self):
        s = self.head
        count = 0
        while s == self.head and count < 5:
            s = self.simplify()
            count += 1
        return str(self.head)[1:-1]
    
    
    def __repr__(self):
        return self.__str__()
            

    def treeify(self, expression):
        ''' Create a tree representing the equation '''
        tokens = list(expression)
        tokens = self.join_digits(tokens)
        tokens = self.add_mult(tokens)
        equals = tokens.index("=")
        lhs = self.create_postfix(tokens[:equals])
        rhs = self.create_postfix(tokens[equals+1:])
        self.head.left = self.create_nodes(lhs)
        self.head.right = self.create_nodes(rhs)
        self.fix_add_inv()
    
    
    def add_mult(self, tokens):
        i = 0
        ops = list("=+-*/()^\\")
        new_toks = []
        while i < len(tokens)-1:
            new_toks.append(tokens[i])
            if tokens[i] not in ops and tokens[i+1] not in ops:
                new_toks.append("*")
            elif tokens[i] == ")" and tokens[i+1] == "(":
                new_toks.append("*")
            elif tokens[i] not in ops and tokens[i+1] == "(":
                new_toks.append("*")
            i += 1
        new_toks.append(tokens[i])
        paul.log("TOKENS:", new_toks)
        return(new_toks)
    
    
    def join_digits(self, expression):
        ''' Join two-or-more digit numbers together. Also spots pi and e '''
        numbers = list("1234567890.")
        letters = list("abcdefghijklmnopqrstuvwxyz")
        ops = list("(+*-^\\/")
        paul.log("DIGITIZING", expression)
        new_expression = []
        i = 0
        neg = False
        while i < len(expression):
            paul.log(expression[i], new_expression)
            if expression[i] == " ":
                i += 1
            elif expression[i] in letters:
                if expression[i] == "e":
                    new_expression.append(e)
                    i += 1
                elif expression[i] == "p" and expression[i+1] == "i":
                    new_expression.append(pi)
                    i += 2
                else:
                    new_expression.append(expression[i])
                    i += 1
            elif expression[i] == "-" and new_expression[-1] in ops:
                neg = True
                i += 1
            elif expression[i] not in numbers:
                new_expression.append(expression[i])
                i += 1
            else:
                number = ""
                j = i
                while j < len(expression) and expression[j] in numbers:
                    number += expression[j]
                    j += 1
                i = j
                if neg:
                    number = "-" + number
                    neg = False
                new_expression.append(float(number))
        return new_expression
    
    
    
    
    def create_postfix(self, expression):
        ''' Create the postfix version of the expression '''
        paul.log("STARTED POSTFIX ON", expression)
        operators = {"^":3,"\\":3,"*":2,"/":2,"+":1,"-":1,"(":0}
        stack = []
        postfix = []
        for item in expression:
            if item == "(":
                stack.append(item)
            elif item == ")":
                stacked = stack.pop()
                while stacked != "(":
                    postfix.append(stacked)
                    stacked = stack.pop()
            elif item not in list(operators.keys()):
                postfix.append(item)
            else:
                prec = operators[item]
                while len(stack) != 0 and prec <= operators[stack[-1]]:
                    postfix.append(stack.pop())
                stack.append(item)
        while len(stack) != 0:
            postfix.append(stack.pop())
        paul.log("ENDED POSTFIX ON", postfix)
        return postfix
    
    
    def create_nodes(self, stack):
        operators = list("^\\*/+-")
        paul.log("STARTED NODES ON", stack)
        if len(stack) == 1:
            return stack[0] if type(stack[0]) == Node else Node(stack[0])
        else:
            pos = 2
            for i in range(len(stack)):
                if stack[i] in operators:
                    pos = i
                    break
            n = Node(stack[pos])
            n.left = stack[pos-2] if type(stack[pos-2]) == Node else Node(stack[pos-2])
            n.right = stack[pos-1] if type(stack[pos-1]) == Node else Node(stack[pos-1])
            paul.log("STACK NOW", stack[:pos-2] + [n] + stack[pos + 1:])
            return self.create_nodes(stack[:pos-2] + [n] + stack[pos + 1:])
    
    
    
    def common_factor(self, node):
        op = node.value
        ll = node.left.left
        lr = node.left.right
        rl = node.right.left
        rr = node.right.right
        
        if ll.value == rl.value:
            n = Node("*")
            n.left = Node(ll.value)
            n.right = Node(op)
            n.right.left = lr
            n.right.right = rr
        elif ll.value == rr.value:
            n = Node("*")
            n.left = Node(ll.value)
            n.right = Node(op)
            n.right.left = lr
            n.right.right = rl
        elif lr.value == rl.value:
            n = Node("*")
            n.left = Node(lr.value)
            n.right = Node(op)
            n.right.left = ll
            n.right.right = rr
        elif lr.value == rr.value:
            n = Node("*")
            n.left = Node(lr.value)
            n.right = Node(op)
            n.right.left = ll
            n.right.right = rl
        else:
            n = Node(op)
            n.left = node.left
            n.right = node.right
        node.value = n.value
        node.left = n.left
        node.right = n.right
    
        
    def gcd_help(self, a, b):
        if a % b == 0:
            return b
        else:
            return self.gcd_help(b, a % b)
    
    
    def gcd(self, node):
        ''' Try and simplify fractions, e.g. 2/4 to 1/2 '''
        left = self.follow_to_end(node.left, "*")
        right = self.follow_to_end(node.right, "*")
        
        l = [item for item in left if type(item) == float]
        r = [item for item in right if type(item) == float]
        
        if l and r:
            l = l[0]
            r = r[0]
        
            c = self.gcd_help(max(l, r), min(l, r))
        
            self.replace(node.left, l, l/c)
            self.replace(node.right, r, r/c)
    
    
    def correct_sign(self, s1, s2):
        ''' 2 negatives make a positive and what not '''
        if s1 == s2:
            return "+"
        else:
            return "-"
    
    
    
    def prune_value(self, node, value, replace=1):
        ''' Prune just one value from the tree starting at node '''
        
        if node.is_terminal():
            if node.value == value:
                node.replace(replace)
        else:
            self.prune_value(node.left, value, replace)
            self.prune_value(node.right, value, replace)
        self.simplify(node)
        
    
    def follow_to_end(self, node, key):
        ''' Follow nodes of value 'key' to the base, return a list of all values '''
        if node.is_terminal():
            return [node.value]
        elif node.value != key:
            return []
        else:
            l1 = self.follow_to_end(node.left, key)
            l2 = self.follow_to_end(node.right, key)
            return l1 + l2
    
    
    def cancel(self, node):
        ''' Find common elements on the numerator and denominator '''
        
        if node.left == node.right:
            node.replace(1)
            return None
        
        left = self.follow_to_end(node.left, "*")
        right = self.follow_to_end(node.right, "*")
        
        common = []
        for i in left:
            for j in right:
                if i==j:
                    common.append(i)
                    
        if common:
            for item in common:
                self.prune_value(node.left, item)
                self.prune_value(node.right, item)
    
    def expand_helper_left(self, node1, node2):
        left = node1
        one = node2.left
        two = node2.right
        op = node2.value
        
        new_left = Node("*")
        new_left.left = left
        new_left.right = one
        self.simplify(new_left)
        
        new_right = Node("*")
        new_right.left = left
        new_right.right = two
        self.simplify(new_right)
        
        return new_left, new_right, op

    def expand_helper_right(self, node1, node2):
        left = node1
        one = node2.left
        two = node2.right
        op = node2.value
        
        new_left = Node("*")
        new_left.left = left
        new_left.right = two
        self.simplify(new_left)
        
        new_right = Node("*")
        new_right.left = left
        new_right.right = one
        self.simplify(new_right)
        
        return new_left, new_right, op
    
    
    def expand(self, node=-1):
        ''' Expand out any quadratic brackets '''
        if node == -1:
            node = self.head
        
        if (node.value == "*" 
            and node.left.is_terminal() 
            and not node.right.is_terminal() 
            and node.right.value in ["+", "-"]):
            left, right, op = self.expand_helper_left(node.left, node.right)
            node.value = op
            node.left = left
            node.right = right
        elif (node.value == "*" 
              and node.right.is_terminal() 
              and not node.left.is_terminal() 
              and node.left.value in ["+", "-"]):
            right, left, op = self.expand_helper_right(node.right, node.left)
            node.value = op
            node.right = right
            node.left = left
        elif (node.value == "*" 
              and not node.left.is_terminal() 
              and not node.right.is_terminal()):
            a = node.left.left
            b = node.left.right
            c = node.right.left
            d = node.right.right
            n = self.create_nodes([a, d, "*", a, c, "*", b, d, "*", "+", b, c, "*", "+", "+"])
            node.value = n.value
            node.left = n.left
            node.right = n.right
            self.simplify(node.left)
            self.simplify(node.right)
        elif node.value == "^" and node.right.value == 2 and not node.left.is_terminal():
            self.fps(node)
        else:
            pass
    
    
    def fps(self, node):
        ''' Fast perfect square '''
        a = node.left.left
        b = node.left.right
        sign = node.left.value
        if sign == "-":
            node.value = "-"
        elif sign == "+":
            node.value = "+"
        else:
            return None
        node.left = Node("^")
        node.left.left = Node(a)
        node.left.right = Node(2)
        node.right = Node("+")
        node.right.left = Node("*")
        node.right.left.left = Node(a)
        node.right.left.right = Node("*")
        node.right.left.right.left = Node(2)
        node.right.left.right.right = Node(b)
        node.right.right = Node("^")
        node.right.right.left = Node(b)
        node.right.right.right = Node(2)
    
    
    def simplify(self, node=-1):
        ''' Try and simplify the tree -- at the moment, only basically '''
        if node == -1:
            node = self.head
        
        ops = {
            "+": lambda x, y: x + y,
            "-": lambda x, y: x - y,
            "*": lambda x, y: x * y,
            "/": lambda x, y: x / y,
            "^": lambda x, y: x ** y,
            "\\": lambda x, y: x ** (1 / y),
            "=": lambda x, y: x == y
        }
        
        if node.value in ops.keys():
            self.simplify(node.left)
            self.simplify(node.right)
            nums = [int, float]
            
            val = node.value
            left =  node.left.value
            right = node.right.value
            
            if val in ["+", "-"] and right == "*" and left == "*":
                self.common_factor(node)
                #self.simplify()
            elif val == "/" and not (node.right.is_terminal() and node.left.is_terminal()):
                self.cancel(node)
                self.gcd(node)
            elif val in ["*", "^"]:
                self.expand(node)
            
            if val == "*":
                self.associativity(node, "*")
            elif val == "+":
                self.associativity(node, "+")
                
            paul.log("SIMPLIFYING", node)
            paul.log("VAL", val, "LEFT", left, "RIGHT", right)
            if type(left) in nums and type(right) in nums:
                paul.log("Simplify Option 1")
                node.value = ops[val](left, right)
                if node.value % 1 == 0:
                    node.value = int(node.value)
                node.left = None
                node.right = None
            elif val in ["+", "-"] and left == 0:
                paul.log("Simplify Option 2")
                node.value = node.right
                node.left = None
                node.right = None
            elif val in ["+", "-"] and right == 0:
                paul.log("Simplify Option 3")
                node.value = node.left
                node.left = None
                node.right = None
            elif val in ["*", "/"] and left == 1:
                paul.log("Simplify Option 4")
                node.value = node.right
                node.left = None
                node.right = None
            elif val in ["*", "/"] and right == 1:
                paul.log("Simplify Option 5")
                node.value = node.left
                node.left = None
                node.right = None
            elif val == "*" and (left == 0 or right == 0):
                paul.log("Simplify Option 6")
                node.value = 0
                node.left = None
                node.right = None
            elif val == "*" and (node.left == node.right):
                paul.log("Simplify Option 7")
                node.value = "^"
                node.right = Node(2)
            elif val == "^" and left == 0:
                paul.log("Simplify Option 8")
                node.value = 0
                node.left = None
                node.right = None
            elif val == "^" and right == 0:
                paul.log("Simplify Option 9")
                node.value = 1
                node.left = None
                node.right = None
        
        if type(node.value) == Node:
            node.left = node.value.left
            node.right = node.value.right
            node.value = node.value.value
    
    
    def replace(self, node, var, val):
        if node.value == var:
            node.value = val
        elif node.left is None and node.right is None:
            pass
        else:
            self.replace(node.left, var, val)
            self.replace(node.right, var, val)
        
    
    def substitute(self, *args):
        subs = args
        for var, val in subs:
            self.replace(self.head, var, float(val))
        self.simplify()
    
    
    def target_in_branch(self, node, target):
        if node.value == target:
            return True
        elif node.left is None and node.right is None:
            return False
        else:
            return (self.target_in_branch(node.left, target) 
                    or self.target_in_branch(node.right, target))
    
    
    def collect_values(self, node, condition):
        ''' Condition takes a node, returns a bool. '''
        if node.is_terminal():
            return ([node.value], True)
        if condition(node):
            a, i = self.collect_values(node.left, condition)
            b, j = self.collect_values(node.right, condition)
            return (a+b, i and j)
        else: 
            return ([node], False)
    
    
    def split(self, lst, cond):
        ''' Condition takes a value, returns a bool. '''
        a = []
        b = []
        for i in lst:
            if cond(i):
                a.append(i)
            else:
                b.append(i)
        return a, b
    
    
    def associativity(self, node, symbol):
        cond1 = lambda n: n.value == symbol
        cond2 = lambda n: type(n) in [int, float]
        vals, succ = self.collect_values(node, cond1)
        if succ:
            nums, varis = self.split(vals, cond2)
        else:
            return None
        if symbol == "*":
            n = 1
            check = 1
            for i in nums: n *= i
        elif symbol == "+":
            n = 0
            check = 0
            for i in nums: n += i
        if check != n:
            node.value = symbol
            node.left = Node(n)
            if varis:
                paul.log("VARIS:", varis)
                if len(varis) == 1:
                    node.right = Node(varis[0])
                else:
                    varis.sort()
                    oths = [varis[0]]
                    for i in varis[1:]:
                        oths.append(i)
                        oths.append(symbol)
                    node.right = self.create_nodes(oths)
    
    
    
    def rearrange_linear_for(self, target, show_steps=False):
        node = self.head
        ops = {
            "+": "-",
            "-": "+",
            "*": "/",
            "/": "*",
            "^": "\\",
            "\\": "^",
        }
        
        if show_steps:
            print(self.head)
        
        if node.left.value == target:
            self.simplify()
            return True
        
        in_left = self.target_in_branch(node.left, target)
        in_right = self.target_in_branch(node.right, target)
        
        if in_right:
            old_left = node.left 
            old_right = node.right
            node.right = old_left
            node.left = old_right
            self.rearrange_linear_for(target, show_steps)
        elif in_left:
            old_left = node.left 
            old_right = node.right
            value = ops[node.left.value]
            if value == "\\":
                display_val = "^"
            else:
                display_val = value
            node.right = Node(display_val)
            node.right.left = old_right
            if self.target_in_branch(node.left.right, target):
                if value == "\\":
                    n = Node("/")
                    n.left = Node(1)
                    n.right = node.left.left
                    node.right.right = n
                    node.left = node.left.right
                else:
                    node.right.right = node.left.left
                    node.left = node.left.right
            elif self.target_in_branch(node.left.left, target):
                if value == "\\":
                    n = Node("/")
                    n.left = Node(1)
                    n.right = node.left.right
                    node.right.right = n
                    node.left = node.left.left
                else:
                    node.right.right = node.left.right
                    node.left = node.left.left
            self.rearrange_linear_for(target, show_steps)
        
    
    def fix_add_inv(self, node=-1):
        if node == -1:
            node = self.head
        if node.is_terminal():
                    pass
        elif node.left.is_terminal() and node.right.is_terminal():
            if node.value == "-":
                node.value = "+"
                new_right = Node("*")
                new_right.left = Node(-1.0)
                new_right.right = node.right
                node.right = new_right
        else:
            self.fix_add_inv(node.left)
            self.fix_add_inv(node.right)



def make_equations(sentence):
    ''' Create a set of equations to work with '''
    eqn_string = []
    index = 0
    for word, _ in sentence:
        is_eq = (paul.has_one_of(word, "+/^*-=1234567890") 
                 or word in list("abcdefghijklmnopqrstuvwxyz"))
        if not is_eq:
            if len(eqn_string) != index:
                index += 1
        else:
            try:
                eqn_string[index] += word
            except IndexError:
                eqn_string.append(word)
        paul.log("EQN_STRING:", eqn_string, "INDEX:", index)
    return eqn_string



def process(sentence):
    ''' Process the sentence. '''
    
    sentence.replace_it()
    eqns = make_equations(sentence)
    if len(eqns) == 0:
        return "I'm not sure what you want me try try and solve. Sorry!"
    subs = sentence.has_one_of(["sub", "substitute", "solve"])
    rearrange = sentence.has_one_of(["rearrange", "solve"])
    if (paul.get_it() and
        paul.Sentence(paul.get_it()).has_one_of("+/^*-=1234567890")):
        eqns.append(paul.get_it())
    paul.log(eqns)
    eqn_string = eqns[0]
    if subs:
        try:
            eqn_string = eqns[1]
        except IndexError:
            eqn_string = eqns[0]
    if rearrange:
        for e in eqns:
            if len(e) > 1:
                eqn_string = e
    
    paul.log("SUBS:", subs, "REARRANGE:", rearrange)
    paul.log("EQUATION:", eqn_string)
    had_equals = True
    if not paul.has_word(eqn_string, "="):
        eqn_string = "y=" + eqn_string
        had_equals = False
    elif eqn_string.strip()[0] == "=":
        eqn_string = "y" + eqn_string
    paul.log("EQUATION:", eqn_string)
    
    # try:
    eqn = Equation(eqn_string)
    # except:
    #     return "Something went horribly wrong when I tried to math. Oops."
    # 
    if subs and len(eqns) > 1:
        eq2 = Equation(eqns[0])
        if type(eq2.head.right.value) == float:
            eqn.substitute((eq2.head.left.value, eq2.head.right.value))
        elif type(eqn.head.right.value) == float:
            eq2.substitute((eqn.head.left.value, eqn.head.right.value))
            eqn, eq2 = eq2, eqn
        else:
            url = "http://www.wolframalpha.com/input/?i="
            query = "sub {} into {}".format(eq2, eqn)
            query.replace("+", "%2D").replace("=", "%3D").replace("/", "%2F")
            paul.open_URL(url+query)
            return '''I was unsuccessful in finding the solution:\n{}\n{}'''.format(eq2, eqn)
    
    if rearrange:
        targ = "x"
        targets = sentence.keywords()
        for word, _ in targets:
            if len(word) == 1:
                targ = word
        try:
            eqn.rearrange_linear_for(targ)
        except RuntimeError:
            url = "http://www.wolframalpha.com/input/?i="
            query = "rearrange {} for {}".format(eqn, targ)
            query.replace("+", "%2D").replace("=", "%3D").replace("/", "%2F")
            paul.open_URL(url+query)
            return "Oh dear, not a clue. Try this instead."
    
    result = str(eqn)
    if not had_equals:
        result = result[4:]
    
    paul.set_it(result)
    try:
        if result[0] == "(" and result[-1] == ")": result = result[1:-1]
    except IndexError:
        pass
    return result
    
    

def main():
    ''' The main function '''
    
    words = {
        "solve": ("math", "verb"),
        "substitute": ("math", "verb"),
        "rearrange": ("math", "verb"),
    }
    
    paul.associate(words)
    paul.register("math", process)

main()