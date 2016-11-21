import json, pytest
import db_initial
from datetime import date
from datetime import time

class Location:
    def __init__(self, name, group):
        self.lat = 42.727
        self.long = -73.676
        self.location_name = name
        self.location_group = group

    def setCoords(self, _lat, _long):
        self.lat = _lat
        self.long = _long


##this will be initialized using strings and datetime objects created from the information in the mongo db entries
class Incident:
    def __init__(self, _event_num, _incident_type, _location, _date_occurred, _date_reported):
        self.event_num = _event_num #int
        self.incident_type = _incident_type #string
        self.location = _location #location description

        ##just use python built-in date objects for these::
        self.date_reported = _date_reported #datetime.date
        self.date_occurred = _date_occurred #datetime.date

class LocationData():
    def __init__(self):

        self.north = {"GYMNASIUM, '87", "CAMPUS PARKING, NORTH LOT", "E-COMPLEX", "COLONIE APARTMENTS", "HEFFNER ALUMNI HOUSE", "J-BUILDING", "SAGE AVENUE", "BLITMAN RESIDENCE COMMONS"}

        self.east = {"EAST CAMPUS ATHLETIC VILLAGE", "HOUSTON FIELD HOUSE", "BURDETT AVENUE RESIDENCE", "DAVISON HALL", "NASON HALL", "CROCKETT HALL", "BARTON HALL", "RENSSELAER UNION", "BRAY HALL" "RAHPS - ALBRIGHT", "RAHPS-B", "COMMONS DINING HALL (FRES", "COMMONS PARKING", "Robinson Pool", "MUELLER CENTER", "QUADRANGLE DORMS", "DEPARTMENT OF PUBLIC SAFETY", "NED HARKNESS ATHLETIC FIE", "STACWYCK - MCGIFFERT", "Sherry Road", "BRYCKWYCK APARTMENTS", "WARREN HALL", "CARY HALL", "BRINSMADE TERRACE", "Sharp Hall", "RENSSELAER CRITICAL FACIL", "NUGENT HALL", "STACWYCK-ROUSSEAU", "STACWYCK - WILTSIE", "PUBLIC SAFETY OFFICE", "H- BUILDING"}

        self.off = {"OTHER OFF-CAMPUS LOCATION", "BEMAN LANE", "SHERRY ROAD"}
        self.west = {"POLYTECH APARTMENTS", "CITY STATION", "CAMPUS PARKING, WEST LOT", "EMPAC BUILDING", "WEST HALL"}
        self.south = {"MOE'S SOUTHWEST GRILL"}
        self.academic = {"RUSSELL SAGE LABORATORY", "COGSWELL LABORATORY", "GREENE BUILDING", "JONSSON ENGINEERING CENTE", "ACADEMY HALL", "BIOTECH"}
        self.default_group = "RPI"

    def locationGroup(self, loc):
        assert loc != ""

        if(loc in self.north): return "North"
        elif(loc in self.off): return "Off Campus"
        elif(loc in self.west): return "West"
        elif(loc in self.south): return "South"
        else:
            return self.default_group


class JsonToIncident:
    def __init__(self):
        self.begin_date = date(2016, 10, 1)
        self.end_date = date(2016, 10, 31)

        self.location_data = LocationData()
        self.json_files = {}

    def setJsonFiles(self, files):
        self.json_files = files
        return 0

    #returns list of dictionaries for months matching date range
    def getJsonDic(self):
        json_dic_list = [] #list of dictionaries with all json files of specified date range

        assert isinstance(self.begin_date, date())
        assert isinstance(self.end_date, date())

        m = self.begin_date.month
        y = self.begin_date.year

        while (y <= date.today().year):
            time_pair = (m, y)
            if time_pair in self.json_files:
                with open(self.json_files[time_pair]) as f:
                    incid = json.load(f) #list of dictionaries containing json info
                json_dic_list = json_dic_list + incid

            m = m+1
            if (m == 12):
                m = 1
                y = y + 1

            if (y > self.end_date.year): break
            elif (m > self.end_date.month and y == self.end_date.year): break

        return json_dic_list

    def assignLocationGroup(self, location):
        location = location.upper()
        return self.location_data.locationGroup(location)


    def createIncidents(self):
        incidents = {}

        incid = self.getJsonDic()
        assertTrue(len(incid) > 0)
        d = self.begin_date
        i = 0

        while (i < len(incid)):
            inc = incid[i]
            inc_date_occ = inc['event #'].split("-")
            date_occurred = date(2000 + int(inc_date_occ[0]), int(inc_date_occ[1]), int(inc_date_occ[2]) )

            if(date_occurred >= self.end_date):
                break
            elif (date_occurred >= self.begin_date and not(inc['event #'] in incidents) ):
                #print(inc)
                inc_date_rep = inc['date reported'].split(" ", 1)
                inc_date_rep = inc_date_rep[0].split("/")
                date_reported = date(2000 + int(inc_date_rep[2]), int(inc_date_rep[0]), int(inc_date_rep[1]))

                loc = Location(inc['location'], self.assignLocationGroup(inc['location']))

                loc.setCoords(inc['coordinates'][0], inc['coordinates'][1])
                inc_obj = Incident(inc['event #'], incid[i]['incident'], loc, date_occurred, date_reported)

                incidents[inc['event #']] = inc_obj
            i = i + 1

        print(len(list(incidents.values() )))
        return list(incidents.values() )

    def setDateRange(self, _begin, _end):
        assertTrue(_begin <= _end)
        self.begin_date = _begin
        self.end_date = _end

class IncidentToJson():

    def __init__(self):
        pass

    def dumpJSON(self, file_obj, incid_dic_list):
        #docs_list = list(incid_dic)
        json_docs = json.dumps(incid_dic_list, indent = 4)
        file_obj.write(json_docs)

    def createJson(self, incidents):

        fname = 'incidents.json'
        incid_dic_list = []

        with open(fname, 'w') as json_file:
            for incid in incidents:

                incid_dic = {'event #': incid.event_num, 'incident_type': incid.incident_type, 'location': incid.location.location_name, 'location group': incid.location.location_group, 'latitude': incid.location.lat, "longitude": incid.location.long, 'date reported': incid.date_reported.isoformat(), 'date_occurred': incid.date_occurred.isoformat()}

                incid_dic_list.append(incid_dic)

            self.dumpJSON(json_file, incid_dic_list)
        json_file.close()

        return fname

#holds selection of incidents based on date range
class IncidentCache:

    #init will take in date objects made outside of the cache class in the main function upon start up reflecting the range of dates in the database that we want to pull incidents from
    def __init__(self):
        self.incidents = [] #list of incident objects
        self.begin_date = date(date.today().year, date.today().month-1, 1) #default starting last month
        self.end_date = date.today()

        self.JtoI = JsonToIncident()

    def assignJsonFiles(self, files):
        r = self.JtoI.setJsonFiles(files)
        assert r == 0

    def setCacheByDate(self, _begin_date, _end_date):
        assert _begin_date < _end_date


        if (len(self.incidents) == 0):
            self.begin_date = _begin_date
            self.end_date = _end_date
            self.fullyPopulateCache()
        elif (_begin_date == self.begin_date and _end_date == self.end_date):
            return 0
        else:
            self._setCacheByDate(_begin_date, _end_date)
        return 0

    def fullyPopulateCache(self):
        assert self.begin_date != None
        assert self.end_date != None
        assert self.begin_date <= self.end_date

        self.JtoI.setDateRange(self.begin_date, self.end_date)
        self.incidents = self.JtoI.createIncidents()

    def _setCacheByDate(self, new_begin, new_end):

        assert new_begin <= date.today()
        assert new_end <= date.today()

        new_incidents = []

        for incid in self.incidents:
            if (incid.date_occurred <= new_end and incid.date_occurred >= new_begin):
                new_incidents.append(incid)

        if (new_begin < self.begin_date):
            self.JtoI.setDateRange(new_begin, self.begin_date)
            new_incidents = new_incidents + self.JtoI.createIncidents()

        if (new_end > self.end_date):
            self.JtoI.setDateRange(self.end_date, new_end)
            new_incidents = new_incidents + self.JtoI.createIncidents()

        self.begin_date = new_begin
        self.end_date = new_end

        self.incidents = new_incidents



def getCacheJsonByMonth(month):

    assert db_initial.runDB() == 0
    cache = IncidentCache()

    cache.assignJsonFiles(db_initial.filename())
    r = cache.setCacheByDate(date(2016, month, 1), date(2016, month, 30))
    assert r == 0
    ItoJ = IncidentToJson()

    return ItoJ.createJson(cache.incidents)
