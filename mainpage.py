import math

def isPrime(n):
	for i in range(2, n):
		if n%i==0: return False
	return True

def USAMO1(n):
	a, b=0, 0
	remain=4
	for i in range(11, n):
		if i%remain==1:
			if isPrime(i):
				a=(i+1)//2
				b=(3*i-1)//2
				print(i)
				print(str(a**b+b**a) + ',' + str(a+b))
				if (a**b+b**a)%(a+b)!=0: print(False)
				




print(USAMO1(100))

