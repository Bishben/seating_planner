import numpy as np
import datetime as dt
import test
import models
from collections import defaultdict

# Room(self, rows, columns)
# Branch(self, name, year, strength)
# Exam(self, code, date, time, Branches)
# ExamRoom(self, type, number, addBranches)


def next_sub(i, subjs): # index, list: index of list, list of subjects f[("A", 14), ("B", 14),]

    for s in range(len(subjs)):
        if(subjs[s][1] == 0):
            subjs.pop(s)

    # if(empty): return -1

    if(i >= len(subjs)-1):
        return 0
    
    return i + 1

def rmv_sub(i, subjs):
    last = len(subjs)-1
    
    if(subjs[i][1] == 0):
        subjs.pop(i)
        if(i == last): return 0

    return i

def arrange(exam_room, subjs, offset_start = 0, diagonal = 0):

    room = exam_room.room
    i = 0

    columns = room.columns+1 if room.gap else room.columns

    count_a = 0
    count_b = 0
    count_c = 0
    count_d = 0 #--! IMPROVED BELOW !--
    # subj_counts = defaultdict(int)
    
    for row in range(room.rows):
        start_col = ((0 if row%2 == 0 else 1) if offset_start else 0)
        for col in range(start_col, columns, 2):
            if(col == room.gap):
                col += 2 if offset_start else 1
            cur_pos = (row, col)
            next_called = 0
            while(True):

                col_check = any(
                    (0 <= (col + offset) < columns) and (exam_room.matrix[row][col + offset] == subjs[i][0])
                    for offset in (-2, 2)
                )

                row_check = (not col_check) and any(
                    (0 <= (row + offset) < room.rows) and (exam_room.matrix[row + offset][col] == subjs[i][0])
                    for offset in (-1, 1)
                )

                if(offset_start):
                    diagonal_check = any(
                        (0 <= (row + row_offset) < room.rows) and (0 <= (col + col_offset) < columns) and
                        (exam_room.matrix[row + row_offset][col + col_offset] == subjs[i][0])
                        for row_offset, col_offset in [(-1, 1), (-1, -1), (1, 1), (1, -1)]
                    )
                else:
                    diagonal_check = any(
                        (0 <= (row + row_offset) < room.rows) and (0 <= (col + col_offset) < columns) and
                        (exam_room.matrix[row + row_offset][col + col_offset] == subjs[i][0])
                        for row_offset, col_offset in [(-1, 2), (-1, -2), (1, 2), (1, -2)]
                    )

                if(col_check or row_check or (diagonal_check if diagonal != 0 else False)):
                    if(next_called == len(subjs)): break

                    i = next_sub(i, subjs)

                    if((row,col) == cur_pos):
                        next_called += 1
                else:
                    exam_room.matrix[row][col] = subjs[i][0]
                    match subjs[i][0]: #--! IMPROVED BELOW !--
                        case "A":
                            count_a += 1
                        case "B":
                            count_b += 1
                        case "C":
                            count_c += 1
                        case "D":
                            count_d += 1    
                    subjs[i] = (subjs[i][0], subjs[i][1]-1)
                    i = rmv_sub(i, subjs)
                    #subj_counts[subjs[i][0]] += 1
                    break

    
    print(f"A:{count_a}  B:{count_b}  C:{count_c}   D: {count_d}")



# Only Runs if ALL Tests have Passed
if(test.run_tests()): 
    print("...")
    test_cases = [
        ("CC", "24", 60),
        ("CS", "23", 100),
        ("EE", "25", 40)
    ]
    CC = models.Branch(test_cases[0][0], test_cases[0][1], test_cases[0][2])
    CS = models.Branch(test_cases[1][0], test_cases[1][1], test_cases[1][2])
    EE = models.Branch(test_cases[2][0], test_cases[2][1], test_cases[2][2])

    type1 = models.Room(7, 5)
    print(type1)
    print("\n")
    math = models.Exam("GMAT101", "29/12/2003", "09:30", [CC, CS])
    chem = models.Exam("CHEM101", "30/12/2003", "09:30", [CC, CS])
    math2 = models.Exam("GMAT201", "30/12/2003", "09:30", [EE])
    chem2 = models.Exam("CHEM201", "29/12/2003", "09:30", [EE])

    room707 = models.ExamRoom(type1, 707, [("GMAT101", '23CS', 0, 10), ("GMAT101", '24CC', 0, 5), ("CHEM201", '25EE', 30, 40)])
    arrange(room707, [("A", 14), ("B", 14), ("C", 8), ("D", 6)], 1, 1)
    print (room707)

    #('24CC', 1, 20), ('25EE', 15, 30)