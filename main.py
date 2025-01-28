import numpy as np
import datetime as dt
import test
import models

# Only Runs if ALL Tests have Passed
if(test.run_tests()): 
    def addBranches():
        branches_range = [] # ("24CC", '01', '10')
        while(True):
            branch = input("Enter Branch in format 'YYBB': ")

            check = 0
            for i in models.branches:
                if branch == models.branches[i].identity:
                    check = 1
                    break
            if (check == False):
                print("Branch Does Not Exist")
            else:
                branches_range.append(branch)
            
            cont = input("Add Another? (Y/N)")
            
    # Exam-Room : selection student
    class ExamRoom():
        def __init__(self, type, addBranches):
            self.type = type
            self.branches_range = addBranches