'''
Created on 1 Feb 2016

@author: MichaelPorter
'''

import http
from lxml import html
import re
import requests
import time
import urllib
import settings

payload = {
           "user_id" : settings.settings['mybu_user'],
           "password" : settings.settings['mybu_pass']
           }

course_id = "48041"

login_url = "https://mybu.bournemouth.ac.uk/webapps/login/"
gradeurl = 'https://mybu.bournemouth.ac.uk/webapps/bb-mygrades-bb_bb60/myGrades?course_id=_' + course_id + '_1&stream_name=mygrades&is_stream=false'
     
def getGrades():
    with requests.Session() as s:
        s.post(login_url, data=payload)
        gradetext = s.get(gradeurl)
        
        return gradetext.text
    
def checkGrade():
    tree = html.fromstring(getGrades())
    bucket_elems = tree.findall(".//div[@id='grades_wrapper']")
    bucket_names = [bucket_elem.text_content().replace("\n", "").strip() for bucket_elem in bucket_elems]
    
    t = re.split(r'\s{2,}', bucket_names[0])
    
    if len(t) > 4:
        if settings.pushoverSettings['usePushover']:
            sendPush(bucket_names[0])
        else:
            print("Grades are up!")
            print(t)
      
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
    