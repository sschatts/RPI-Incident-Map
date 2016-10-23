import urllib2, sys, subprocess, os, datetime, re
from pymongo import MongoClient

__date_format = datetime.datetime.now().strftime("%b").upper() + "_" + str(datetime.datetime.now().year % 100)
__connection = MongoClient()
__db = __connection['incident-db']
__collection = __db['incident-collection']
__posts = __db.posts

def download_and_convert_file(download_url):
    response = urllib2.urlopen(download_url)
    file = open("{fn}.pdf".format(fn = __date_format), 'wb')
    file.write(response.read())
    file.close()

    os.system('gs -sDEVICE=txtwrite -o ./{fn}.txt ./{fn}.pdf 1> /dev/null'.format(fn = __date_format))

    print("Completed")

def parse_text():
	file = open("{fn}.txt".format(fn = __date_format), 'r')
	report_num = []; date_reported = []; location = []; event_num = []; datetime_fromto = []; incident = [];  report_num = []; disposition = []

	for line in file:
		if re.findall(r'date reported:.* (?=location)', line):
			date_reported = ''.join(re.findall(r'date reported:.* (?=location)', line))
			#print date_reported

		if re.findall(r'location :.* (?=event)', line):
			location = ''.join(re.findall(r'location :.* (?=event)', line))
			#print location

		if re.findall(r'event #:.*', line):
			event_num = ''.join(re.findall(r'event #:.*', line))
			#print event_num

		if re.findall(r'date and time occurred from - occurred to:.*', line):
			datetime_fromto = ''.join(re.findall(r'date and time occurred from - occurred to:.*', line))
			#print datetime_fromto

		if re.findall(r'incident :.* (?=report #:)', line):
			incident = ''.join(re.findall(r'incident :.* (?=report #:)', line))
			#print incident

		if re.findall(r'report #:.*', line):
			report_num = ''.join(re.findall(r'report #:.*', line))
			#print report_num

		if re.findall(r'disposition:.*', line):
			disposition = ''.join(re.findall(r'disposition:.*', line))
			#print disposition

		if date_reported and location and event_num and datetime_fromto and incident and report_num and disposition:
			date_reported = date_reported.replace('date reported:','').strip()
			location = location.replace('location :','').strip()
			event_num = event_num.replace('event #:','').strip()
			datetime_fromto = datetime_fromto.replace('date and time occurred from - occurred to:','').strip()
			incident = incident.replace('incident :','').strip()
			report_num = report_num.replace('report #:','').strip()
			disposition = disposition.replace('disposition: :','').strip()

			post = {"date reported": date_reported,
					 "location": location,
					 "event #": event_num,
					 "date and time occurred from to occurred to": datetime_fromto,
					 "incident": incident,
					 "report #": report_num,
					 "disposition": disposition}
			__posts.insert(post)

			# print repr(date_reported)
			# print repr(location)
			# print repr(event_num)
			# print repr(datetime_fromto)
			# print repr(incident)
			# print repr(report_num)
			# print repr(disposition)




def main():
    	download_and_convert_file("http://www.rpi.edu/dept/public_safety/blotter/{fn}.pdf".format(fn = __date_format))
    	parse_text()

    	# for post in __posts.find():
    	# 	print post

if __name__ == "__main__":
    main()