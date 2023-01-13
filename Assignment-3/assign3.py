import sys

def n1(formula):
	for i in formula:
		count = 0
		for j in formula[i]:
			if(j > 0):
				count += 1
		if count > 1:
			return False
	return True


def n2(formula):
	ans = []
	for i in formula:
		temp = list(formula[i])
		for j in range(len(temp)):
			for i in range(j):
				if [temp[i], temp[j]] not in ans:
					ans.append([temp[i], temp[j]])
	return ans

def dfs(root, visited, adj, order):
	if(visited[root]):
		return
	visited[root] = True
	for i in adj[root]:
		dfs(i, visited, adj, order)
	order.append(root)

def dfs1(root, visited, adj, scc, n):
	if(visited[root]):
		return
	visited[root] = True
	scc[root] = n
	for i in adj[root]:
		dfs1(i, visited, adj, scc, n)

def n3(sat, num):
	adj = {}
	adjInv = {}
	visited = {}
	visitedInv = {}
	scc = {}
	for i in range(1, num + 1):
		adj[i] = []
		adj[-1*i] = []
		adjInv[i] = []
		adjInv[-1*i] = []
		visited[i] = False
		visited[-1*i] = False
		visitedInv[i] = False
		visitedInv[-1*i] = False
		scc[i] = -1
		scc[-1*i] = -1
	for i in sat:
		adj[-1*i[0]].append(i[1])
		adj[-1*i[1]].append(i[0])
		adjInv[i[1]].append(-1*i[0])
		adjInv[i[0]].append(-1*i[1])

	# print(adj)
	# print(adjInv)
	order = []
	for i in visited:
		if(visited[i] == False):
			dfs(i, visited, adj, order)
	n = 0
	for i in order[::-1]:
		if(visitedInv[i] == False):
			dfs1(i, visitedInv, adjInv, scc, n)
			n += 1

	# print(scc)
	return scc


# Do not change the name of the function. 
# Do not use global variables as we will run your code on multiple test cases.
# 
def solve(inputString, n):
	#
	# Write your code here
	#
	formula = {}
	i = 1
	num = 0
	inputString = inputString.split("\n")
	for x in inputString:
		if(i == 2):
			s = x.split()
			num = int(s[2])
		if(i > 2):
			s = x.split()
			formula[i] = set([int(value) for value in s if value != "0"])
		i += 1

	# For n = 1
	if(n == 1):
		# print(formula)
		# print(num)
		isHorn = n1(formula)
		if(isHorn):
			return "already horn"
		else:
			return "not horn"

	# For n = 2
	if(n == 2):
		isHorn = n1(formula)
		res = ""
		if(isHorn):
			res += "c here is an empty CNF formula over " + str(num) + " variables\n"
			res += "p cnf " + str(num) + " 0"
		else:
			ans = n2(formula)
			res += "c 2-CNF formula which is sat iff input is renamable Horn\n"
			res += "p cnf " + str(num) + " " + str(len(ans)) + "\n"
			for x in ans:
				res += str(x[0]) + " " + str(x[1]) + " 0\n"
		return res

	# For n = 3
	if(n == 3):
		isHorn = n1(formula)
		if(isHorn):
			return "already horn"
		else:
			ans = n2(formula)
			scc = n3(ans, num)
			for i in range(1, num + 1):
				if(scc[i] == scc[-1*i]):
					return "not renamable"
			return "renamable"
		

	if(n == 4):
		isHorn = n1(formula)
		if(isHorn):
			return "already horn"
		else:
			ans = n2(formula)
			scc = n3(ans, num)
			for i in range(1, num + 1):
				if(scc[i] == scc[-1*i]):
					return "not renamable"
			res = ""
			for i in range(1, num + 1):
				if(scc[i] > scc[-1*i]):
					res += str(i) + " "
			return res



	return "nil"


# Main function: do NOT change this.
if __name__=="__main__":
	inputFile = sys.argv[1]
	n = int(sys.argv[2])
	with open(inputFile, 'r') as f:
		inputString = f.read()
		print(solve(inputString, n))
