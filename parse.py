#slr parsing

from prettytable import PrettyTable
from collections import defaultdict

parseTable = PrettyTable(["Stack", "Action", "Input"])

terminals = ["+","*","i","$"]
nonTerminals = ["E","T","F"]

table=defaultdict(dict)
table['0']= {'+': '', '*': '', 'i': 'shift 4', '$': '', 'E': '1', 'T': '2', 'F': '3'}
table['1']= {'+': 'shift 5', '*': '', 'i': '', '$': 'ACC', 'E': '', 'T': '', 'F': ''}
table['2']= {'+': 'reduce E->T', '*': 'shift 6', 'i': '', '$': 'reduce E->T', 'E': '', 'T': '', 'F': ''}
table['3']= {'+': 'reduce T->F', '*': 'reduce T->F', 'i': '', '$': 'reduce T->F', 'E': '', 'T': '', 'F': ''}
table['4']= {'+': 'reduce F->i', '*': 'reduce F->i', 'i': '', '$': 'reduce F->i', 'E': '', 'T': '', 'F': ''}
table['5']= {'+': '', '*': '', 'i': 'shift 4', '$': '', 'E': '', 'T': '7', 'F': '3'}
table['6']= {'+': '', '*': '', 'i': 'shift 4', '$': '', 'E': '', 'T': '', 'F': '8'}
table['7']= {'+': 'reduce E->E+T', '*': 'shift 6', 'i': '', '$': 'reduce E->E+T', 'E': '', 'T': '', 'F': ''}
table['8']= {'+': 'reduce T->T*F', '*': 'reduce T->T*F', 'i': '', '$': 'reduce T->T*F', 'E': '', 'T': '', 'F': ''}

inp=input("Enter a string:")+"$"

stack=['0']
top=-1
while inp:
    do=table[stack[top]][inp[0]]
    if do=="":
      parseTable.add_row(["".join(stack),"REJECTED",inp])
      break
    if do=="ACC":
      parseTable.add_row(["".join(stack),"ACCEPT",inp])
      break
    parseTable.add_row(["".join(stack),do,inp])
    if do.startswith("shift"):
      stack.extend([inp[0],do.lstrip("shift ")])
      inp=inp[1:]
    elif do.startswith("reduce"):
        production=do.lstrip("reduce ").split("->")
        replace_string=""
        stack_replace_string=""
        for i in range(len(stack)-1,0,-1):
            stack_replace_string+=stack[i]
            if stack[i] in terminals or stack[i] in nonTerminals:
              replace_string+=stack[i]
            rev_string=replace_string[::-1]
            if rev_string == production[1]:
              break
        for chr in range(len(stack_replace_string)):
            stack.pop()
        stack.append(production[0])
        stack.append(table[stack[-2]][stack[-1]])

print(parseTable)