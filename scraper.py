'''
Created on 1 Feb 2016

@author: MichaelPorter
'''
import http
from lxml import html
from lxml.html import tostring
import re
import requests
import time
import urllib

from grade import Grade
import settings


payload = {
           "user_id" : settings.settings['mybu_user'],
           "password" : settings.settings['mybu_pass']
           }

#48037
#48041
course_id = "48037"

login_url = "https://mybu.bournemouth.ac.uk/webapps/login/"
gradeurl = 'https://mybu.bournemouth.ac.uk/webapps/bb-mygrades-bb_bb60/myGrades?course_id=_' + course_id + '_1&stream_name=mygrades&is_stream=false'
     
def getGrades():
    with requests.Session() as s:
        s.post(login_url, data=payload)
        gradetext = s.get(gradeurl)
        
        return gradetext.text
    
def parseGrades(uglyGrades):
    grades = []
    for uglyGrade in uglyGrades:
        title = uglyGrade.find_class('gradable')[0].text_content().replace("\n", "").strip()
        gradedDate = uglyGrade.find_class('lastActivityDate')[0].text_content().replace("\n", "").strip()
        mark = uglyGrade.findall(".//span[@class='grade']")[0].text_content()
        
        grades.append(Grade(title, gradedDate, mark))
        
    for gr in grades:
        gr.toString()
    
def checkGrade():
    tree = html.fromstring(getGrades())
    bucket_elems = tree.find_class('graded_item_row')
    
    parseGrades(bucket_elems)
    
    
    
    uglyGrades = [bucket_elem.text_content().replace("\n", "").strip() for bucket_elem in bucket_elems]
    
    grades = []
    
    for uglyGrade in uglyGrades:
        grades.append(re.split(r'\s{2,}', uglyGrade))
    
    if len(grades) > 0:
        if settings.pushoverSettings['usePushover']:
            sendPush(uglyGrades[0])
        else:
            #print("Grades are up!")
            #print(grades)
            pass

def sendPush(grades):
    conn = http.client.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json",
    urllib.parse.urlencode({
                            "token": settings.pushoverSettings['pushover_token'],
                            "user": settings.pushoverSettings['pushover_user_api'],
                            "message": grades,
                            }), { "Content-type": "application/x-www-form-urlencoded" })
    conn.getresponse()
  
if __name__ == '__main__':
    while True:
        checkGrade()
        time.sleep(5)
    