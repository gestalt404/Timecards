import pandas as pd
import csv
import pprint
from datetime import datetime as dt
from datetime import timedelta
import os
 
# shifts source file name
shiftsName = "Shifts.xlsx"
# logins source file name
loginsName = "Logins.xlsx"

employees = {}
inv = []
logins = []
lateArrivals= []

# ascii escape codes for text colors
green = "\033[1;32m"
yellow = "\033[1;33m"
red = "\033[1;31m"
purple = "\033[1;35m"
blue = "\033[1;34m"
reset = "\033[m"

# directions string
directions = """Instructions:
'help'\t- to see these directions again
'pid'\t- of employee to see breakdown (aproximate value is ok)
'calc'\t- to see result
'end'\t- to stop program"""
# break string
breakString = "------------------------------"


def main():
	print("Generating Employees...  ", end = "\r")
	generateEmployees()  
	print("Generating Logins...     ", end = "\r")	
	generateLogins() 
	# pprint.pprint(employees) 
	# pprint.pprint(logins)
	for x in range(5): # do this (max number of consecutive shifts) - 1 times. doesnt matter if you go over
		shiftCombine()
	print("Calculating...           ", end = "\r")
	calcList = calc()

	print("                         ", end = "\r")
	print(directions)
	exit = False
	while (not exit):
		inp = input("Enter Instruction: ")
		if(inp == "help"):
			print(directions)
		elif(inp == "calc"):
			print("Timecards Result:")
			for e in calcList:
				print(e)
		elif(inp == "end" or inp == ""):
			exit = True
		else:
			investigate(inp)
	deleteTempFiles()



def calc():
	calcList = []
	for employee in employees:
		for shift in employees[employee]:
			firstLogin = dt.strptime("23:59:59", '%H:%M:%S')
			lastLogout = dt.strptime("00:00:00", '%H:%M:%S')
			pid = employee.split()[-1]
			shiftDate = shift[0]
			start = dt.strptime(shift[1], '%H:%M:%S')
			end = dt.strptime(shift[2], '%H:%M:%S')
			app = ""

			inOnTime = False
			outOnTime = False
			cameIn = False

			for login in logins:
				logPid = login[0]
				logDate = login[1].split()[0]
				loginTime = dt.strptime(login[1].split()[1], '%H:%M:%S')
				logoutTime = dt.strptime(login[2].split()[1], '%H:%M:%S')


				if(pid == logPid and shiftDate == logDate):
				# right date and person
					if(loginTime < firstLogin):
						firstLogin = loginTime
					if(logoutTime > lastLogout):
						lastLogout = logoutTime

					if(loginTime <= start + timedelta(minutes = 6) and loginTime > start - timedelta(hours = 1)):
					# they showed up before their shift within 1 hour of starting
						inOnTime = True
					if(logoutTime >= end - timedelta(minutes = 5) and logoutTime < end + timedelta(hours = 1)):
					# they logged out on time within 1 hour of it ending
						outOnTime = True
					cameIn = True

			# convert 24 hour datetime into 12 hour string
			fls = firstLogin.strftime("%I:%M:%S %p")
			lls = lastLogout.strftime("%I:%M:%S %p")

			if(inOnTime and outOnTime and cameIn):
				app = f"{green}{pid}\t{shiftDate}\tGOOD{reset}"
			elif(outOnTime):
				app = f"{yellow}{pid}\t{shiftDate}\tLATE\tIN-{fls}{reset}"
			elif(inOnTime):
				app = f"{yellow}{pid}\t{shiftDate}\tEARL\tOUT-{lls}{reset}"
			elif(not cameIn):
				app = f"{red}{pid}\t{shiftDate}\tNONE{reset}"
			elif(not inOnTime and not outOnTime): # possible no show if they logged out before their shift started
				app = f"{yellow}{pid}\t{shiftDate}\tBOTH\tIN-{fls}\tOUT-{lls}{reset}"
			else: # something weird happened
				app = f"{purple}{pid}\t{shiftDate}\tINDT{reset}"
			calcList.append(app)

			# adds this shift to logs for investigate function
			startTime = start.strftime("%I:%M:%S %p")
			endTime = end.strftime("%I:%M:%S %p")
			inv.append(app + f"\n{blue}{startTime} | {endTime}{reset}")
			logs = getLogins(pid, shiftDate)
			for l in logs:
				inv.append(l)

		calcList.append(breakString)
	return calcList	
	
# creates the employees dictionary: name -> list of shifts
def generateEmployees():
	# Give the location of the file
	read_file = pd.read_excel(shiftsName)
	read_file.to_csv("Shifts.csv", index = None ,header=True)
	filename = 'Shifts.csv'
	# read csv file and create the employees datastructure
	with open(filename, 'r') as csvfile:
		datareader = csv.reader(csvfile)
		employee = ""
		for row in datareader:
			if("|" in row[0]):
			#this is the employee name
				employee = row[0].lower()
				employees[employee] = []
			elif("-" in row[0]):
			#this is the shift
				date = row[0].split()[0]
				#date without the time
				shift = [date, row[1], row[2]]
				employees[employee].append(shift)

# creates a list of all logins from student employees (converts MAC full names into PID)
def generateLogins():
	read_file = pd.read_excel(loginsName)
	read_file.to_csv("Logins.csv", index = None ,header=True)   
	filename = 'Logins.csv'

	with open(filename,"r") as source:
		rdr= csv.reader( source )
		with open("loginsPruned.csv","w") as result:
			wtr= csv.writer( result )
			for r in rdr:
				for key in employees:
					names = r[3].lower().split()
					if r[3].lower() in key:
						# this gets wonky with middle names
						pid = key.split()[-1]
						wtr.writerow((pid, r[4], r[5]))
					elif(len(names) > 1):
						if(names[0] in key and names[1] in key):
						# convert MAC names into PID
							pid = key.split()[-1]
							# print(names[0] + names[1] + " -> " + pid)
							wtr.writerow((pid, r[4], r[5]))
	# create datastructure from csv
	with open("loginsPruned.csv", "r") as csvfile:
		datareader = csv.reader(csvfile)
		for row in datareader:
			logins.append([row[0], row[1], row[2]])

def investigate(myPid):
	for e in inv:
		if(myPid in e):
		# this is the calc log for that shift
			print(breakString)
			print(e)
		for i in e:
			if(myPid in i):
				# this is the login for that day
				# convert to AM/PM times
				inTime = dt.strptime(e[1].split()[1], '%H:%M:%S').strftime("%I:%M:%S %p")
				outTime = dt.strptime(e[2].split()[1], '%H:%M:%S').strftime("%I:%M:%S %p")
				print(f"{inTime} | {outTime}")

def getLogins(myPid, date):
	ret = []
	for login in logins:
		logPid = login[0]
		logDate = login[1].split()[0]
		if(myPid in logPid and logDate == date):
			ret.append(login)
	# sort it by date
	ret.sort(key = lambda x: x[1])
	return ret

#combines shifts that happen back to back
def shiftCombine():
	for employee in employees:
		prevDate = [0, 0, 0]
		i = 0
		for date in employees[employee]:
		#Iterate through all shifts for each employee
			if(date[0] == prevDate[0] and prevDate[2] == date[1]):
			#if the shift started at the same time as the end of the previous combine them
				newDate = [date[0], prevDate[1], date[2]]
				employees.get(employee)[i] = newDate
				employees.get(employee).remove(prevDate)
			prevDate = date	
			i += 1

# delete temporary files
def deleteTempFiles():
	os.remove('Shifts.csv')
	os.remove('Logins.csv')
	os.remove('loginsPruned.csv')

if __name__ == '__main__':
	main()