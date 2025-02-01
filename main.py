import numpy as np
import datetime as dt
import test
import models

# Room(self, rows, columns)
# Branch(self, name, year, strength)
# Exam(self, code, date, time, Branches)
# ExamRoom(self, type, number, addBranches)

# 

def arrange(exam_room, exam_type):

    room = exam_room.room
    temp = exam_room.matrix

    for col in range(0, room.columns, 2):  # Step of 2 ensures spacing
        row, current_col = 0, col
        while row < room.rows and current_col < room.columns:
            if exam_room.matrix[row][current_col] == "_":
                exam_room.matrix[row][current_col] = exam_type
            row += 2  # Step of 2 ensures spacing
            current_col += 2
    
    exam_room.matrix = temp

# Only Runs if ALL Tests have Passed
if(test.run_tests()): 
    print("...")
    test_cases = [
        ("CC", "24", 60),
        ("CS", "23", 100),
        ("EE", "25", 40)
    ]
    print("\n\n")
    CC = models.Branch(test_cases[0][0], test_cases[0][1], test_cases[0][2])
    CS = models.Branch(test_cases[1][0], test_cases[1][1], test_cases[1][2])
    EE = models.Branch(test_cases[2][0], test_cases[2][1], test_cases[2][2])

    type1 = models.Room(6, 10)
    print(type1)
    print("\n\n")
    math = models.Exam("GMAT101", "29/12/2003", "09:30", [CC, CS])
    chem = models.Exam("CHEM101", "30/12/2003", "09:30", [CC, CS])
    math2 = models.Exam("GMAT201", "30/12/2003", "09:30", [EE])
    chem2 = models.Exam("CHEM201", "29/12/2003", "09:30", [EE])

    room707 = models.ExamRoom(type1, 707, [("GMAT101", '23CS', 0, 10), ("GMAT101", '24CC', 0, 5), ("CHEM201", '25EE', 30, 40)])
    print (room707)
    print("\n\n")

    #('24CC', 1, 20), ('25EE', 15, 30)