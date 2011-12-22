'''
	Name: Cha Li
	Date: 09.30.2011
	Class: TA - CS007

	This program recursively calculates the nth number in the fibonacci sequence.
	I'm going to use f(n) to represent the value of the nth fibonacci number
	The first number is the 0th number.
	0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, ...

	The value of the nth fibonacci number is the sum of the previous 2 
	numbers:
	f(n) = f(n-1) + f(n-2)


	More Info:
	http://en.wikipedia.org/wiki/Fibonacci_number
'''


#this function is used to recursively calculate f(n)
def fib(n):
	#base cases, f(0) = 0, f(1) = 1
	if n == 0:
		return 0;
	elif n == 1:
		return 1;
	
	#the recursive call
	#the value of f(n) is the sum of the two numbers that preceed it:
	#f(n) = f(n-1) + f(n-2)
	#
	#NOTE: before f_n can be calculated, the two function calls on the right 
	#have to be calculated
	f_n = fib(n - 1) + fib(n - 2);
	return f_n;
	

#get user input and run the fib function
#need to convert numbers to strings before concatenating them
number = input("Which fibonacci number, f(n), do you want to know? n=")
print "f(" + str(number) + ") = " + str(fib(number));


#SIDENOTE:
#this is one of those examples where it's more efficient to use a standard
#loop instead of recursion. The recursive approach duplicates a lot of 
#math (for example, it might calculate fib(3) more than once). For small 
#values of n this doesn't really matter but for large values, the program
#is repeating A LOT of math it's already done. A loop wouldn't waste time
#recalculating values.


