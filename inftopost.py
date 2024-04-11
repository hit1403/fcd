#infix to postfix and tree geneartion


result = []
stack = []
def prec(c):
	if c == '/' or c == '*':
		return 2
	elif c == '+' or c == '-':
		return 1
	else:
		return -1

def infix_to_postfix(s):
	for i in range(len(s)):
		c = s[i]
		if ('a' <= c <= 'z') or ('A' <= c <= 'Z') or ('0' <= c <= '9'):
			result.append(c)
		elif c == '(':
			stack.append(c)
		elif c == ')':
			while stack and stack[-1] != '(':
				result.append(stack.pop())
			stack.pop()
		else:
			while stack and (prec(s[i]) < prec(stack[-1]) or (prec(s[i]) == prec(stack[-1]) )):
				result.append(stack.pop())
			stack.append(c)

	while stack:
		result.append(stack.pop())
	print(''.join(result))

exp = "a+b*c"

infix_to_postfix(exp)

print(result)

operator=['+','-','*','/']
class Node:
  def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None
        self.vall = None
        self.valr = None
stack=[]
ops=[]
i=0
while i<len(result):
  if result[i] not in operator:
    root=Node(result[i])
    root.left=None
    root.right=None
    root.data=result[i]
    stack.append(root)
    print(result[i])
  else:
    if len(stack)>=2:
      root=Node(result[i])
      r=stack.pop()
      l=stack.pop()
      root.left=l
      root.right=r
      root.vall = l.data
      root.valr=r.data
      root.data=result[i]
      stack.append(root)
      print(result[i])
  i+=1


def inorder(root):
  if root==None:
    return
  inorder(root.left)
  print("---------------------")
  print("Value : ",root.data)
  print("left : ",root.vall)
  print("right : ",root.valr)
  print("---------------------\n")
  inorder(root.right)
inorder(root)