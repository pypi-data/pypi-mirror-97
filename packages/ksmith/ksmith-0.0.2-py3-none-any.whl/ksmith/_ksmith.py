import sys as _sys
import time as _time
import os as _os

__all__= ['hello', 'delay_print','clear','get_num','delay']

def delay(x):
	_time.sleep(x)

def hello(name):
	string = f"Hello {name}, my name is Kent Smith"
	return string

def delay_print(s, end=''):
	for c in s:
		_sys.stdout.write(c)
		_sys.stdout.flush()
		_time.sleep(0.04)
	print('end')
	return 0

def get_num(prompt="Enter a number:", start=False, finish=False, integer=False, round_up=False):
	while True:
		try:
			x = float(input(prompt))
			if integer:
				if round_up:
					num=x - int(x)
					if num >= 0.5:
						x= int(x)+1
				else:
					x = int(x)
		except ValueError:
			print("Please enter a number!")
			continue
		if finish != False:
			if start != False:
				if x <= finish and x >= start:
					return x
				else: 
					print(f"Enter a value between {start} and {finish}!")
			else:
				if x <= finish:
					return x
				else:
					print(f"Enter a value below {finish}!")
					continue
		elif start != False:
			if x >= start:
				return x
			else:
				print(f"Enter a value above {start}!")
				continue
		else:
			return x
		

#print(get_num(start=3,finish=5,integer=True,round_up=True))	test get_num



def clear():
	if _sys.platform.startswith('win32'):
		_os.system('cls')
	else:
		_os.system('clear')
	return 0
