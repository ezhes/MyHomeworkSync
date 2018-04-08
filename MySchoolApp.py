# coding: utf-8

from HTMLParser import HTMLParser
from datetime import date
from pprint import PrettyPrinter

class MLStripper(HTMLParser):
	def __init__(self):
		self.reset()
		self.fed = []
	def handle_data(self, d):
		self.fed.append(d)
	def get_data(self):
		return ''.join(self.fed)

def strip_tags(html):
	s = MLStripper()
	s.feed(html)
	return s.get_data()


import urllib2,re,json

cookie = ""

def login(username,password):
	url = 'https://domain.myschoolapp.com/api/SignIn'
	request = urllib2.Request(url, data='{"From":"","Username":"' + username + '","Password":"'+password+'","remember":false,"InterfaceSource":"WebApp"}')
	request.add_header('Content-Type', 'application/json')
	res = urllib2.urlopen(request)
	
	#Now we need to extract our token
	token = res.info()["Set-Cookie"]
	token = re.search('t=........-....-....-....-............;',token).group(0)
	return token
	
class Assignment(object):
	def __init__(self, attributes):
			self.__dict__ = attributes
#									M/D/Y 2/12/16
#Same date for both returns all actie assignments
def getAssignments(startDate,endDate):
	startDate = startDate.replace("/","%2F")
	endDate = endDate.replace("/","%2F")
	url = "https://domain.myschoolapp.com/api/DataDirect/AssignmentCenterAssignments/?format=json&filter=2&dateStart=" +startDate+"&dateEnd="+ endDate +"&persona=2&statusList=&sectionList="
	request = urllib2.Request(url)
	request.add_header('cookie',cookie)
	request.add_header("user-agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.103 Safari/537.36")
	res = urllib2.urlopen(request)
	#Replace <br> with new lines, and then strip so we preserve formatting
	formattedData = res.read().replace("<br />","\\n");
	parsedJSON = json.loads(strip_tags(formattedData))
	classData = []
	for assignmentData in parsedJSON:
		#Generate the assignment object stuffed with our data. Notice though that we don't strip any data
		classData.append(Assignment(assignmentData))
	return classData
	
