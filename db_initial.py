import urllib2, sys, subprocess, os, datetime, re, geocoder, json, pytest
from pymongo import MongoClient
from mapbox import Geocoder
from bson import Binary, Code, json_util
from bson.json_util import dumps

#Since Pub Safe uses the first three letters of the month (capitalized) followed by an _ and then the last two digits of the year for the .pdf naming convention. I use __dateFormat to hold that string
__dateFormat = datetime.datetime.now().strftime("%b").upper() + "_" + str(datetime.datetime.now().year % 100)

#Connect to the proper set of posts in the incident database's collection.
__connection = MongoClient()
__db = __connection['incident-db']
__collection = __db['incident-collection']
__posts = __db.posts

#Download the .pdf for the current month from Pub Safe by opening the URL and dumping it into a PDF. Then use Ghost Script (gs) to convert it to a text file
def downloadAndConvertFile(download_url):
    response = urllib2.urlopen(download_url)
    file = open("{fn}.pdf".format(fn = __dateFormat), 'wb')
    file.write(response.read())
    file.close()

    os.system('gs -sDEVICE=txtwrite -o ./{fn}.txt ./{fn}.pdf 1> /dev/null'.format(fn = __dateFormat))

    return 0

def createDatabase():
	file = open("{fn}.txt".format(fn = __dateFormat), 'r')
	reportNum = []; dateReported = []; location = []; eventNum = []; dateTimeFromTo = []; incident = [];  disposition = []; coords = []; month = "";
	seenDisposition = False

	for line in file: #for every line in the text file
		#Every if statement uses regular expressions to locate the desired field and then records whatever comes after the field up to where the question mark is (or the end of the line if not question mark)
		#Basically, if what it finds isn't null then write what it (it being re.findall()) finds to a variable
		if re.findall(r'date reported:.* (?=location)', line):
			dateReported = ''.join(re.findall(r'date reported:.* (?=location)', line))
			dateReported = dateReported.replace('date reported:','').strip().rstrip()
			month = dateReported[:2]
			#print dateReported

		if re.findall(r'location :.* (?=event)', line):
			location = ''.join(re.findall(r'location :.* (?=event)', line))
			location = location.replace('location :','').strip()
			#Using the location's name, use Google's API to find it's latitude and longitude
			#response = geocoder.mapbox("{loc}, Troy, New York 12180, United States".format(loc = location))
			#coords = response.latlng
			geocoder = Geocoder(access_token='pk.eyJ1Ijoic3NjaGF0dHMiLCJhIjoiY2l1NDdib3N1MGl2MTJwbGhycnNqNGYxciJ9.uCMQ9n7xQCjRvRMnmFrLrw')
			response = geocoder.forward("{loc}, Troy, New York 12180, United States".format(loc = location))
			first = response.geojson()['features'][0]
			coords = [first['geometry']['coordinates'][1], first['geometry']['coordinates'][0]]
			print coords
			#print location

		if re.findall(r'event #:.*', line):
			eventNum = ''.join(re.findall(r'event #:.*', line))
			eventNum = eventNum.replace('event #:','').strip().rstrip()
			#print eventNum

		if re.findall(r'date and time occurred from - occurred to:.*', line):
			dateTimeFromTo = ''.join(re.findall(r'date and time occurred from - occurred to:.*', line))
			dateTimeFromTo = dateTimeFromTo.replace('date and time occurred from - occurred to:','').strip().rstrip()
			#print dateTimeFromTo

		if re.findall(r'incident :.* (?=report #:)', line):
			incident = ''.join(re.findall(r'incident :.* (?=report #:)', line))
			incident = incident.replace('incident :','').strip()
			#print incident

		if re.findall(r'report #:.*', line):
			reportNum = ''.join(re.findall(r'report #:.*', line))
			reportNum = reportNum.replace('report #:','').strip()
			#print reportNum

		if re.findall(r'disposition:.*', line):
			disposition = ''.join(re.findall(r'disposition:.*', line))
			disposition = disposition.replace('disposition: :','').strip().rstrip()
			seenDisposition = True
			#print disposition

		if seenDisposition:
			#write the formatted information into a properly formatted post for the MongoDB
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

def dumpJSON():
	f = open("{fn}.json".format(fn = __dateFormat), "w+")
    	docsList = list(__posts.find())
    	jsonDocs = json.dumps(docsList, default=json_util.default, indent=4, separators=(',', ': '))
    	f.write(jsonDocs)
    	f.close()
    	return 0

def filename():
	year = datetime.datetime.now().year
	month = datetime.datetime.now().month
	filename = __dateFormat
	desireable = {(month, year) : "{fn}.json".format(fn=filename)}
	return desireable

def testDB():
	assert downloadAndConvertFile("http://www.rpi.edu/dept/public_safety/blotter/{fn}.pdf".format(fn = __dateFormat)) == 0
    	assert createDatabase() == 0
    	assert dumpJSON() == 0
    	#assert isinstance(filename(), str)

def runDB():
	#print __dateFormat
	result = __posts.delete_many({})
	#print result.deleted_count
    	downloadAndConvertFile("http://www.rpi.edu/dept/public_safety/blotter/{fn}.pdf".format(fn = __dateFormat))
    	createDatabase()
    	dumpJSON()
    	#print filename()