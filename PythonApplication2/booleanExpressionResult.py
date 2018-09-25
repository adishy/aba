#http://www.martinbroadhurst.com/shunting-yard-algorithm-in-python.html
def is_search_text(str):
    return not (str in ['&&', '||', '(', ')'])
 
def peek(stack):
    return stack[-1] if stack else None
 
def apply_operator(operators, values):
    operator = operators.pop()
    right = values.pop()
    left = values.pop()

    print('Apply operator')

    print(operator)

    if operator == '||':
        values.append(left | right)

    elif operator == '&&':
        values.append(left & right)
 
def greater_precedence(op1, op2):
    precedences = {'||' : 0, '&&' : 1}
    return precedences[op1] > precedences[op2]
 
def boolean_evaluate(some_expression):
    print('Evaluate expression')

    print(some_expression)

    tokens = some_expression

    print(some_expression)

    values = []
    operators = []

    for token in tokens:
        if is_search_text(token):
            values.append(token)
        elif token == '(': 
            operators.append(token)
        elif token == ')':
            top = peek(operators)
            while top is not None and top != '(':
                apply_operator(operators, values)
                top = peek(operators)
            print(values)
            operators.pop() # Discard the '('
        else:
            # Operator
            top = peek(operators)
            while top is not None and top not in "()" and greater_precedence(top, token):
                apply_operator(operators, values)
                top = peek(operators)
            operators.append(token)
    while peek(operators) is not None:
        apply_operator(operators, values)
 
    return values[0]
