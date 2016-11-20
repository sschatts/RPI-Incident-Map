import urllib2, sys, subprocess, os, datetime, re, geocoder, json, pytest
from pymongo import MongoClient
from mapbox import Geocoder
from bson import Binary, Code, json_util
from bson.json_util import dumps

#import location
#import incident
#import incident_cache

#TODO: How to make this work with multiple PDFs
#TODO: Add to the database instead of recreate it every time
#TODO: Have this run continuously instead of just once

#Since Pub Safe uses the first three letters of the month (capitalized) followed by an _ and then the last two digits of the year for the .pdf naming convention. I use __date_format to hold that string
__date_format = datetime.datetime.now().strftime("%b").upper() + "_" + str(datetime.datetime.now().year % 100)
#__date_format = "OCT_16"

#Connect to the proper set of posts in the incident database's collection.
__connection = MongoClient()
__db = __connection['incident-db']
__collection = __db['incident-collection']
__posts = __db.posts

#Download the .pdf for the current month from Pub Safe by opening the URL and dumping it into a PDF. Then use Ghost Script (gs) to convert it to a text file
def downloadAndConvertFile(download_url):
    response = urllib2.urlopen(download_url)
    file = open("{fn}.pdf".format(fn = __date_format), 'wb')
    file.write(response.read())
    file.close()

    os.system('gs -sDEVICE=txtwrite -o ./{fn}.txt ./{fn}.pdf 1> /dev/null'.format(fn = __date_format))

    return 0

    #print("Completed")

def createDatabase(incid_cache):
	file = open("{fn}.txt".format(fn = __date_format), 'r')
	report_num = []; date_reported = []; location = []; event_num = []; datetime_fromto = []; incident = [];  report_num = []; disposition = []; coords = [];
	seen_disposition = False

	for line in file: #for every line in the text file
		#Every if statement uses regular expressions to locate the desired field and then records whatever comes after the field up to where the question mark is (or the end of the line if not question mark)
		#Basically, if what it finds isn't null then write what it (it being re.findall()) finds to a variable
		if re.findall(r'date reported:.* (?=location)', line):
			date_reported = ''.join(re.findall(r'date reported:.* (?=location)', line))
			date_reported = date_reported.replace('date reported:','').strip().rstrip()
			#print date_reported

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
			event_num = ''.join(re.findall(r'event #:.*', line))
			event_num = event_num.replace('event #:','').strip().rstrip()
			#print event_num

		if re.findall(r'date and time occurred from - occurred to:.*', line):
			datetime_fromto = ''.join(re.findall(r'date and time occurred from - occurred to:.*', line))
			datetime_fromto = datetime_fromto.replace('date and time occurred from - occurred to:','').strip().rstrip()
			#print datetime_fromto

		if re.findall(r'incident :.* (?=report #:)', line):
			incident = ''.join(re.findall(r'incident :.* (?=report #:)', line))
			incident = incident.replace('incident :','').strip()
			#print incident

		if re.findall(r'report #:.*', line):
			report_num = ''.join(re.findall(r'report #:.*', line))
			report_num = report_num.replace('report #:','').strip()
			#print report_num

		if re.findall(r'disposition:.*', line):
			disposition = ''.join(re.findall(r'disposition:.*', line))
			disposition = disposition.replace('disposition: :','').strip().rstrip()
			seen_disposition = True
			#print disposition

		if seen_disposition:
			month = date_reported[:2]


			#print str(coords) + ":" + location + ":" + incident
			#print coords

			#write the formatted information into a properly formatted post for the MongoDB
			post = {"date reported": date_reported,
					 "month": month,
					 "location": location,
					 "event #": event_num,
					 "date and time occurred from to occurred to": datetime_fromto,
					 "incident": incident,
					 "report #": report_num,
					 "disposition": disposition,
					 "coordinates": coords}
			#Insert the post into the database's collection's posts
			__posts.insert(post)

			#l = Location(location, coords)
			#i = Incident(event_num, event_type, l, disposition)
			#i_cache.insertIncident(i)
			seen_disposition = False

	return 0

def dumpJSON():
	f = open("{fn}.json".format(fn = __date_format), "w+")
    	docs_list = list(__posts.find())
    	json_docs = json.dumps(docs_list, default=json_util.default, indent=4, separators=(',', ': '))
    	f.write(json_docs)
    	f.close()
    	return 0

def filename():
	year = datetime.datetime.now().year
	month = datetime.datetime.now().month
	filename = __date_format
	desireable = [((month, year), "{fn}".format(fn=filename))]
	return desireable

def test_db():
	assert downloadAndConvertFile("http://www.rpi.edu/dept/public_safety/blotter/{fn}.pdf".format(fn = __date_format)) == 0
    	assert createDatabase(None) == 0
    	assert dumpJSON() == 0

def main():
	print __date_format
	result = __posts.delete_many({})
	print result.deleted_count
    	downloadAndConvertFile("http://www.rpi.edu/dept/public_safety/blotter/{fn}.pdf".format(fn = __date_format))
	#cache = IncidentCache()
    	#cache = create_database_and_cache(cache)
    	createDatabase(None)
    	# for post in __posts.find():
    	# 	print post
    	dumpJSON()
    	print filename()

if __name__ == "__main__":
    main()