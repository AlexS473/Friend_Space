# 816001671 Question 5b COMP 3601 Final Exam June 2020


def changeMaking(D, n):
	# changeMaking algorithm adapted from the Dynamic Programming lecture
	F = [0 for i in range(n+1)]  # Creates the array to establish it's length
	m = len(D)
	for i in range(1, n+1):
		temp = float('inf')
		j = 1
		while j <= m-1 and D[j] <= i:
			temp = min(F[i - D[j]], temp)
			j += 1
		F[i] = temp +1
	print("The minimum number of coins to make change for n = ", n, " is ", F[n])
	return F[n], F  # returns F instead of using a global variable


def Backtrack(D, n, minimum, F):
	s = []  # stores the minimum coin set as it is generated
	j = len(D)-1
	while j >= 1 and n > 0:
		# checking the computations for  their component denominations
		if F[n-D[j]] + 1 == minimum and D[j] <= n:
			s.append(D[j])
			n = n - D[j]
			if n > 0:
				j = len(D) - 1  # reset the pointer to the denominations array
				minimum = F[n]  # move to the next minimum produced
			else:
				j = 0
		else:
			j -= 1
	return s


D = [0, 1, 5, 10]
n = 8
minm, F = changeMaking(D, n)
min_coin_set = Backtrack(D, n, minm, F)
print("The minimum coin set for n = ", n, "is", min_coin_set)
