"""
math.py
Paul's main Math module. This is still in its infancy, and is very buggy and limited. Use with caution. Check all the values it produces.
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
        s =" ".join([str(item) for item in [self.left, self.value, self.right]
                      if item is not None])
        return "({})".format(s)
    
    def __repr__(self):
        return self.__str__()
    
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
        self.simplify()
        return str(self.head)[1:-1]
            

    def treeify(self, expression):
        ''' Create a tree representing the equation '''
        tokens = list(expression)
        tokens = self.join_digits(tokens)
        equals = tokens.index("=")
        lhs = self.create_postfix(tokens[:equals])
        rhs = self.create_postfix(tokens[equals+1:])
        self.head.left = self.create_nodes(lhs)
        self.head.right = self.create_nodes(rhs)
    
    
    def join_digits(self, expression):
        ''' Join two-or-more digit numbers together. Also spots pi and e '''
        numbers = list("1234567890.")
        letters = list("abcdefghijklmnopqrstuvwxyz")
        
        new_expression = []
        i = 0
        while i < len(expression):
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
                new_expression.append(float(number))
        return new_expression
    
    
    
    
    def create_postfix(self, expression):
        ''' Create the postfix version of the expression '''
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
        
        return postfix
    
    
    def create_nodes(self, stack):
        operators = list("^\\*/+-")
        
        if len(stack) == 1:
            return Node(stack[0])
        elif len(stack) == 3:
            n = Node(stack[2])
            n.left = stack[0] if type(stack[0]) == Node else Node(stack[0])
            n.right = stack[1] if type(stack[1]) == Node else Node(stack[1])
            return n
        else:
            next_ops = []
            for op in operators:
                if op in stack:
                    next_ops.append(stack.index(op))
            next_op = min(next_ops)
            n = Node(stack[next_op])
            vl = stack[next_op - 2]
            vr = stack[next_op - 1]
            n.left = vl if type(vl) == Node else Node(vl)
            n.right = vr if type(vr) == Node else Node(vr)
            return self.create_nodes(stack[:next_op - 2] + [n] + stack[next_op + 1:])
    
    
    
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
        
        if node.value == "*" and node.left.is_terminal() and not node.right.is_terminal():
            left, right, op = self.expand_helper_left(node.left, node.right)
            node.value = op
            node.left = left
            node.right = right
        elif node.value == "*" and node.right.is_terminal() and not node.left.is_terminal():
            right, left, op = self.expand_helper_right(node.right, node.left)
            node.value = op
            node.right = right
            node.left = left
        elif node.value == "*" and not node.left.is_terminal() and not node.right.is_terminal():
            sign = self.correct_sign(node.left.value, node.right.value)
            new_left = Node(node.right.value)
            new_left.left = Node("*")
            new_left.left.left = node.left.left
            new_left.left.right = node.right.left
            new_left.right = Node("*")
            new_left.right.left = node.left.left
            new_left.right.right = node.right.right
        
            new_right = Node(sign)
            new_right.left = Node("*")
            new_right.left.left = node.left.right
            new_right.left.right = node.right.left
            new_right.right = Node("*")
            new_right.right.left = node.left.right
            new_right.right.right = node.right.right
        
            node.value = node.left.value
            node.left = new_left
            node.right = new_right
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
            if type(left) in nums and type(right) in nums:
                node.value = Node(ops[val](left, right))
                node.left = None
                node.right = None
            elif val in ["+", "-"] and left == 0:
                node.value = node.right
                node.left = None
                node.right = None
            elif val in ["+", "-"] and right == 0:
                node.value = node.left
                node.left = None
                node.right = None
            elif val in ["*", "/"] and left == 1:
                node.value = node.right
                node.left = None
                node.right = None
            elif val in ["*", "/"] and right == 1:
                node.value = node.left
                node.left = None
                node.right = None
            elif val == "*" and (left == 0 or right == 0):
                node.value = 0.0
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


def make_equations(sentence):
    ''' Create a set of equations to work with '''
    eqn_string = []
    index = 0
    for word, _ in sentence:
        is_eq = paul.has_one_of(word, "+/^*-=1234567890")
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
    eqn_string = eqns[0]
    subs = sentence.has_one_of(["sub", "substitute", "solve"])
    rearrange = sentence.has_one_of(["rearrange", "solve"])
    if subs:
        try:
            eqn_string = eqns[1]
        except IndexError:
            eqn_string = eqns[0]
    
    paul.log("SUBS:", subs, "REARRANGE:", rearrange)
    paul.log("EQUATION:", eqn_string)
    had_equals = True
    if not paul.has_word(eqn_string, "="):
        eqn_string = "y=" + eqn_string
        had_equals = False
    elif eqn_string.strip()[0] == "=":
        eqn_string = "y" + eqn_string
    paul.log("EQUATION:", eqn_string)
    
    eqn = Equation(eqn_string)
    
    if subs and len(eqns) > 1:
        eq2 = Equation(eqns[0])
        if type(eq2.head.right.value) == float:
            eqn.substitute((eq2.head.left.value, eq2.head.right.value))
        elif type(eqn.head.right.value) == float:
            eq2.substitute((eqn.head.left.value, eqn.head.right.value))
            eqn, eq2 = eq2, eqn
        else:
            return '''I was unsuccessful in finding the solution:\n{}\n{}'''.format(eq2, eqn)
    
    if rearrange:
        targ = "x"
        targets = sentence.keywords()
        for word, _ in targets:
            if len(word) == 1:
                targ = word
        eqn.rearrange_linear_for(targ)
    
    result = str(eqn)
    if not had_equals:
        result = result[4:]
    
    paul.set_it(result)
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