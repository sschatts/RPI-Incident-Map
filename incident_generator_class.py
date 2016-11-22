#classes centered around processing data taken from the database JSON, storing it, and wriitng it to a JSON for the front end to parse
#written for RPI Incident Map

import sys
import json
import os

import db_initial
from datetime import date
from datetime import time

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
        self.__endDate = date(date.today().year, date.today().month, 30)

        self.__locationData = LocationData()
        self.__jsonFiles = {}

    #assign dicitonary of {(month, year), "filename"} entries to refer to for parsing grouped by months
    def setJsonFiles(self, files):
        self.__jsonFiles = files
        return 0
        
    #returns list of dictionaries for months matching date range
    def __getJsonDic(self):
        jsonDicList = [] #list of dictionaries with all json files of specified date range
        
        m = self.__beginDate.month
        y = self.__beginDate.year

        while (y <= date.today().year):
            timePair = (m, y)
            if timePair in self.__jsonFiles:
                with open(self.__jsonFiles[timePair]) as f:
                    incid = json.load(f) #list of dictionaries containing json info
                jsonDicList = jsonDicList + incid

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
            inc = incid[i]
            incDateOcc = inc['event #'].split("-")
            dateOccurred = date(2000 + int(incDateOcc[0]), int(incDateOcc[1]), int(incDateOcc[2]) )

            if(dateOccurred >= self.__endDate):
                break
            elif (dateOccurred >= self.__beginDate and not(inc['event #'] in incidents) ):
                #print(inc)
                inc_date_rep = inc['date reported'].split(" ", 1)
                inc_date_rep = inc_date_rep[0].split("/")
                dateReported = date(2000 + int(inc_date_rep[2]), int(inc_date_rep[0]), int(inc_date_rep[1]))

                loc = Location(inc['location'], self.__assignLocationGroup(inc['location']))
                
                loc.setCoords(inc['coordinates'][0], inc['coordinates'][1])
                inc_obj = Incident(inc['event #'], incid[i]['incident'], loc, dateOccurred, dateReported)

                incidents[inc['event #']] = inc_obj
            i = i + 1

        #print(len(list(incidents.values() )))
        return list(incidents.values() )

    #set the date range for the incidents to be used to be created
    def setDateRange(self, begin, end):
        
        self.__beginDate = begin
        self.__endDate = end

#IncidentToJson class has the responsibility of taking the set of Incident objects being stored in the Incident Cache and creating a Json for use with the front-end
class IncidentToJson():
    def __init__(self):
        pass #currently takes no parameters but wanted to write functionality into class for extensiblilty purposes.

    #helper function handles writing to JSON 
    def __dumpJSON(self, file_obj, incidDicList):
        #docs_list = list(incid_dic)
        jsonDocs = json.dumps(incidDicList, indent = 4)
        file_obj.write(jsonDocs)

    #creates JSON object for each incident object and writes to a JSON file whose name it returns
    def createJson(self, incidents):

        fname = 'incidents_.json'
        incidDicList = []

        with open(fname, 'w') as jsonFile:
            for incid in incidents:
                #create dictionary out of incident object as intermediate step in making JSON object
                incid_dic = {'event #': incid.eventNum, 'incidentType': incid.incidentType, 'location': incid.location.locationName, 'location group': incid.location.locationGroup, 'latitude': incid.location.lat, "longitude": incid.location.long, 'date reported': incid.dateReported.isoformat(), 'dateOccurred': incid.dateOccurred.isoformat()}

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

    #called to interface with use
    def assignJsonFiles(self, files):
        self.__jToI.setJsonFiles(files)

    #public-interfacing function to handle cache-date setting and population logic
    def setCacheByDate(self, beginDate, endDate):

        if (len(self.incidents) == 0):
            #if list of incidents is empty, populate with all from begin - end
            self.__beginDate = beginDate
            self.__endDate = endDate
            self.__fullyPopulateCache()
        elif (_beginDate == self.__beginDate and _endDate == self.__endDate):
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
    def __setCacheByDate(self, new_begin, new_end):

        new_incidents = []
        
        #add all of the Incidents from the old cache that fulfill the new dates into what
        #will be the new list
        for incid in self.incidents:
            if (incid.dateOccurred <= new_end and incid.dateOccurred >= new_begin):           
                new_incidents.append(incid)
        
        #find and add to list incidents that took place before the current beginning date
        #but after/during the new benning date
        if (new_begin < self.beginDate):
            self.__jToI.setDateRange(new_begin, self.beginDate)
            new_incidents = new_incidents + self.__jToI.createIncidents()

        #find and add to list incidents that took place after the current ending date 
        #but before/during the new end date
        if (new_end > self.endDate):
            self.__jToI.setDateRange(self.endDate, new_end)
            new_incidents = new_incidents + self.__jToI.createIncidents()
        
        self.__beginDate = new_begin
        self.__endDate = new_end

        self.incidents = new_incidents

#test to make sure that json file was succefully made and is not empty
def testJsonSuccessfullyCreated(jsonOutputFile):   
    
    assert(os.path.isfile(jsonOutputFile))
    assert(os.stat(jsonOutputFile).st_size > 0)
    
#test to be sure that cache is not empty before trying to make json from its contents    
def testCachePopulated(cache):      
    assert(len(cache.incidents) > 0)
    

#called by front end to create cache,  occupy, and create JSON for given month value
def getCacheJsonByMonth(month):
    
    db_initial.runDB()
    cache = IncidentCache()

    cache.assignJsonFiles(db_initial.filename())
    
    cache.setCacheByDate(date(2016, month, 1), date(2016, month, 30))
    testCachePopulated(cache)
    
    ItoJ = IncidentToJson()
    jsonFname = ItoJ.createJson(cache.incidents)
    testJsonSuccessfullyCreated(jsonFname)
    
    return jsonFname
