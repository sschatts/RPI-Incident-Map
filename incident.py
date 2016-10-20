class Incident:
	def __init__(self, date_reported, location, event_num, datetime_from, datetime_to, incident_type, report_num, disposition):
		self.__date_reported = date_reported
		self.__location = location
		self.__event_num = event_num
		self.__datetime_from = datetime_from
		self.__datetime_to = datetime_to
		self.__incident_type = incident_type
		self.__report_num = report_num
		self.__disposition = disposition

	def get_date_reported(self):
		return self.__date_reported

	def get_location(self):
		return self.__location

	def get_event_num(self):
		return self.__event_num

	def get_datetime_from(self):
		return self.__datetime_from

	def get_datetime_to(self):
		return self.__datetime_to

	def get_incident_type(self):
		return self.__incident_type

	def get_report_num(self):
		return self.__report_num

	def get_disposition(self):
		return self.__disposition
