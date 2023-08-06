
"""
Created by Snehashish Laskar
Email : snehashish.laskar@gmail.com
Created on 08-03-2021
This a very Basic Simple Intrest  and Compound intrest calculator
This is a very simple project to try

"""
import webbrowser

def SimpleIntrest():
	principal = input("please enter the principal or the money you want to lend/deposit:")

	while True:
		rate = input("please enter the rate of intrest or if you wanna google it hen type g:")

		if rate == "g":
			webbrowser.open("www.google.com")
		else:
			break

	time = int(input("please enter the time period: "))

	intrest = (int(principal)*int(rate)*time)/100

	amount = int(principal)+intrest

	print(f" You'r money will amount to {amount} and the intrest you are paying is {intrest}")


def CompoundIntrest():
	principal = int(input("please enter the principal or the money you want to lend/deposit:"))
	while True:
		rate = input("please enter the rate of intrest or if you wanna google it then type g:")

		if rate == "g":
			webbrowser.open("www.google.com")
		else:
			rate = int(rate)/100
			break

	time = int(input("please enter the time period: "))


	amount = principal*((1 + rate)**time)

	intrest = amount - principal

	print(f" You'r money will amount to {amount} and the intrest you are paying is {intrest}")

def Run():
	while True:
		print("Type s below to calculate simple intrest , type c to calculate compound intrest or type q to quit:")
		in1 = input()

		if in1 == "s":
			SimpleIntrest()

		elif in1 == "c":
			CompoundIntrest()
		elif in1 == "q":
			exit()

