def parse_expression(exp):

    asg = exp[0]
    stack = list(exp[2:])
    int_code = {}
    count = 0
    
    for i in range(len(exp)):
        if exp[i] == ')':
            s = ''
            while stack[-1] != '(':
                s = stack.pop() + s
            stack.pop()  

            count += 1
            temp_var = f'T{count}'
            int_code[temp_var] = s
            stack.append(temp_var)
        else:
            stack.append(exp[i])
    
    int_code[asg] = f'T{count}'
    return int_code

def generate_quadruples(int_code):
    
    operators = ['*', '+', '-', '/']
    quadruples = []
    
    for k, v in int_code.items():
        if v[0] == '-':
            quadruples.append((v[0], v[1:], '-', k))
        else:
            flag = 0
            for i in operators:
                if i in v:
                    flag = 1
                    ind = v.index(i)
                    quadruples.append((v[ind], v[0:ind], v[ind + 1:], k))
                    break
            if flag == 0:
                quadruples.append(('=', v, '-', k))
    
    
    for quadruple in quadruples:
        print(quadruple)

def generate_triples(int_code):
    
    operators = ['*', '+', '-', '/']
    triples = []
    
    for k, v in int_code.items():
        if v[0] == '-':
            triples.append((v[0], v[1:], '-'))
        else:
            flag = 0
            for i in operators:
                if i in v:
                    flag = 1
                    ind = v.index(i)
                    triples.append((v[ind], v[0:ind], v[ind + 1:]))
                    break
            if flag == 0:
                triples.append(('=', k, v))
                
    for triple in triples:
        print(triple)


def main():
    exp = input("\nEnter arithmetic expression:  ")
    print("\nARITHMETIC EXPRESSION: ", exp)
    
    int_code = parse_expression(exp)
    choice = int(input("\nChoose: 1 >> QUADRUPLES\nChoose: 2 >> TRIPLES\n\n>>> "))
    
    if choice == 1:
        print("\nQUADRUPLES\n")
        generate_quadruples(int_code)
    elif choice == 2:
        print("\nTRIPLES\n")
        generate_triples(int_code)
    else:
        print("\nInvalid choice")

if _name_ == "_main_":
    main()