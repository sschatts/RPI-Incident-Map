import urllib2, sys, subprocess, os, datetime

date_format = datetime.datetime.now().strftime("%b").upper() + "_" + str(datetime.datetime.now().year % 100)

def main():
    	download_file("http://www.rpi.edu/dept/public_safety/blotter/{fn}.pdf".format(fn = date_format))
    	parse_file()

def download_file(download_url):
    response = urllib2.urlopen(download_url)
    file = open("{fn}.pdf".format(fn = date_format), 'wb')
    file.write(response.read())
    file.close()
    print("Completed")

def parse_file():
	os.system('gs -sDEVICE=txtwrite -o ./output.txt ./{fn}.pdf 1> /dev/null'.format(fn = date_format))

if __name__ == "__main__":
    main()