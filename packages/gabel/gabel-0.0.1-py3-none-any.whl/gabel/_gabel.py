import sys as _sys
import time as _time
import os as _os

__all__ = ['hello', 'delay_print', 'clear', 'get_num']
def hello(name):
	print(f"Hello {name}, my name is Will Gabel")

def delay_print(s, end = ''):
	for c in s:
		_sys.stdout.write(c)
		_sys.stdout.flush()
		_time.sleep(0.04)
	print(end)

def get_num(prompt="Enter a number: ", start = False, finish = False, integar = False, round= False):
	while True:
		try:
			x = float(input(prompt))
		except ValueError:
			print("Please enter a number!")
			continue

		if finish != False:
			if start != False:
				if x > start and x < finish:
					return x
				else:
					print(f"Enter a value above {start} and below {finish}!")
					continue
			else:
				if x < finish:
					break
				else:
					print(f"Enter a value below {finish}!")
					continue
		elif start != False:
			if x > start:
				break
			else:
				print(f"Enter a value above {start}!")
				continue
		else:
			break
	if x == int(x):
		x = int(x)
	elif round == True:
		x = round(x)
	elif integar == True:
		x = int(x)
	print(x)
	return x
	
def clear():
	if _sys.platform.startswith('win32'):
		_os.system('cls')
	else:
		_os.system('clear')