#Initializes the database by downloading/converting files from Pub Safe and then populating the database with the extracted information. It then dumps the JSON from the database for use by incident_generator_class.py.
#Written for RPI Incident Map

import urllib2, sys, subprocess, os, datetime, re, geocoder, json, pytest, urlparse, lxml.html
from pymongo import MongoClient
from mapbox import Geocoder
from bson import Binary, Code, json_util
from bson.json_util import dumps

#Since Pub Safe uses the first three letters of the month (capitalized) followed by an _ and then the last two digits of the year for the .pdf naming convention. I use __dateFormat to hold that string for the current month
__dateFormat = datetime.datetime.now().strftime("%b").upper() + "_" + str(datetime.datetime.now().year % 100)

#Connect to the proper set of posts in the incident database's collection.
__connection = MongoClient()
__db = __connection['incident-db']
__collection = __db['incident-collection']
__posts = __db.posts

#Download the .pdf for the current month from Pub Safe by opening the URL and dumping it into a PDF. Then use Ghost Script (gs) to convert it to a text file
def downloadAndConvertFile(download_url):
	filePath = download_url.replace("http://www.rpi.edu/dept/public_safety/blotter/", "").replace(".pdf", "")
	response = urllib2.urlopen(download_url)
	file = open("./pdfs/{fp}.pdf".format(fp = filePath), 'wb')
	file.write(response.read())
	file.close()

	os.system('gs -sDEVICE=txtwrite -o ./pdfs/{fp}.txt ./pdfs/{fp}.pdf 1> /dev/null'.format(fp = filePath))

	return 0

def aquireBacklog():
	#The url of the page you want to scrape
	baseURL = 'http://www.rpi.edu/dept/public_safety/blotter/'

	#Fetch the page
	res = urllib2.urlopen(baseURL)

	#Parse the response into an xml tree
	tree = lxml.html.fromstring(res.read())

	#Construct a namespace dictionary to pass to the xpath() call
	#This lets us use regular expressions in the xpath
	ns = {'re': 'http://exslt.org/regular-expressions'}

	#Iterate over all <a> tags whose href ends in ".pdf" (case-insensitive)
	for node in tree.xpath('//a[re:test(@href, "\.pdf$", "i")]', namespaces=ns):
		#Save the href, joining it to the baseURL as well as the file name to check and see if it exists
		scrapedURL = urlparse.urljoin(baseURL, node.attrib['href'])
		fileName = node.attrib['href']
		if not os.path.exists('./pdfs/{fp}'.format(fp = fileName)):
			downloadAndConvertFile(scrapedURL)

	return 0

def createDatabase():
	file = open("./pdfs/{fn}.txt".format(fn = __dateFormat), 'r')
	reportNum = []; dateReported = []; location = []; eventNum = []; dateTimeFromTo = []; incident = [];  disposition = []; coords = []; month = "";
	seenDisposition = False

	for line in file: #For every line in the text file
		#Every if statement uses regular expressions to locate the desired field and then records whatever comes after the field up to where the question mark is (or the end of the line if not question mark)
		#Basically, if what it finds isn't null then write what it (it being re.findall()) finds to a variable
		if re.findall(r'date reported:.* (?=location)', line):
			dateReported = ''.join(re.findall(r'date reported:.* (?=location)', line))
			dateReported = dateReported.replace('date reported:','').strip().rstrip()
			month = dateReported[:2]

		if re.findall(r'location :.* (?=event)', line):
			location = ''.join(re.findall(r'location :.* (?=event)', line))
			location = location.replace('location :','').strip()

			#Using the location's name, use Mapbox's API to find it's latitude and longitude
			geocoder = Geocoder(access_token='pk.eyJ1Ijoic3NjaGF0dHMiLCJhIjoiY2l1NDdib3N1MGl2MTJwbGhycnNqNGYxciJ9.uCMQ9n7xQCjRvRMnmFrLrw')
			response = geocoder.forward("{loc}, Troy, New York 12180, United States".format(loc = location))
			first = response.geojson()['features'][0]
			coords = [first['geometry']['coordinates'][1], first['geometry']['coordinates'][0]]

		if re.findall(r'event #:.*', line):
			eventNum = ''.join(re.findall(r'event #:.*', line))
			eventNum = eventNum.replace('event #:','').strip().rstrip()

		if re.findall(r'date and time occurred from - occurred to:.*', line):
			dateTimeFromTo = ''.join(re.findall(r'date and time occurred from - occurred to:.*', line))
			dateTimeFromTo = dateTimeFromTo.replace('date and time occurred from - occurred to:','').strip().rstrip()

		if re.findall(r'incident :.* (?=report #:)', line):
			incident = ''.join(re.findall(r'incident :.* (?=report #:)', line))
			incident = incident.replace('incident :','').strip()

		if re.findall(r'report #:.*', line):
			reportNum = ''.join(re.findall(r'report #:.*', line))
			reportNum = reportNum.replace('report #:','').strip()

		if re.findall(r'disposition:.*', line):
			disposition = ''.join(re.findall(r'disposition:.*', line))
			disposition = disposition.replace('disposition: :','').strip().rstrip()
			seenDisposition = True

		if seenDisposition:
			#Write the formatted information into a properly formatted post for the MongoDB
			post = {"date reported": dateReported,
					 "month": month,
					 "location": location,
					 "event #": eventNum,
					 "date and time occurred from to occurred to": dateTimeFromTo,
					 "incident": incident,
					 "report #": reportNum,
					 "disposition": disposition,
					 "coordinates": coords}
			#Insert the post into the database's collection's posts
			__posts.insert(post)
			seenDisposition = False

	return 0

#Dumps the posts from the database collection into a json file named with the month and year i.e. NOV_16
def dumpJSON():
	f = open("{fn}.json".format(fn = __dateFormat), "w+")
	#Gets a list of all of the posts that are in the database. Each post is an incident.
    	docsList = list(__posts.find())
    	#Creates a dump of the posts.
    	jsonDocs = json.dumps(docsList, default=json_util.default, indent=4, separators=(',', ': '))
    	#Writes the dumps to a JSON file
    	f.write(jsonDocs)
    	f.close()
    	return 0

#Returns the filename of the JSON created in the function above along with the month and year in number, number tuple. Needed for part of Kit's code.
def filename():
	year = datetime.datetime.now().year
	month = datetime.datetime.now().month
	filename = __dateFormat
	desireable = {(month, year) : "{fn}.json".format(fn=filename)}
	return desireable

#Assert statements to test that all functions run and return the proper result
def testDB():
	assert runDB() == 0
	assert downloadAndConvertFile("http://www.rpi.edu/dept/public_safety/blotter/{fn}.pdf".format(fn = __dateFormat)) == 0
    	assert createDatabase() == 0
    	assert dumpJSON() == 0
    	#assert aquireBacklog() == 0
    	assert isinstance(filename(), dict)

#How another file can populate the database and dump the JSON
def runDB():
	newpath = r'./pdfs'
	if not os.path.exists(newpath):
		os.makedirs(newpath)

	aquireBacklog()
	downloadAndConvertFile("http://www.rpi.edu/dept/public_safety/blotter/{fn}.pdf".format(fn = __dateFormat))
	createDatabase()
	dumpJSON()
	return 0

# if __name__ == "__main__":
# 	runDB()