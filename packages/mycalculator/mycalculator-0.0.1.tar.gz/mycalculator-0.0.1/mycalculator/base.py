
class base_calculator:

	def add(a,b):
		return a+b

	def sub(a, b):
		return a-b

	def mlt(a,b):
		return a*b

	def div(a,b):
		return a/b

	def simple_equation(a,b,c):
		print('value of a is=%.3f'%(a))
		print('value of b is=%.3f'%(b))
		print('value of c is=%.3f'%(c))
		return a+2*b+3*c