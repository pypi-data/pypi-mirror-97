def average(*args):
	a=0
	for arg in args:
		a += 1
	print(f"The average is {sum(args)/a}")

average(5, 5, 5, 4, 2, 2)

