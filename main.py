import numpy as np
import datetime as dt
import test
import models

# Room(self, rows, columns)
# Branch(self, name, year, strength)
# Exam(self, code, date, time, Branches)
# ExamRoom(self, type, number, addBranches)

def arrange(exam_room):
    

# Only Runs if ALL Tests have Passed
if(test.run_tests()): 
    print("...")