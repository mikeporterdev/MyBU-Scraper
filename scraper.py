'''
Created on 1 Feb 2016

@author: MichaelPorter
'''
from datetime import datetime
import http
from lxml import html
import requests
import time
import urllib

from grade import Grade
import settings


payload = {
           "user_id" : settings.settings['mybuUser'],
           "password" : settings.settings['mybuPass']
           }

LOGIN_URL = "https://mybu.bournemouth.ac.uk/webapps/login/"

GRADE_URL_START = 'https://mybu.bournemouth.ac.uk/webapps/bb-mygrades-bb_bb60/myGrades?course_id=_'
GRADE_URL_END = '_1&stream_name=mygrades&is_stream=false'

gradeTitles = []
     
def getGrades():
    with requests.Session() as s:
        s.post(LOGIN_URL, data=payload)
        
        grades = []
        
        for courseId in settings.settings['courseIds']:
            grades.append(s.get(GRADE_URL_START + courseId + GRADE_URL_END))
        
        return grades
    
def parseGrades(uglyGrades):
    grades = []
    for uglyGrade in uglyGrades:
        gradedDate = uglyGrade.find_class('lastActivityDate')[0].text_content().replace("\n", "").strip()
        gradedDate = datetime.strptime(gradedDate, '%d-%b-%Y %H:%M')
        title = uglyGrade.find_class('gradable')[0].text_content().replace("\n", "").strip()
        mark = uglyGrade.findall(".//span[@class='grade']")[0].text_content()
        
        if gradedDate.date() == datetime.today().date() and title not in gradeTitles:    
            gradeTitles.append(title)
            grades.append(Grade(title, gradedDate, mark))
        
    return grades
    
def checkGrade():
    for returnedGrades in getGrades():
        tree = html.fromstring(returnedGrades.text)
        bucket_elems = tree.find_class('graded_item_row')
        
        grades = parseGrades(bucket_elems)
    
        if len(grades) > 0:
            message = [str(grade) for grade in grades]    
            if settings.pushoverSettings['usePushover']:
                sendPush(message)
            else:
                print("Grades are up!")
                print(message)

def sendPush(message):
    conn = http.client.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json",
    urllib.parse.urlencode({
                            "token": settings.pushoverSettings['pushoverToken'],
                            "user": settings.pushoverSettings['pushoverUserApiKey'],
                            "message": message,
                            }), { "Content-type": "application/x-www-form-urlencoded" })
    conn.getresponse()
  
if __name__ == '__main__':
    while True:
        checkGrade()
        time.sleep(5)
    