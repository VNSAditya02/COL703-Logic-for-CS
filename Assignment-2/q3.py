import sys
sys.setrecursionlimit(100000)

def resolve(set1, set2):
	l = []
	for i in set1:
		if (-1*i in set2):
			l.append([abs(i), i])
	if l == []:
		return "Unable"
	l.sort()
	res = []
	for element in l:
		s1 = set1.copy()
		s2 = set2.copy()
		s1.remove(element[1])
		s2.remove(-1*element[1])
		res.append(s1.union(s2))
	return res

def backtrack(line_no, formula, proof, lines):
	# If all the lines are processed, check if the last line is empty
	# print(lines)
	if line_no == len(lines) + 1:
		if proof[line_no - 1] != set():
			return False
		else:
			return True

	# If both clauses are already filled, go to next line	
	if lines[line_no][0] != "??" and lines[line_no][1] != "??":
		c1 = lines[line_no][0]
		c2 = lines[line_no][1]
		s1 = set()
		s2 = set()

		# Get clause 1
		if c1[1] == 'f':
			s1 = formula[int(c1[0])]
		elif c1[1] == 'p' and int(c1[0]) >= line_no:
			return False
		else:
			s1 = proof[int(c1[0])]

		# Get clause 2
		if c2[1] == 'f':
			s2 = formula[int(c2[0])]
		elif c2[1] == 'p' and int(c2[0]) >= line_no:
			return False
		else:
			s2 = proof[int(c2[0])]

		res = resolve(s1, s2)
		for temp in res:
			proof[line_no] = temp
			ans = backtrack(line_no + 1, formula, proof, lines)
			if ans:
				return True
		return False

	# Check which clause is not filled and store the other clause in s1
	c1 = lines[line_no][0]
	c2 = lines[line_no][1]
	s1 = set()
	notfilled = -1

	if c1 == "??":
		notfilled = 0
		if c2[1] == 'f':
			s1 = formula[int(c2[0])]
		elif c2[1] == 'p' and int(c2[0]) >= line_no:
			return False
		else:
			s1 = proof[int(c2[0])]
	else:
		notfilled = 1
		if c1[1] == 'f':
			s1 = formula[int(c1[0])]
		elif c1[1] == 'p' and int(c1[0]) >= line_no:
			return False
		else:
			s1 = proof[int(c1[0])]

	for i in formula:
		res = resolve(s1, formula[i])
		if res != "Unable":
			for temp in res:
				proof[line_no] = temp
				lines[line_no][notfilled] = str(i) + "f"
				ans = backtrack(line_no + 1, formula, proof, lines)
				if ans:
					return True
				proof[line_no] = {}
				lines[line_no][notfilled] = "??"

	for i in range(1, line_no):
		res = resolve(s1, proof[i])
		if res != "Unable":
			for temp in res:
				proof[line_no] = temp
				lines[line_no][notfilled] = str(i) + "p"
				ans = backtrack(line_no + 1, formula, proof, lines)
				if ans:
					return True
				proof[line_no] = {}
				lines[line_no][notfilled] = "??"
	return False

def solve(formula_file, modified_proof_file, ouput_file):
	f1 = open(formula_file, "r")
	f2 = open(modified_proof_file, "r")

	# Read Formula File
	formula = {}
	i = 1
	for x in f1:
		if(i > 2):
			s = x.split()
			formula[i] = set([int(value) for value in s if value != "0"])
		i += 1

	# Read Proof file
	i = 1
	lines = {}
	for x in f2:
		s = x.split()
		lines[i] = s[:2]
		i += 1

	proof = {}

	# print(formula)
	# print(lines)
	ans = backtrack(1, formula, proof, lines)
	output = open(ouput_file, "w")
	if ans:
		for i in lines:
			output.write(lines[i][0] + " " + lines[i][1] + " ")
			for j in proof[i]:
				output.write(str(j) + " ")
			output.write("0\n")
	else:
		for i in lines:
			if lines[i][0] == "??":
				lines[i][0] = "np"
			if lines[i][1] == "??":
				lines[i][1] = "np"
		for i in lines:
			output.write(lines[i][0] + " " + lines[i][1] + "\n")
	output.close()