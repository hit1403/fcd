
class Node:
  def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None
        self.val = None
next=0
logic=['&&','||','!']
relop=['<','>','<=','>=','==','!=']
inp=input("Enter the String : ")
inp = [i for i in inp.split()]
print(inp)
print("\n")
st=[]
while True:

  if inp[0] >='a' and inp[0]<='z':
    if inp[1] in relop and inp[2] >='a' and inp[2]<='z':
      root=Node('E')
      root.val=str(inp[0]+inp[1]+inp[2])
      print('if ',inp[0],inp[1],inp[2],'goto',next+3)
      print('E = 0')
      print('goto',next+2)
      print('E = 1')
      next+=4
      inp=inp[3:]
      st.append(root)

  elif inp[0] in logic:
    st.append(inp[0])
    inp=inp[1:]

  if len(st)==3:
    root=Node(st[1])
    root.left=st[0]
    root.right=st[2]
    root.val=str(st[0].data+root.data+st[2].data)
    print('E = ',st[0].data,root.data,st[2].data)
    st=[root]

  if len(inp)==0:
    break



def inorder(root):
  if root==None:
    return
  inorder(root.left)
  print("---------------------")
  print("Value : ",root.data)
  print("left : ",root.val)
  print("---------------------\n")
  inorder(root.right)
inorder(root)