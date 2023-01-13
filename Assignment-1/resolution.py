import sys
file1 = sys.argv[1]
file2 = sys.argv[2]
f = open(file1, "r")

i = 1
formula = {}
for x in f:
  if(i > 2):
    s = x.split()
    formula[i] = set([int(value) for value in s if value != "0"])
  i += 1

f = open(file2, "r")

i = 1
proof = {}
lines = {}
for x in f:
  s = x.split()
  j = 0
  lines[i] = s[:2]
  proof[i] = set([int(value) for value in s[2:] if value != "0"])
  i += 1

correct = True
for i in lines:
  x = lines[i]
  s1 = []
  s2 = []
  if(x[0][1] == 'f'):
    s1 = formula[int(x[0][0])]
  else:
    s1 = proof[int(x[0][0])]
  if(x[1][1] == 'f'):
    s2 = formula[int(x[1][0])]
  else:
    s2 = proof[int(x[1][0])]
  res = list(s1) + list(s2)
  for j in proof[i]:
    if j not in res:
      correct = False
      break
    res.remove(j)
  if correct == False:
    break
  found = False
  for j in res:
    if -1*j in res:
      temp = []
      temp.extend(res)
      temp.remove(j)
      temp.remove(-1*j)
      flag = True
      for k in temp:
        if k not in proof[i]:
          flag = False
          break
      if flag:
        found = True
        break
  if found == False:
    correct = False
  if correct == False:
    break

if(correct and proof[len(proof)] == set()):
  print("correct")
else:
  print("incorrect")