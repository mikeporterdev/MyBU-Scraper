'''
Created on 1 Feb 2016

@author: michael
'''

class Grade(object):
   
    def __init__(self, title, date, grade):
        self.title = title
        self.grade = grade
        self.date = date
        
    def toString(self):
        print("Assignment: " + self.title + " marked, grade: " + self.grade)