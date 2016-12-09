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

    #based on location name, set to pre-described set of coordinates or simply set given coordinates otherwise
    def setCoords(self, _lat, _long):
        if self.locationName == "GYMNASIUM, '87":
            self.lat = 42.73067242610324
            self.long = -73.67879659842443
        elif self.locationName == "CAMPUS PARKING, NORTH LOT":
            self.lat = 42.73189580232432
            self.long = -73.67973331475349
        elif self.locationName == "E-COMPLEX":
            self.lat = 42.73135202794529
            self.long = -73.67918059513268
        elif self.locationName == "COLONIE APARTMENTS":
            self.lat = 42.73703620020072
            self.long = -73.66976682211441
        elif self.locationName == "HEFFNER ALUMNI HOUSE":
            self.lat = 42.73284560630685
            self.long = -73.67817593843475
        elif self.locationName == "J-BUILDING":
            self.lat = 42.733117266688254
            self.long = -73.67986472791176
        elif self.locationName == "SAGE AVENUE":
            self.lat = 42.730761766371955
            self.long = -73.67722773270161
        elif self.locationName == "BLITMAN RESIDENCE COMMONS":
            self.lat = 42.7310933063807
            self.long = -73.68591563187375
        elif self.locationName == "COLONIE APTS., BUILDING A":
            self.lat = 42.737090635765725
            self.long = -73.67009919263029
        elif self.locationName == "EAST CAMPUS ATHLETIC VILLAGE":
            self.lat = 42.73263084166069
            self.long = -73.66764682428808
        elif self.locationName == "HOUSTON FIELD HOUSE":
            self.lat = 42.73209560605264
            self.long = -73.66953744376613
        elif self.locationName == "BURDETT AVENUE RESIDENCE":
            self.lat = 42.73098888681125
            self.long = -73.67125398839589
        elif self.locationName == "DAVISON HALL":
            self.lat = 42.72722486686345
            self.long = -73.67399248324392
        elif self.locationName == "NASON HALL":
            self.lat = 42.72751314059482
            self.long = -73.67337991308187
        elif self.locationName == "CROCKETT HALL":
            self.lat = 42.72824436551426
            self.long = -73.673207627723778
        elif self.locationName == "BARTON HALL":
            self.lat = -73.6740888160001
            self.long = 42.72911680528088
        elif self.locationName == "RENSSELAER UNION":
            self.lat = 42.7299463204162
            self.long = -73.676624920769692
        elif self.locationName == "BRAY HALL":
            self.lat = 42.728702046516275
            self.long = -73.6736673423851
        elif self.locationName == "RAHPS - ALBRIGHT":
            self.lat = 42.73088520955366
            self.long = -73.6700955123804
        elif self.locationName == "RAHPS-B":
            self.lat = 42.73474220634665
            self.long = -73.66483559926472
        elif self.locationName == "COMMONS DINING HALL (FRES":
            self.lat = 42.728243546616795
            self.long = -73.6742899720452
        elif self.locationName == "COMMONS PARKING":
            self.lat = 42.727979016564916
            self.long = -73.6735453658362
        elif self.locationName == "SPORTS CENTER AND ROBISON":
            self.lat = 42.72845782378502
            self.long = -73.67688407231195
        elif self.locationName == "MUELLER CENTER":
            self.lat = 42.72881676290331
            self.long = -73.67688407231195
        elif self.locationName == "QUADRANGLE DORMS":
            self.lat = 42.730143100420605
            self.long = -73.67761291257993
        elif self.locationName == "DEPARTMENT OF PUBLIC SAFETY":
            self.lat = 42.72923586512002
            self.long = -73.67701569236513
        elif self.locationName == "NED HARKNESS ATHLETIC FIE":
            self.lat = 42.73156863244981
            self.long = -73.67825085235435
        elif self.locationName == "STACWYCK - MCGIFFERT":
            self.lat = 42.73314062630479
            self.long = -73.66511451257983
        elif self.locationName == "Sherry Road" or self.locationName == "SHERRY ROAD":
            self.lat = 42.73087899884066
            self.long = -73.67369139472586
        elif self.locationName == "BRYCKWYCK APARTMENTS":
            self.lat = 42.73492910066227
            self.long = -73.66361998826527
        elif self.locationName == "WARREN HALL":
            self.lat = 42.72784050877053
            self.long = -73.67509812972061
        elif self.locationName == "CARY HALL":
            self.lat = 42.728905018929055
            self.long = -73.67478480132652
        elif self.locationName == "BRINSMADE TERRACE":
            self.lat = 42.735632211847616
            self.long = -73.66506320340723
        elif self.locationName == "Sharp Hall":
            self.lat = 42.7269822575488
            self.long = -73.67466417847211
        elif self.locationName == "RENSSELAER CRITICAL FACIL":
            self.lat = 42.73264514900845
            self.long = -73.6622607418487
        elif self.locationName == "NUGENT HALL":
            self.lat = 42.72739026689658
            self.long = -73.67502527441694
        elif self.locationName == "STACWYCK-ROUSSEAU":
            self.lat = 42.734344759418576
            self.long = -73.66428968303421
        elif self.locationName == "STACWYCK - WILTSIE":
            self.lat = 42.733541665388685
            self.long = -73.6648587073975
        elif self.locationName == "PUBLIC SAFETY OFFICE":
            self.lat = 42.729223288503164
            self.long = -73.67700513871677
        elif self.locationName == "H- BUILDING":
            self.lat = 42.73256750010199
            self.long = -73.6792379380625
        elif self.locationName == "OTHER OFF-CAMPUS LOCATION":
            self.lat = 0
            self.long = 0
        elif self.locationName == "BEMAN LANE":
            self.lat = 42.735035688099885
            self.long = -73.66443557297075
        elif self.locationName == "POLYTECH APARTMENTS":
            self.lat = 42.72221214829
            self.long = -73.67948651818986
        elif self.locationName == "CITY STATION":
            self.lat = 42.727739110499016
            self.long = -73.68723375821551
        elif self.locationName == "CAMPUS PARKING, WEST LOT":
            self.lat = 42.73165871918334
            self.long = -73.68223708828592
        elif self.locationName == "EMPAC BUILDING":
            self.lat = 42.728812765654794
            self.long = -73.68385189903341
        elif self.locationName == "WEST HALL":
            self.lat = 42.731690336122455
            self.long = -73.68310910272476
        elif self.locationName == "MOE'S SOUTHWEST GRILL":
            self.lat = 42.72674767040843
            self.long = -73.67849312485687
        elif self.locationName == "RUSSELL SAGE LABORATORY":
            self.lat = 42.730856613395844
            self.long = -73.68167224683165
        elif self.locationName == "COGSWELL LABORATORY":
            self.lat = 42.72806029085524
            self.long = -73.6813180789666
        elif self.locationName == "GREENE BUILDING":
            self.lat = 42.72998227661651
            self.long = -73.68120622042984
        elif self.locationName == "JONSSON ENGINEERING CENTE":
            self.lat = 42.729572616483665
            self.long = -73.68038928445317
        elif self.locationName == "ACADEMY HALL":
            self.lat = 42.727467124534115
            self.long = -73.678754225567
        elif self.locationName == "BIOTECH":
            self.lat = 42.728339214725366
            self.long = -73.6788414520519
        else:
            self.lat = _lat
            self.long = _long

#Used to standardize the incident types when creating incident objects from the 
class IncidentData:
    def __init__(self):
        self.__categories = ["Mischief","Fire Alarm", "Medical Incident", "Intoxication","Property Damage","Larceny and Assault", "Other"]

    def getCat(self, description):
        descCategory = ""
        #find matching description for incident type
        i = 0
        while i < len(self.__categories):
            if (self.__categories[i].upper() in description.upper()):
                descCategory = descCategory + self.__categories[i]
            i += 1

        #if no description matches, use other
        if (descCategory == ""):
            #print("in other")
            descCategory = "Other"
        #print(descCategory)
        return descCategory

    #returns copy of list of incident categories
    def getCategories(self):
        return self.__categories

#Incident class to hold information for filtering/displaying individual incidents
#initialization requires strings for eventNum and incidentType, a location object, and date objects for dateReported and dateOccurred
class Incident:
    def __init__(self, _eventNum, _incidentType, _location, _dateOccurred, _dateReported):
        self.eventNum = _eventNum #string
        self.incidentType = _incidentType #string
        self.location = _location #location description

        #just use python built-in date objects for these::
        self.dateReported = _dateReported #datetime.date
        self.dateOccurred = _dateOccurred #datetime.date

#LocationData class for storing data used for populating Location objects for use within an Incident object
#known, static set of buildings and landmarks are grouped into location groups based on subjective campus significance, hence the hard-coding
class LocationData():
    def __init__(self):

        self.__locationGroups = ["North", "East", "South", "West", "Off-Campus", "Academic", "all"]

        self.__north = {"GYMNASIUM, '87", "CAMPUS PARKING, NORTH LOT", "E-COMPLEX", "COLONIE APARTMENTS", "HEFFNER ALUMNI HOUSE", "J-BUILDING", "SAGE AVENUE", "BLITMAN RESIDENCE COMMONS", "COLONIE APTS., BUILDING A"}

        self.__east = {"EAST CAMPUS ATHLETIC VILLAGE", "HOUSTON FIELD HOUSE", "BURDETT AVENUE RESIDENCE", "DAVISON HALL", "NASON HALL", "CROCKETT HALL", "BARTON HALL", "RENSSELAER UNION", "BRAY HALL" "RAHPS - ALBRIGHT", "RAHPS-B", "COMMONS DINING HALL (FRES", "COMMONS PARKING", "SPORTS CENTER AND ROBISON", "MUELLER CENTER", "QUADRANGLE DORMS", "DEPARTMENT OF PUBLIC SAFETY", "NED HARKNESS ATHLETIC FIE", "STACWYCK - MCGIFFERT", "Sherry Road", "BRYCKWYCK APARTMENTS", "WARREN HALL", "CARY HALL", "BRINSMADE TERRACE", "Sharp Hall", "RENSSELAER CRITICAL FACIL", "NUGENT HALL", "STACWYCK-ROUSSEAU", "STACWYCK - WILTSIE", "PUBLIC SAFETY OFFICE", "H- BUILDING"}
        self.__off = {"OTHER OFF-CAMPUS LOCATION", "BEMAN LANE", "SHERRY ROAD"}
        self.__west = {"POLYTECH APARTMENTS", "CITY STATION", "CAMPUS PARKING, WEST LOT", "EMPAC BUILDING", "WEST HALL"}
        self.__south = {"MOE'S SOUTHWEST GRILL"}
        self.__academic = {"RUSSELL SAGE LABORATORY", "COGSWELL LABORATORY", "GREENE BUILDING", "JONSSON ENGINEERING CENTE", "ACADEMY HALL", "BIOTECH"}
        self.__defaultGroup = "RPI"
        
    def locationGroup(self, loc):
        if(loc in self.__north): return self.__locationGroups[0]
        elif(loc in self.__east): return self.__locationGroups[1]
        elif(loc in self.__south): return self.__locationGroups[2]
        elif(loc in self.__west): return self.__locationGroups[3]
        elif(loc in self.__off): return self.__locationGroups[4]
        elif(loc in self.__academic): return self.__locationGroups[5]
        else:
            return self.__defaultGroup
    
    #return 
    def getLocGroup(self):
        return self.__locationGroups;

#JsontoIncident class uses a given (or default) date range to select an appropriate set of month/year tagged JSON files to create
#a list of incident objects
class JsonToIncident:
    def __init__(self):
        self.__beginDate = date(date.today().year, date.today().month, 1)
        self.__endDate = date(date.today().year, date.today().month, 30)

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

        while (y <= date.today().year):
            timePair = (m, y)
            if timePair in self.__jsonFiles:
                with open("./pdfs/{fn}".format(fn = self.__jsonFiles[timePair])) as f:
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
        #loop to create incident objects and populate cahce,
        while (i < len(incid)):
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
        
    #not used currently, for extensibility. sets dates range of jsonToIncident dates to widest possible
    #range given the currently available set of by-month json files from the db
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
            elif (d[1] == maxDate[1] and d[0] > miax_date[0]):
                maxDate = d

        self.__endDate = maxDate

#IncidentToJson class has the responsibility of taking the set of Incident objects being stored in the Incident Cache and creating a Json for use with the front-end
class IncidentToJson():
    def __init__(self):
        pass #currently takes no parameters but wanted to write functionality into class for extensibility purposes.

    #virtual for more trait-specific jsons being made
    def extendFname(self, fname, extended):
        if (extended != "all"):
            fname_spl = fname.split(".")
            extended= extended.replace(" ", "-")
            fname = fname_spl[0] + "_" + extended + "." + fname_spl[1]
        return fname

    #helper function handles writing to JSON
    def dumpJSON(self, fileObj, incidDicList):
        #docs_list = list(incid_dic)
        jsonDocs = json.dumps(incidDicList, indent = 4)
        fileObj.write(jsonDocs)

    def incidToDic(self, incid):
        incid_dic = {"event #": incid.eventNum, "incidentType": incid.incidentType, "location": incid.location.locationName, "location group": incid.location.locationGroup, "latitude": incid.location.lat, "longitude": incid.location.long, "date reported": incid.dateReported.isoformat(), "dateOccurred": incid.dateOccurred.isoformat()}

        return incid_dic


    #creates JSON object for each incident object and writes to a JSON file whose name it returns
    def createJson(self, incidents, fname):

        incidDicList = []
        with open("./pdfs/{fn}".format(fn = fname), "w") as jsonFile:
            for incid in incidents:
                #create dictionary out of incident object as intermediate step in making JSON object
                #checks for locaiton group to make pins for
                incid_dic = self.incidToDic(incid)
                incidDicList.append(incid_dic)
            self.dumpJSON(jsonFile, incidDicList)
        jsonFile.close()

        return fname

#subclass of IncidentToJson class speficially for providing a Json of incidents given a specific location group
class IncidentToJsonLocationGroup(IncidentToJson):
    #creates JSON object for each incident object and writes to a JSON file whose name it returns
    
    #checks for presence of targeted trait in an incident or that any trait is permissalbe
    #in this subtype, checking for location grouping
    def __checkTrait(self, location_group, incid):
        if (location_group == "all"):
            return True
        elif (location_group == incid.location.locationGroup):
            return True
        else:
            return False

    #return the name of newly created Json file having created it from Incident objects filtered for location groups
    def createJson(self, incidents, fname, location_group):
        incidDicList = []
        fname = super(IncidentToJsonLocationGroup, self).extendFname(fname, location_group)
        with open("./pdfs/{fn}".format(fn = fname), "w") as jsonFile:
            for incid in incidents:
                #create dictionary out of incident object as intermediate step in making JSON object
                #checks for locaiton group to make pins for
                if (self.__checkTrait(location_group, incid)):
                    incid_dic = super(IncidentToJsonLocationGroup, self).incidToDic(incid)
                    incidDicList.append(incid_dic)
            super(IncidentToJsonLocationGroup, self).dumpJSON(jsonFile, incidDicList)
        jsonFile.close()

        return fname

#subclass of IncidentToJson class, creates incident jsons filtered by incident_type
class IncidentToJsonIncidentType(IncidentToJson):

    #checks for incident_type in incident object
    def __checkTrait(self, incident_type, incid):
            if (incident_type == "all"):
                return True
            elif (incident_type == incid.incidentType):
                return True
            else:
                return False

    #creates JSON object for each incident object and writes to a JSON file whose name it returns
    def createJson(self, incidents, fname, incident_type):
        incidDicList = []
        fname = super(IncidentToJsonIncidentType, self).extendFname(fname, incident_type)
        with open("./pdfs/{fn}".format(fn = fname), "w") as jsonFile:
            for incid in incidents:
                #create dictionary out of incident object as intermediate step in making JSON object
                #checks for locaiton group to make pins for
                if (self.__checkTrait(incident_type, incid)):
                    incid_dic = super(IncidentToJsonIncidentType, self).incidToDic(incid)
                    incidDicList.append(incid_dic)
            super(IncidentToJsonIncidentType, self).dumpJSON(jsonFile, incidDicList)
        jsonFile.close()

        return fname

#simple factory method that creates and returns an appropriate IncidentToJson class object for doing Json parsing
def createJsonMaker(category):
    if (category == "location"):
        return IncidentToJsonLocationGroup()
    elif (category == "incident_type"):
        return IncidentToJsonIncidentType()
    else:
        return IncidentToJson()


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
    assert(cache.incidents > 0)
    

def generateRangeSeperateMonths(cache, begin_month, begin_year, end_month, end_year, extra_parameters=""):
    ItoJ = IncidentToJson()

    i_month = begin_month
    i_year = begin_year

    days_in_month = calendar.monthrange(i_year, i_month)[1];

    while (i_month <= end_month and i_year <= end_year):
        generateUpdatedJsonByMonth(cache, i_month, i_year, extra_parameters)

        i_month = i_month + 1
        if (i_month > 12):
            i_month = 0
            i_year = i_year+1

        #testJsonSuccessfullyCreated(jsonFname)
        #return jsonFname

#called by front end to create cache,  occupy, and create JSON for given month value
def generateUpdatedJsonByMonth(cache, month, year, extra_parameters=""):
    #db_initial.runDB()
    cache.setCacheByDate(date(year, month, 1), date(year, month, calendar.monthrange(year, month)[1]))

    #testCachePopulated(cache)

    ItoJ = IncidentToJson()
    fname = "incidents_" + str(month) + "_" + str(year) + ".json"

    if (extra_parameters == "location"):
        l_groups = LocationData().getLocGroup()
        for loc in l_groups:
            jsonFname = createJsonMaker("location").createJson(cache.incidents, fname, loc)
    elif (extra_parameters == "incident_type"):
        in_type = IncidentData().getCategories()
        for it in in_type:

            jsonFname = createJsonMaker("incident_type").createJson(cache.incidents, fname, it)
    else:
        jsonFname = createJsonMaker("").createJson(cache.incidents, fname)

    #testJsonSuccessfullyCreated(jsonFname)
    return jsonFname

def main():
    cache = IncidentCache()
    #know the set of raw data available json files
    cache.setJsonFiles({(12,2016): "DEC_16.json", (11,2016): "NOV_16.json",(10,2016): "OCT_16.json",(9,2016): "SEP_16.json",(8,2016): "AUG_16.json",(7,2016): "JUL_16.json",(6,2016): "JUN_16.json",(5,2016): "MAY_16.json",(4,2016): "APR_16.json",(3,2016): "MAR_16.json",(2,2016): "FEB_16.json",(1,2016): "JAN_16.json"})

    #call using "location", "incident_type", or "all"
    generateRangeSeperateMonths(cache, 1, 2016, 12, 2016, "all")
    generateRangeSeperateMonths(cache, 1, 2016, 12, 2016, "location")
    generateRangeSeperateMonths(cache, 1, 2016, 12, 2016, "incident_type")

    generateUpdatedJsonByMonth(cache, 12, 2016, "all")
    generateUpdatedJsonByMonth(cache, 12, 2016, "location")
    generateUpdatedJsonByMonth(cache, 12, 2016, "incident_type")



if __name__ == "__main__":
    main()
