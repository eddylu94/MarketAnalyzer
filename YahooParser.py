import csv
import urllib
import time
import os

# transfers company information from Yahoo! to .CSV
def writeCompanyInfo():

	url = 'http://ichart.finance.yahoo.com/table.csv?s=' + symbol + '&a=0&b=1&c=2010&d=0&e=1&f=2015&g=d&ignore=.csv'

	response = urllib.urlopen(url)
	responseText = csv.reader(response)

	if not os.path.exists(os.path.dirname('Yahoo_Files/' + symbol + '.csv')):
    		os.makedirs(os.path.dirname('Yahoo_Files/' + symbol + '.csv'))

	with open('Yahoo_Files/' + symbol + '.csv', 'w') as destination:
		writer = csv.writer(destination, delimiter = ',')
		for row in responseText:
			writer.writerows([row])

# create .CSV of percent changes for companies
def writePercentChanges():

	with open('Yahoo_Files/' + symbol + '.csv', 'r') as companyInfo:
		reader = csv.reader(companyInfo)
		row0 = next(reader)
		row1 = next(reader)
		current = float(row1[6])

		if not os.path.exists(os.path.dirname('Yahoo_Files/' + symbol + '_percent.csv')):
    			os.makedirs(os.path.dirname('Yahoo_Files/' + symbol + '_percent.csv'))
		
		with open('Yahoo_Files/' + symbol + '_percent.csv', 'w') as destination:

			writer = csv.writer(destination, delimiter = ',')

			for row in reader:
			
				previous = current
				current = float(row[6])
				percentChange = ((current - previous) / current) * 100
				if abs(percentChange) < 5:
					comment = 'no'
				elif percentChange > 0:
					comment = 'YES   <-- SIGNIFICANT INCREASE'
				elif percentChange < 0:
					comment = 'YES   <-- SIGNIFICANT DECREASE'
				percentChange_str = str(round(percentChange, 3))
				date = row[0]
			
				writer.writerows([[date, percentChange_str, comment]])

# create two .CSVs of significant changes for increasing and decreasing
def listSignificant():

	if not os.path.exists(os.path.dirname('Yahoo_Significant/' + symbol + '_increase.csv')):
    		os.makedirs(os.path.dirname('Yahoo_Significant/' + symbol + '_increase.csv'))

	if not os.path.exists(os.path.dirname('Yahoo_Significant/' + symbol + '_decrease.csv')):
    		os.makedirs(os.path.dirname('Yahoo_Significant/' + symbol + '_decrease.csv'))

	writer_increase = open('Yahoo_Significant/' + symbol + '_increase.txt', 'w')
	writer_decrease = open('Yahoo_Significant/' + symbol + '_decrease.txt', 'w')
	
	with open('Yahoo_Files/' + symbol + '_percent.csv', 'r') as companyPercents:
		reader = csv.reader(companyPercents)

		for row in reader:
			if 'INCREASE' in row[2]:
				writer_increase.write(row[0] + '\n')
			elif 'DECREASE' in row[2]:
				writer_decrease.write(row[0] + '\n')

	writer_increase.close()
	writer_decrease.close()

# open CSV list of companies
def main():

	global symbol

	start_time = time.time()

	# writing company info
	print '\nWriting company information to SYMBOL.csv...\n'
	with open('companies.csv', 'r') as companiesFile:
		reader = csv.reader(companiesFile)
		counter = 1
		for row in reader:
			companyName = row[0]
			while len(companyName) < 19:
				companyName += ' '
			symbol = row[1]
			writeCompanyInfo()
			print 'Writing information... \t' + companyName + '\t' + row[1] + '\t   ' + str(counter) + ' of 30   \t' + str(round(counter / 30.0 * 100, 1)) + ' %'
			counter = counter + 1

	# writing percent changes
	print '\nWriting percent changes to SYMBOL_percent.csv...\n'
	with open('companies.csv', 'r') as companiesFile:
		reader = csv.reader(companiesFile)
		counter = 1
		for row in reader:
			companyName = row[0]
			while len(companyName) < 19:
				companyName += ' '
			symbol = row[1]
			writePercentChanges()
			print 'Writing percentages... \t' + companyName + '\t' + row[1] + '\t   ' + str(counter) + ' of 30   \t' + str(round(counter / 30.0 * 100, 1)) + ' %'
			counter = counter + 1

	# writing percent changes
	print '\nListing significant percent changes to SYMBOL_increase.csv and SYMBOL_decrease...\n'
	with open('companies.csv', 'r') as companiesFile:
		reader = csv.reader(companiesFile)
		counter = 1
		for row in reader:
			companyName = row[0]
			while len(companyName) < 19:
				companyName += ' '
			symbol = row[1]
			listSignificant()
			print 'Listing significant... \t' + companyName + '\t' + row[1] + '\t   ' + str(counter) + ' of 30   \t' + str(round(counter / 30.0 * 100, 1)) + ' %'
			counter = counter + 1

	end_time = time.time()

	minutes = int( (end_time - start_time) / 60 )
	seconds = int( (end_time - start_time) % 60 )
	milliseconds = int ((end_time - start_time) * 1000) % 1000

	print '\nCompletion time:   ' + str(minutes) + ' min ' + str(seconds) + ' secs ' + str(milliseconds) + ' ms\n'

# entry point of program
main()