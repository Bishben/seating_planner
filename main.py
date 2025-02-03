import numpy as np
import datetime as dt
import test
import models
from collections import defaultdict

# Room(self, rows, columns)
# Branch(self, name, year, strength)
# Exam(self, code, date, time, Branches)
# ExamRoom(self, type, number, addBranches)


def next_sub(i, subjs): # index, list: index of list, list of subjects f["A", "B"]
    next = i
    empty = True

    for sub, amt in subjs:
        if(amt > 0):
            empty = False
            break

    if(empty): return -1

    if(i == len(subjs)-1):
        next = 0
    else:
        next += 1

    if(subjs[next][1] == 0):
        next += 1
    
    return next

def arrange(exam_room, subjs):

    room = exam_room.room
    empty = False
    i = 0

    # count_a = 0
    # count_b = 0
    # count_c = 0
    # count_d = 0 --! IMPROVED BELOW !--
    subj_counts = defaultdict(int)

    invert_start = 0
    
    for row in range(room.rows):
        if(empty): break
        start_col = ((0 if row%2 == 0 else 1) if invert_start else 0)
        for col in range(start_col, room.columns+1, 2):
            if(empty): break
            if(col == room.gap):
                col += 2 if invert_start else 1
            cur_pos = (row, col)
            next_called = 0
            while(True):
                # col_check_right = (col + 2 < room.columns) and (exam_room.matrix[row][col + 2] == subjs[i]) 
                # col_check_left = (col - 2 >= 0) and (exam_room.matrix[row][col - 2] == subjs[i])
                # col_check = col_check_right or col_check_left --! IMPROVED BELOW !--
                col_check = any(
                    (0 <= (col + offset) <= room.columns) and (exam_room.matrix[row][col + offset] == subjs[i][0])
                    for offset in (-2, 2)
                )

                # row_check_bottom = (row + 1 < room.rows) and (exam_room.matrix[row + 1][col] == subjs[i]) 
                # row_check_top = (row - 1 >= 0) and (exam_room.matrix[row - 1][col] == subjs[i])
                # row_check = row_check_bottom or row_check_top --! IMPROVED BELOW !--
                row_check = any(
                    (0 <= row + offset < room.rows) and (exam_room.matrix[row + offset][col] == subjs[i][0])
                    for offset in (-1, 1)
                )

                # top_right = ((row - 1 >= 0) and (col + 1 <= room.columns)) and (exam_room.matrix[row-1][col + 1] == subjs[i]) 
                # top_left = ((row - 1 >= 0) and (col - 1 >= 0)) and (exam_room.matrix[row-1][col - 1] == subjs[i])
                # bottom_right = ((row + 1 < room.rows) and (col + 1 <= room.columns)) and (exam_room.matrix[row+1][col + 1] == subjs[i])
                # bottom_left = ((row + 1 < room.rows) and (col - 1 >= 0)) and (exam_room.matrix[row+1][col - 1] == subjs[i])
                # diagnol_check = top_right or top_left or bottom_right or bottom_left #--! IMPROVED BELOW !--
                if(invert_start):
                    diagnol_check = any(
                        (0 <= (row + row_offset) < room.rows) and (0 <= (col + col_offset) <= room.columns) and
                        (exam_room.matrix[row + row_offset][col + col_offset] == subjs[i][0])
                        for row_offset, col_offset in [(-1, 1), (-1, -1), (1, 1), (1, -1)]
                    )
                else:
                    diagnol_check = any(
                        (0 <= (row + row_offset) < room.rows) and (0 <= (col + col_offset) <= room.columns) and
                        (exam_room.matrix[row + row_offset][col + col_offset] == subjs[i][0])
                        for row_offset, col_offset in [(-1, 2), (-1, -2), (1, 2), (1, -2)]
                    )

                diagnol = 0

                if(col_check or row_check or (diagnol_check if diagnol != 0 else False)):
                    if(next_called == len(subjs)): break

                    i = next_sub(i, subjs)

                    if (i == -1): empty = True
                    if(empty): break

                    if((row,col) == cur_pos):
                        next_called += 1
                else:
                    exam_room.matrix[row][col] = subjs[i][0]
                    # match subjs[i]: --! IMPROVED BELOW !--
                    #     case "A":
                    #         count_a += 1
                    #     case "B":
                    #         count_b += 1
                    #     case "C":
                    #         count_c += 1
                    #     case "D":
                    #         count_d += 1    
                    subjs[i] = (subjs[i][0], subjs[i][1]-1)
                    subj_counts[subjs[i][0]] += 1
                    break

    
    print(f"A:{subj_counts.get('A', 0)}  B:{subj_counts.get('B', 0)}  C:{subj_counts.get('C', 0)}   D: {subj_counts.get('D', 0)}")



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

    type1 = models.Room(6, 10, 5)
    print(type1)
    print("\n")
    math = models.Exam("GMAT101", "29/12/2003", "09:30", [CC, CS])
    chem = models.Exam("CHEM101", "30/12/2003", "09:30", [CC, CS])
    math2 = models.Exam("GMAT201", "30/12/2003", "09:30", [EE])
    chem2 = models.Exam("CHEM201", "29/12/2003", "09:30", [EE])

    room707 = models.ExamRoom(type1, 707, [("GMAT101", '23CS', 0, 10), ("GMAT101", '24CC', 0, 5), ("CHEM201", '25EE', 30, 40)])
    arrange(room707, [("A", 10), ("B", 10)])
    print (room707)

    #('24CC', 1, 20), ('25EE', 15, 30)