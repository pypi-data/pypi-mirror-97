import sys as _sys
import time as _time
import os as _os

_all_ = ['hello', 'delay_print', 'get_int', 'clear']


def hello(name):
	string= f"Hello {name}, my name is Alek Chase"
	return string

def delay_print(s, end=''):
	for c in s:
		_sys.stdout.write(c)
		_sys.stdout.flush()
		_time.sleep(0.04)
	print(end)

def get_int(prompt="Enter a number", start=0, finish=0):
	while True:
		try:
			x = int(input(f"{prompt}: "))
			return x
		except ValueError:
			print("Please enter an integer!")
		if finish != 0:
			if start != 0:
				if x < finish and x > start:
					return x
			elif x < finish:
				return x
			else:
				print(f"Enter a value between {start} and {finish}")


def clear():
	if _sys.platform.startswith('win32'):
		_os.system('cls')
	else:
		_os.system('clear')
	return 0

def get_num(prompt="Enter a numbner: ", start=False, finish=False, integer=False, round_up=False):
	while True:
		try:
			x = float(input(prompt))
			if integer:
				if round_up:
					num = x - int(x)
			#	 0.99	1.99	- 1
					if num >= 0.5:
						x=int(x)+1
				# 1.99 -> 1
			else:
				x = int(x)
		except ValueError:
			print("Please enter a number!")
			continue
		if finish != False:
			if start != False:
				if x < finish and x > start: # and means both boolean statements NEED to be true
				# start < x < finish
					return x
				else:
					print(f"Enter a value between {start} and {finish}!")	
			else: #start == False
				if x < finish:
					return x
				else:
					print(f"Enter a value below {finish}!")
					continue
		elif start != False:
			if x > start:
				return x
			else:
				print(f"Enter a value above {finish}!")
				continue
		else:
			return x



get_num(start=1, finish=3)		
