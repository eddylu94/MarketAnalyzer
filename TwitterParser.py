import tweepy
import os
import csv
import sys

from TwitterParserAPI import api

#year-month-date
start_date = "2016-01-31"
end_date = "2017-01-01"

inputString = str(sys.argv[1])

match = 0
fullName = ""

with open('companies.csv', 'r') as companiesFile:
		reader = csv.reader(companiesFile)
		for row in reader:
			companyName = row[1]
			if inputString == companyName:
				match = 1
				fullName = companyName
				break		

if match == 0:
	print "Invalid company symbol"

else:

	symbol = inputString
	
	keyword = fullName
	#keyword = "$" + inputString

	if not os.path.exists(os.path.dirname('Twitter_Statuses/' + symbol + '_statuses.csv')):
	    		os.makedirs(os.path.dirname('Twitter_Statuses/' + symbol + '_statuses.csv'))

	with open('Twitter_Statuses/' + symbol + '_statuses.csv', 'w') as destination:
			writer = csv.writer(destination, delimiter = ',')

			for tweet in tweepy.Cursor(api.search, q=keyword, since=start_date, until=end_date, lang="en", limit=10).items():
			    writer.writerows([[tweet.text.encode('utf8')]])
			    print tweet.text.encode('utf8')
