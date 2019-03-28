#!/usr/bin/env python3
# Yegeon Seo
# CS265 Final Project

# This program takes a formatted schedule and convert / export it as ics file

import sys
import fileinput
import re
import random


# Read the file and pass it to different method as a parameter to get data
def readFile():
	contents = []

	for line in fileinput.input():
		file = line.split("\n")
		for word in file:
			contents.append(word.split(" "))

	# call helper functions to get class name and time.
	contents = simplify(contents)
	resClass = getClass(contents)
	resTime = getTime(contents)
	ical = formatical(resClass, resTime)

	return ical


# Export the data received from formatical function as ics file in the current directory
def export(ics):
	name = sys.argv[1] + ".ics"
	f = open(name, "w+")
	f.write(ics)
	f.close()


# takes class name and time to format ics file
def formatical(className, classTime):
	time = ""

	# This is a basic format that will be used later
	ical = "BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:-//Final Project//\nCALSCALE:GREGORIAN\nMETHOD:PUBLISH\nX-WR-TIMEZONE:America/New_York\nBEGIN:VTIMEZONE\nTZID:America/New_York\nX-LIC-LOCATION:America/New_York\nBEGIN:DAYLIGHT\nTZOFFSETFROM:-0500\nTZOFFSETTO:-0400\nTZNAME:EDT\nRRULE:FREQ=YEARLY;BYMONTH=3;BYDAY=2SU\nEND:DAYLIGHT\nBEGIN:STANDARD\nTZOFFSETFROM:-0400\nTZOFFSETTO:-0500\nTZNAME:EST\nDTSTART:19701101T020000\nRRULE:FREQ=YEARLY;BYMONTH=11;BYDAY=1SU\nEND:STANDARD\nEND:VTIMEZONE"

	# If class time is TBA, it's an online class, so remove it
	for i in range(0, len(classTime)):
		if classTime[i][0] == "TBA":
			className.pop(i)

	classTime = [sublist for sublist in classTime if sublist[0] != 'TBA']

	a = classTime[0][3].split(" ")

	# check the months and change it to numbers. Strings cannot be used for ics format
	# bmonth is the beginning (the month classes start)
	# emonth is the end (ending month)
	if a[0] == "Jan":
		bmonth = "01"
	elif a[0] == "Sep":
		bmonth = "09"
	elif a[0] == "Apr":
		bmonth = "04"
	elif a[0] == "Jun":
		bmonth = "06"

	if a[4] == "Mar":
		emonth = "03"
	elif a[4] == "Jun":
		emonth = "06"
	elif a[4] == "Sep":
		emonth = "09"
	elif a[4] == "Dec":
		emonth = "12"

	c = 0
	for lt in classTime:
		t = lt[0].split(" ")
		bhr = t[0].replace(":", "")
		ehr = t[3].replace(":", "")

		# change the time to ics format
		# bhr is starting time (the time classes start)
		# ehr is ending time (the time classes end)
		if t[1] == "am":
			if len(bhr) == 3:
				bhr = "0" + bhr + "00"
			else:
				bhr += "00"
		elif t[1] == "pm":
			if bhr == "1200":
				bhr += "00"
			else:
				bhr = (1200 + int(bhr))
				bhr = str(bhr) + "00"

		if t[4] == "am":
			if len(ehr) == 3:
				ehr = "0" + ehr + "00"
			else:
				ehr += "00"
		elif t[4] == "pm":
			if ehr == "1200" or ehr == "1220" or ehr == "1250":
				ehr += "00"
			else:
				ehr = (1200 + int(ehr))
				ehr = str(ehr) + "00"

		days = lt[1]
		day = list(days)

		# Change the days to ics format
		for l in range(0, len(day)):
			if day[l] == "M":
				day[l] = "MO"
			elif day[l] == "T":
				day[l] = "TU"
			elif day[l] == "W":
				day[l] = "WE"
			elif day[l] == "R":
				day[l] = "TH"
			elif day[l] == "F":
				day[l] = "FR"

		day = ",".join(day)

		# create a new ics format using the data extracted previously
		# Unique id is Class name + random integer ranged from 0 - 9999999
		time += "\nBEGIN:VEVENT\nDTSTART;TZID=America/New_York:" + a[2] + bmonth + a[1][:-1] + "T" + bhr + "\nDTEND;TZID=America/New_York:" + a[2] + bmonth + a[1][:-1] + "T" + ehr + "\nRRULE:FREQ=WEEKLY;UNTIL=" + a[2] + emonth + a[5][:-1] + "T035959Z" + ";BYDAY=" + day + "\nDTSTAMP:20190319T220010Z\nUID:" + className[c] + str(random.randint(0, 9999999)) + "\nLOCATION:" + lt[2] + "\nSEQUENCE:0\nSTATUS:CONFIRMED\nSUMMARY:" + className[c] + "\nTRANSP:OPAQUE\nEND:VEVENT"

		c += 1

	# after finishing formatting, append it to the pre-made format before and return it
	ical += time + "\nEND:VCALENDAR"

	return ical


# function to remove not important data
def simplify(contents):
	lineCount = 0
	for line in contents:
		if line == ['']:
			contents.remove(contents[lineCount])
		lineCount += 1
	return contents


# get the class name
def getClass(contents):
	count = 0
	resClass = []

	# Because the inputs are formatted, I can find a specific word to locate where the classes are
	for line in contents:

		# If classes are located, trim the list to get wanted data only
		# and append it to a different list
		if line[0] == "Associated":
			className = contents[count-1]
			className.pop()
			className.pop()

			counter = 0
			for word in className:
				if word == "-":
					temp = []
					temp.append(className[counter + 1])
					temp.append(className[counter + 2])
					r = ''.join(temp)
					resClass.append(r)
				counter += 1
		count += 1

	count = 0

	# EXAM courses (EXAM080, etc) contain weird strings such as I-, II-, and III-.
	# use regex to find and remove them
	for word in resClass:
		if re.match("^EXAM.*$", word):
			resClass.pop(count - 1)
		count += 1

	return resClass


# get the time and dates for each class
def getTime(contents):
	time = []

	count = 0

	# Like before, input is formatted so I can locate a specific word to find the data I want
	for line in contents:

		# If string is found, trim the data and append it to a different list
		# then return it
		if re.search("Class*", line[0]):
			temp = " ".join(line)
			temp = temp.split("\t")
			temp.pop(0)
			temp.pop()
			time.append(temp)
		count += 1
	return time


# Tests if an argument is passed
def testArg():
	if len(sys.argv) < 2:
		print("No arguments passed. Exiting:")
		exit()


# Driver method
if __name__ == "__main__":
	testArg()
	ical = readFile()
	export(ical)


