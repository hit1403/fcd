
class TreeNode:
    def __init__(self, value):
        self.value = value
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def __str__(self):
        return str(self.value)


def generate_code(expression):
    global temp_count
    code = []
    stack = []
    tokens = expression.split()
    for token in tokens:
        if token.isalnum():
            stack.append(token)
        else:
            op2 = stack.pop()
            op1 = stack.pop()
            temp = "T"+str(temp_count)
            temp_count += 1
            code.append((token, op1, op2, temp))
            stack.append(temp)
    return code





def construct_tree(code):
    stack = []
    for op, op1, op2, temp in code:
        node = TreeNode((op, temp))
        if op1.isdigit() or op1.isalpha():
            node.add_child(TreeNode(op1))
        else:
            node.add_child(stack.pop())

        if op2.isdigit() or op2.isalpha():
            node.add_child(TreeNode(op2))
        else:
            node.add_child(stack.pop())
        stack.append(node)
    return stack.pop()


def print_tree(node, level=0):
    if node:
        print("  " * level + str(node))
        for child in node.children:
            print_tree(child, level + 1)


def infix_to_postfix(expression):
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
    output = []
    operator_stack = []
    for token in expression.split():
        if token.isdigit():
            output.append(token)
        elif token == '(':
            operator_stack.append(token)
        elif token == ')':
            while operator_stack and operator_stack[-1] != '(':
                output.append(operator_stack.pop())
            operator_stack.pop()
        else:
            while operator_stack and precedence.get(token, 0) <= precedence.get(operator_stack[-1], 0):
                output.append(operator_stack.pop())
            operator_stack.append(token)
    while operator_stack:
        output.append(operator_stack.pop())
    return ' '.join(output)


# Main program starts here
temp_count = 0
infix_expression = "3 + 4 * ( 2 - 1 )"
postfix_expression = infix_to_postfix(infix_expression)
lines = generate_code(postfix_expression)
root = construct_tree(lines)
print_tree(root)

