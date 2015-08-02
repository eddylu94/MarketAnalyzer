import tweepy
import os
import csv
import sys

inputString = str(sys.argv[1])

match = 0

with open('companies.csv', 'r') as companiesFile:
		reader = csv.reader(companiesFile)
		for row in reader:
			companyName = row[1]
			if inputString == companyName:
				match = 1
				break	

if match == 0:
	print "Invalid company symbol"

else:

	symbol = inputString
	keyword = "$" + inputString

	writer = open('Twitter_Statuses/' + symbol + '_filtered.txt', 'w')

	with open('Twitter_Statuses/' + symbol + '_statuses.csv', 'r') as companyStatuses:
		reader = csv.reader(companyStatuses)
		for cell in reader:
			tempCell = cell[0].split()
			for word in tempCell:
				if (not 'http'in word) and (not '$' in word) and (not '@'in word) and (not 'RT'in word):
					writer.write(word + '\n')
	
	writer.close()