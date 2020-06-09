# 816001671 Question 5b COMP 3601 Final Exam June 2020
def changeMaking(D, n):
	m = len(D)
	F[0] = 0
	for i in range (len(F)):
		temp = float('inf')
		j = 1
		while j <= m and D[j] <= i:
			temp = min(F[i - D[j]], temp)
			j += 1
		F[i] = temp +1
	return F[n]


global F
