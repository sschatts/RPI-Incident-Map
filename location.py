class Null():
	#initialize to None
	def __init__(self):
		return None
	
	#add nothing when called
	def __add__(self, loc, desc, type, date, time):
		return self
		
	#return nothing when asked for info
	def __getLocation__(self, name):
		return self
	def __getDesc__(self, name):
		return self
	def __getType__(self, name):
		return self
	def __getDate__(self, name):
		return self
	def __getTime__(self, name):
		return self
	
	#report that the object is of type 'Null' if asked
	def __repr__(self):
		return '<Null>'
	
