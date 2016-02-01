'''
Created on 1 Feb 2016

@author: michael
'''

class Grade(object):
   
    def __init__(self, title, date, grade):
        self.title = title
        self.grade = grade
        self.date = date
        
    def __str__(self):
        return "Assignment: " + self.title + " marked, grade: " + self.grade
