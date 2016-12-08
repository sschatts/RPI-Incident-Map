#classes centered around processing data taken from the database JSON, storing it, and wriitng it to a JSON for the front end to parse
#written for RPI Incident Map

import sys
import json
import os
#import pytest
#import db_initial
from datetime import date
from datetime import time
import calendar

#class to hold location information within the Incident Class
#initilization requires a location name (building or street) and the appropriate location grouping
class Location:
    def __init__(self, name, group):
        self.lat = 42.730 #default coordinates to be used if none found, center of campus
        self.long = -73.681 #default coordinates to be used if none found, center of campus
        self.locationName = name #building or street name
        self.locationGroup = group #pre-determined region of campus

    def setCoords(self, _lat, _long):
        self.lat = _lat
        self.long = _long


class IncidentData:
    def __init__(self):
        self.__categories = ["Mischief"," Fire Alarm", "Medical Incident", "Intoxication","Property Damage","Larceny and Assault"]

    def getCat(self, description):
        descCategory = ""
        #find matching description for incident type
        while (descCategory != "" and (i < len(self.__categories) ) ):
            if (description.upper() in self.__categories[i].upper()):
                descCategory = descCategory + self.__categories[i]

        #if no description matches, use other
        if (descCategory == ""):
            descCategory == "Other"

        return descCategory

#Incident class to hold information for filtering/displaying individual incidents
#initialization requires strings for eventNum and incidentType, a location object, and date objects for dateReported and dateOccurred
class Incident:
    def __init__(self, _eventNum, _incidentType, _location, _dateOccurred, _dateReported):
        self.eventNum = _eventNum #string
        self.incidentType = _incidentType #string
        self.location = _location #location description

        ##just use python built-in date objects for these::
        self.dateReported = _dateReported #datetime.date
        self.dateOccurred = _dateOccurred #datetime.date

#LocationData class for storing data used for populating Location objects for use within an Incident object
#known, static set of buildings and landmarks are grouped into location groups based on subjective campus significance, hence the hard-coding
class LocationData():
    def __init__(self):

        self.__north = {"GYMNASIUM, '87", "CAMPUS PARKING, NORTH LOT", "E-COMPLEX", "COLONIE APARTMENTS", "HEFFNER ALUMNI HOUSE", "J-BUILDING", "SAGE AVENUE", "BLITMAN RESIDENCE COMMONS", "COLONIE APTS., BUILDING A"}

        self.__east = {"EAST CAMPUS ATHLETIC VILLAGE", "HOUSTON FIELD HOUSE", "BURDETT AVENUE RESIDENCE", "DAVISON HALL", "NASON HALL", "CROCKETT HALL", "BARTON HALL", "RENSSELAER UNION", "BRAY HALL" "RAHPS - ALBRIGHT", "RAHPS-B", "COMMONS DINING HALL (FRES", "COMMONS PARKING", "SPORTS CENTER AND ROBISON", "MUELLER CENTER", "QUADRANGLE DORMS", "DEPARTMENT OF PUBLIC SAFETY", "NED HARKNESS ATHLETIC FIE", "STACWYCK - MCGIFFERT", "Sherry Road", "BRYCKWYCK APARTMENTS", "WARREN HALL", "CARY HALL", "BRINSMADE TERRACE", "Sharp Hall", "RENSSELAER CRITICAL FACIL", "NUGENT HALL", "STACWYCK-ROUSSEAU", "STACWYCK - WILTSIE", "PUBLIC SAFETY OFFICE", "H- BUILDING"}
        self.__off = {"OTHER OFF-CAMPUS LOCATION", "BEMAN LANE", "SHERRY ROAD"}
        self.__west = {"POLYTECH APARTMENTS", "CITY STATION", "CAMPUS PARKING, WEST LOT", "EMPAC BUILDING", "WEST HALL"}
        self.__south = {"MOE'S SOUTHWEST GRILL"}
        self.__academic = {"RUSSELL SAGE LABORATORY", "COGSWELL LABORATORY", "GREENE BUILDING", "JONSSON ENGINEERING CENTE", "ACADEMY HALL", "BIOTECH"}
        self.__defaultGroup = "RPI"

    def locationGroup(self, loc):
        if(loc in self.__north): return "North"
        elif(loc in self.__off): return "Off Campus"
        elif(loc in self.__west): return "West"
        elif(loc in self.__south): return "South"
        elif(loc in self.__east): return "East"
        elif(loc in self.__academic): return "Academic"
        else:
            return self.__defaultGroup

#JsontoIncident class uses a given (or default) date range to select an approprite set of month/year tagged JSON files to create
#a list of incident objects
class JsonToIncident:
    def __init__(self):
        self.__beginDate = date(date.today().year, date.today().month, 1)
        days_in_month = calendar.monthrange(date.today().year, date.today().month)
        days_in_month = days_in_month[1]
        self.__endDate = date(date.today().year, date.today().month, days_in_month)

        self.__locationData = LocationData()
        self.__jsonFiles = {(): ""}
        self.__incidentData = IncidentData()

    #assign filename for newest month using (month, year), "filename"} if entry not already present for more recent month
    def addJsonFile(self, file):
        if ((date.today().month, date.today().year) not in self.__jsonFiles):
            self.__jsonFiles[(date.today().month, date.today().year)] = file
        return 0

    def setJsonFiles(self, jfiles):
        self.__jsonFiles = jfiles

    #returns list of dictionaries for months matching date range
    def __getJsonDic(self):
        jsonDicList = [] #list of dictionaries with all json files of specified date range

        m = self.__beginDate.month
        y = self.__beginDate.year
        #print(self.__jsonFiles)
        while (y <= date.today().year):
            timePair = (m, y)
            print(str(self.__beginDate) + "\n")
            print(str(self.__endDate) + "\n")
            if timePair in self.__jsonFiles:
                with open("./pdfs/{fn}".format(fn = self.__jsonFiles[timePair])) as f:
                    if (f == None):
                        print("file not found\n")
                        continue;
                    incid = json.load(f) #list of dictionaries containing json info
                jsonDicList = jsonDicList + incid
                print(jsonDicList)
            m = m+1
            if (m == 12):
                m = 1
                y = y + 1

            if (y > self.__endDate.year): break
            elif (m > self.__endDate.month and y == self.__endDate.year): break

        return jsonDicList

    #helper function for creating location objects for creating incident objects
    def __assignLocationGroup(self, location):
        location = location.upper()
        return self.__locationData.locationGroup(location)

    #main method for creation of Incident objects from the JSON file
    def createIncidents(self):
        incidents = {}

        incid = self.__getJsonDic()

        d = self.__beginDate
        i = 0

        while (i < len(incid)):
            print(str(self.__beginDate) + "\n")
            print(str(self.__endDate) + "\n")

            inc = incid[i]
            incDateOcc = inc["event #"].split("-")
            dateOccurred = date(2000 + int(incDateOcc[0]), int(incDateOcc[1]), int(incDateOcc[2]) )

            if(dateOccurred >= self.__endDate):
                break
            elif (dateOccurred >= self.__beginDate and not(inc["event #"] in incidents) ):
                #print(inc)
                inc_date_rep = inc["date reported"].split(" ", 1)
                inc_date_rep = inc_date_rep[0].split("/")
                dateReported = date(2000 + int(inc_date_rep[2]), int(inc_date_rep[0]), int(inc_date_rep[1]))

                loc = Location(inc["location"], self.__assignLocationGroup(inc["location"]))
                event =  self.__incidentData.getCat(inc["incident"])

                loc.setCoords(inc["coordinates"][0], inc["coordinates"][1])
                inc_obj = Incident(inc["event #"], event, loc, dateOccurred, dateReported)

                incidents[inc["event #"]] = inc_obj
            i = i + 1

        #print(len(list(incidents.values() )))
        return list(incidents.values() )

    #set the date range for the incidents to be used to be created
    def setDateRange(self, begin, end):

        self.__beginDate = begin
        self.__endDate = end

    def setDateRangeFullAvailable(self):

        minDate = (date.today().month, date.today().year)

        for d in self.__jsonFiles:
            if (d[1] < minDate[1]):
                minDate = d
            elif (d[1] == minDate[1] and d[0] < minDate[0]):
                minDate = d

        self.__beginDate = Date(minDate[1], minDate[0], 1)
        maxDate = minDate

        for d in self.__jsonFiles:
            if (d[1] > maxDate[1]):
                maxDate = d
            elif (d[1] == maxDate[1] and d[0] > max_date[0]):
                maxDate = d

        self.__endDate = maxDate

#IncidentToJson class has the responsibility of taking the set of Incident objects being stored in the Incident Cache and creating a Json for use with the front-end
class IncidentToJson():
    def __init__(self):
        pass #currently takes no parameters but wanted to write functionality into class for extensiblilty purposes.

    #helper function handles writing to JSON
    def __dumpJSON(self, fileObj, incidDicList):
        #docs_list = list(incid_dic)
        jsonDocs = json.dumps(incidDicList, indent = 4)
        fileObj.write(jsonDocs)

    #creates JSON object for each incident object and writes to a JSON file whose name it returns
    def createJson(self, incidents, fname):

        incidDicList = []

        with open("./pdfs/{fn}".format(fn = fname), "w") as jsonFile:
            for incid in incidents:
                #create dictionary out of incident object as intermediate step in making JSON object
                incid_dic = {"event #": incid.eventNum, "incidentType": incid.incidentType, "location": incid.location.locationName, "location group": incid.location.locationGroup, "latitude": incid.location.lat, "longitude": incid.location.long, "date reported": incid.dateReported.isoformat(), "dateOccurred": incid.dateOccurred.isoformat()}

                incidDicList.append(incid_dic)

            self.__dumpJSON(jsonFile, incidDicList)
        jsonFile.close()

        return fname

#holds selection of incidents based on date range
class IncidentCache:

    #init will take in date objects made outside of the cache class in the main function upon start up reflecting the range of dates in the database that we want to pull incidents from
    def __init__(self):
        self.incidents = [] #list of incident objects
        self.__beginDate = date(date.today().year, date.today().month-1, 1) #default starting last month
        self.__endDate = date.today()
        #create own instance of JasonToIncident class to handle populating cache
        self.__jToI = JsonToIncident()

    #checks to see if most recent month's JSON is in the database, adds it in if not
    def checkForMostRecentJsonFile(self, files):
        self.__jToI.addJsonFile(files)

    def setJsonFiles(self, files):
        self.__jToI.setJsonFiles(files)

    #public-interfacing function to handle cache-date setting and population logic
    def setCacheByDate(self, beginDate, endDate):

        if (len(self.incidents) == 0):
            #if list of incidents is empty, populate with all from begin - end
            self.__beginDate = beginDate
            self.__endDate = endDate
            self.__fullyPopulateCache()
        elif (beginDate == self.__beginDate and endDate == self.__endDate):
            #if new dates are identical to dates already assigned no work need be done
            return 0
        else:
            #new begin and end dates will result in potentially different cache contents
            self.__setCacheByDate(beginDate, endDate)
        return 0

    #for when Cache is empty and needs to be newly occupied and create full set o
    def __fullyPopulateCache(self):

        self.__jToI.setDateRange(self.__beginDate, self.__endDate)
        self.incidents = self.__jToI.createIncidents()

    #occupy list of cache objects when there are already Incident objects occupying cache
    #seeks to avoid re-creating Incident objets already stored in cache that are still within newly specified dates
    def __setCacheByDate(self, newBegin, newEnd):

        newIncidents = []

        #add all of the Incidents from the old cache that fulfill the new dates into what
        #will be the new list
        for incid in self.incidents:
            if (incid.dateOccurred <= newEnd and incid.dateOccurred >= newBegin):
                newIncidents.append(incid)

        #find and add to list incidents that took place before the current beginning date
        #but after/during the new benning date
        if (newBegin < self.__beginDate):
            self.__jToI.setDateRange(newBegin, self.__beginDate)
            newIncidents = newIncidents + self.__jToI.createIncidents()

        #find and add to list incidents that took place after the current ending date
        #but before/during the new end date
        if (newEnd > self.__endDate):
            self.__jToI.setDateRange(self.__endDate, newEnd)
            newIncidents = newIncidents + self.__jToI.createIncidents()

        self.__beginDate = newBegin
        self.__endDate = newEnd

        self.incidents = newIncidents

#test to make sure that json file was succefully made and is not empty
def testJsonSuccessfullyCreated(jsonOutputFile):

    assert(os.path.isfile(jsonOutputFile))
    assert(os.stat(jsonOutputFile).st_size > 0)

#test to be sure that cache is not empty before trying to make json from its contents
def testCachePopulated(cache):
    assert(len(cache.incidents) > 0)
    print("help\n")


def generateRangeSeperateMonths(cache, begin_month, begin_year, end_month, end_year):
    ItoJ = IncidentToJson()

    i_month = begin_month
    i_year = begin_year

    days_in_month = calendar.monthrange(i_year, i_month)[1];

    while (i_month <= end_month and i_year <= end_year):
        generateUpdatedJsonByMonth(cache, i_month, i_year)

        i_month = i_month + 1
        if (i_month > 12):
            i_month = 0
            i_year = i_year+1

        #testJsonSuccessfullyCreated(jsonFname)
        #return jsonFname

#called by front end to create cache,  occupy, and create JSON for given month value
def generateUpdatedJsonByMonth(cache, month, year):

    #db_initial.runDB()
    cache.setCacheByDate(date(year, month, 1), date(year, month, calendar.monthrange(year, month)[1]))

    #testCachePopulated(cache)

    ItoJ = IncidentToJson()
    fname = "incidents_" + str(month) + "_" + str(year) + ".json"
    jsonFname = ItoJ.createJson(cache.incidents, fname)
    #testJsonSuccessfullyCreated(jsonFname)

    return jsonFname

def main():
    cache = IncidentCache()
    cache.setJsonFiles({(12,2016): "DEC_16.json", (11,2016): "NOV_16.json",(10,2016): "OCT_16.json",(9,2016): "SEP_16.json",(8,2016): "AUG_16.json",(7,2016): "JUL_16.json",(6,2016): "JUN_16.json",(5,2016): "MAY_16.json",(4,2016): "APR_16.json",(3,2016): "MAR_16.json",(2,2016): "FEB_16.json",(1,2016): "JAN_16.json"})

    generateRangeSeperateMonths(cache, 1, 2016, 12, 2016)
    #generateUpdatedJsonByMonth(cache, 2, 2016)

if __name__ == "__main__":
    main()