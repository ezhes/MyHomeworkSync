# coding: utf-8
import MySchoolApp #The assignment getter class
import MyHomework
from datetime import date, timedelta #needed to get today and next week
import urllib2 #needed to pull and add to myhomework
from HTMLParser import HTMLParser #needed to clean the results from the GET myhomework

import sys
reload(sys)
sys.setdefaultencoding('utf8')


#Setup MYHOMEWORK
MYHOMEWORK_MIDDLEWARETOKEN,MYHOMEWORK_SECRET = MyHomework.login("MyHomeWorkUserName","MY HOMEWORK PASSWORRRDDDD")
MYHOMEWRK_COOKIES = "" + MYHOMEWORK_SECRET+ " " + MYHOMEWORK_MIDDLEWARETOKEN
MyHomework.MYHOMEWRK_COOKIES = MYHOMEWRK_COOKIES

#Setup CA connection
MySchoolApp.cookie = MySchoolApp.login("CA USERNAME","CA PASSSSSWORD")

#Get assignments active in our period through 7 days
classData = MySchoolApp.getAssignments(date.today().strftime("%m/%d/%Y"),(date.today() + timedelta(days=7)).strftime("%m/%d/%Y"))
#First let's nab the current page of myhomework. This is to make sure we don't duplicate.
#NOTICE: PLEAE ENABLE SHOW COMPLETED IN WEB AND DON'T UNCHECK
myHomeWorkAssignmentView = MyHomework.getAssignments()

#Now let's parse CA assignment data
for assignment in classData:
	status = assignment.assignment_status
	if status == -1 or status == 0: #Todo or inprogress
		#Format the groupname to remove unneeded data and increase entropy. The ID is a number and %1000 gives the last 3 digits
		assignmentClassTitle = assignment.groupname.split(" - ")[0] + " " + str(assignment.assignment_id % 1000)
		myHomeWorkAssignmentDisplayName = "[" + assignmentClassTitle + "] " + assignment.short_description
		myHomeWorkAssignmentDisplayName = myHomeWorkAssignmentDisplayName.strip()
		if myHomeWorkAssignmentDisplayName not in myHomeWorkAssignmentView:
			print("ADDING:" + myHomeWorkAssignmentDisplayName)
			#Build the date
			dateClean = assignment.date_due.split()[0]
			#Build the URL
			request = urllib2.Request("https://myhomeworkapp.com/homework/add")
			request.add_header('cookie',MYHOMEWRK_COOKIES)
			data="csrfmiddlewaretoken=" + MYHOMEWORK_MIDDLEWARETOKEN.replace("myhw_csrf=","") + "&title=" + myHomeWorkAssignmentDisplayName +"&cls=&type=0&due_date="+dateClean+"&due_time=&repeats=0&repeat_ends=&priority=3&reminder=&additional_info=" + str(assignment.long_description).replace("\\n","\n") + "&save=Save"
			res = urllib2.urlopen(url=request,data=data)
#		else:
			#print("DUPLICATE, SKIP: " + myHomeWorkAssignmentDisplayName)
			pass
#	else:
		#print("COMPLETED, SKIP: " + assignment.short_description)
		pass
#console.hud_alert("Done!")








