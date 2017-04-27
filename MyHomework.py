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

MYHOMEWRK_COOKIES = ""

def login(username,password):
	#Get our CSRF tokens and our secret before we can authenticate. To do this we need to load the page
	request = urllib2.Request("https://myhomeworkapp.com/login")
	res = urllib2.urlopen(url=request)
	csrfPage = res.read();
	csrfPage = HTMLParser().unescape(csrfPage)
	token = res.info()["Set-Cookie"]
	csrf = re.search('myhw_csrf=................................;',token).group(0)
	secret = re.search('myhw_s=................................;',token).group(0)


	MYHOMEWORK_MIDDLEWARETOKEN = csrf
	MYHOMEWRK_COOKIES = "" + secret + csrf
	url = 'https://myhomeworkapp.com/login'
	request = urllib2.Request(url)
	request.add_header('Cookie',MYHOMEWRK_COOKIES)	
	res = urllib2.urlopen(request, data="csrfmiddlewaretoken=" + csrf.replace("myhw_csrf=","") + "&username=" + username + "&password=" + password + "&next=")
	#print any errors??	
	#print res.read()
	return csrf , secret

#Same date for both returns all actie assignments
def getAssignments():
	request = urllib2.Request("https://myhomeworkapp.com/home")
	request.add_header('cookie',MYHOMEWRK_COOKIES)
	res = urllib2.urlopen(url=request)
	myHomeWorkAssignmentView = res.read();
	#Clean up (remove HTML'd tags)
	myHomeWorkAssignmentView = HTMLParser().unescape(myHomeWorkAssignmentView)
	return myHomeWorkAssignmentView