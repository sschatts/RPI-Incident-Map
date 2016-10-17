import urllib2, sys, subprocess, os, datetime

#gs -sDEVICE=txtwrite -o output.txt 2015.pdf

def main():
    	download_file("http://www.rpi.edu/dept/public_safety/blotter/{ab}_16.pdf".format(ab = datetime.datetime.now().strftime("%b").upper()))
    	parse_file()

def download_file(download_url):
    response = urllib2.urlopen(download_url)
    file = open("document.pdf", 'wb')
    file.write(response.read())
    file.close()
    print("Completed")

def parse_file():
	#args = ['gs', '-dSAFER', '-dNOPAUSE', '-dBATCH', '-sDEVICE=txtwrite', '-sOutputFile=output.txt', 'document.pdf']
	#output = Popen(args, stdout = sys.stdout, stderr = sys.stderr)
	os.system('gs -sDEVICE=txtwrite -o ./output.txt ./document.pdf 1> /dev/null')
if __name__ == "__main__":
    main()