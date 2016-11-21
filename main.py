import db_initial
import incident_generator_class

__dateFormat = datetime.datetime.now().strftime("%b").upper() + "_" + str(datetime.datetime.now().year % 100)

def testDB():
	assert db_initial.downloadAndConvertFile("http://www.rpi.edu/dept/public_safety/blotter/{fn}.pdf".format(fn = __dateFormat)) == 0
    	assert db_initial.createDatabase() == 0
    	assert db_initial.dumpJSON() == 0

def main():
	testDB()
	db_initial.runDB()

if __name__ == "__main__":
    main()