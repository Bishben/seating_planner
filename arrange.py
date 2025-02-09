from collections import defaultdict
from itertools import permutations


def auto_arrange(exam_room, subjs, copy = 0):
    room = exam_room.room

    def find_best_case(offset_start, diagonal, copy=0):
        best_case = {"total": 0}
        for perm in [list(perm) for perm in permutations(subjs)]:
            exam_room.clear()
            seating = arrange(exam_room, perm, offset_start, diagonal, copy)
            if seating["total"] > best_case["total"]:
                best_case = seating
        return best_case

    if(copy):
        best_case_copy = find_best_case(0, 0, 1)
        subjs_permutations_copy = [list(perm) for perm in permutations(subjs)]
        del best_case_copy["matrix"]
        print(" ".join(f"{key}:{best_case_copy[key]}" for key in best_case_copy))
        return best_case_copy


    best_case_offset = find_best_case(1, 1)
    best_case_default = find_best_case(0,1)

    best_case = best_case_offset if best_case_offset["total"] >= best_case_default["total"] else best_case_default
    
    exam_room.matrix = best_case["matrix"]
    del best_case["matrix"]
    print(" ".join(f"{key}:{best_case[key]}" for key in best_case))
    return best_case

# Main Function that Arranges The ExamRoom Matrix
def arrange(exam_room, subjs, offset_start = 0, diagonal = 0, copy = 0): # ExamRoom, list, Bool, Bool: Bool parameters indictate whether the settings are turned on or off 

    # Increments to the next sub and return to first sub if out of index
    def next_sub(i, subjs): # index, list: index of list, list of subjects f[("A", 14), ("B", 14),]
        if(i >= len(subjs)-1):
            return 0
        
        return i + 1

    # Removes a subject if the the amount of students are 0
    def rmv_sub(i, subjs): # index, list: index of list, list of subjects f[("A", 14), ("B", 14),]
        last = len(subjs)-1
        
        if(subjs[i][1] == 0):
            subjs.pop(i)
            if(i == last): return 0

        return i
    

    room = exam_room.room # Gets Room Matrix: [['_']] list of lists 
    i = 2 # indexing for subjs list

    columns = room.columns+1 if room.gap else room.columns # Handles Matrix Columns Amount if Gap is Added

    # Forces Copy Settings
    if(copy):
        offset_start = 0
        diagonal = 0

    # Count for returning how many of each elements were placed
    counts = defaultdict(int)

    for row in range(room.rows):

        start_col = ((0 if row%2 == 0 else 1) if offset_start else 0) # Offsets every odd indexed row if turned on

        for col in range(start_col, columns, 2):

            # Copy On: Copies Element from Corresponding Left
            if((copy) and (col >= (room.gap if room.gap else col // 2))):
                sub = exam_room.matrix[row][col-(columns-room.gap)][:-2]
                roll = f"{sub}{counts[subjs[i][0]]+1:02}"
                exam_room.matrix[row][col] = roll
                counts[sub] += 1
                continue
            # Copy Off: Skips Gap if landed on gap
            elif((not copy) and (col == room.gap)):
                continue

            # Handles Case if no element can be placed ; Skips position / Seat
            cur_pos = (row, col)
            next_called = 0

            while(True):

                # Checks if Current / Placing Element repeats on either left or right side
                col_check = any(
                    (0 <= (col + offset) < columns) and (exam_room.matrix[row][col + offset][:-2] == subjs[i][0])
                    for offset in (-2, 2)
                )

                # Checks if Current / Placing Element repeats on either top or bottom
                row_check = (not col_check) and any(
                    (0 <= (row + offset) < room.rows) and (exam_room.matrix[row + offset][col][:-2] == subjs[i][0])
                    for offset in (-1, 1)
                )

                # Checks if Current / Placing Element repeats on any of the Diagonal Sides
                diagonal_offsets = [(-1, 1), (-1, -1), (1, 1), (1, -1)] if offset_start else [(-1, 2), (-1, -2), (1, 2), (1, -2)] # Handles Diagonal Offset Change when start of placement is offset
                diagonal_check = (not row_check) and any(
                    (0 <= (row + row_offset) < room.rows) and (0 <= (col + col_offset) < columns) and
                    (exam_room.matrix[row + row_offset][col + col_offset][:-2] == subjs[i][0])
                    for row_offset, col_offset in diagonal_offsets
                )

                # IF Element Repeats Switch Element ELSE Place element
                if(col_check or row_check or (diagonal_check if diagonal != 0 else False)):
                    if(next_called == len(subjs)): break # If looped over all elements and none satisfy placement skip place / seat

                    i = next_sub(i, subjs) # Increments to Next Subject

                    if((row,col) == cur_pos):
                        next_called += 1
                else:
                    roll = f"{subjs[i][0]}{counts[subjs[i][0]]+1:02}"
                    exam_room.matrix[row][col] = roll # Places Element
                    subjs[i] = (subjs[i][0], subjs[i][1]-1) # Deducts Amount of Available Element
                    counts[subjs[i][0]] += 1
                    i = rmv_sub(i, subjs) # Removes Element if Amount is 0
                    break

    counts = counts | {"total": sum(counts.values())}
    # print(" ".join(f"{key}:{counts[key]}" for key in counts))
    counts = {"matrix":exam_room.matrix} | counts
    return counts