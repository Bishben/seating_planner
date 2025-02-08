from collections import defaultdict

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

def arrange(exam_room, subjs, offset_start = 0, diagonal = 0, copy = 0): # ExamRoom, list, Bool, Bool: Bool parameters indictate whether the settings are turned on or off 

    room = exam_room.room # Gets Room Matrix: [['_']] list of lists 
    i = 0 # indexing for subjs list

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
                exam_room.matrix[row][col] = exam_room.matrix[row][col-(columns-room.gap)]
                continue
            # Copy Off: Skips Gap if landed on gap
            elif((not copy) and (col == room.gap)):
                col += 2 if offset_start else 1

            # Handles Case if no element can be placed ; Skips position / Seat
            cur_pos = (row, col)
            next_called = 0

            while(True):

                # Checks if Current / Placing Element repeats on either left or right side
                col_check = any(
                    (0 <= (col + offset) < columns) and (exam_room.matrix[row][col + offset] == subjs[i][0])
                    for offset in (-2, 2)
                )

                # Checks if Current / Placing Element repeats on either top or bottom
                row_check = (not col_check) and any(
                    (0 <= (row + offset) < room.rows) and (exam_room.matrix[row + offset][col] == subjs[i][0])
                    for offset in (-1, 1)
                )

                # Checks if Current / Placing Element repeats on any of the Diagonal Sides
                diagonal_offsets = [(-1, 1), (-1, -1), (1, 1), (1, -1)] if offset_start else [(-1, 2), (-1, -2), (1, 2), (1, -2)] # Handles Diagonal Offset Change when start of placement is offset
                diagonal_check = (not row_check) and any(
                    (0 <= (row + row_offset) < room.rows) and (0 <= (col + col_offset) < columns) and
                    (exam_room.matrix[row + row_offset][col + col_offset] == subjs[i][0])
                    for row_offset, col_offset in diagonal_offsets
                )

                # IF Element Repeats Switch Element ELSE Place element
                if(col_check or row_check or (diagonal_check if diagonal != 0 else False)):
                    if(next_called == len(subjs)): break # If looped over all elements and none satisfy placement skip place / seat

                    i = next_sub(i, subjs) # Increments to Next Subject

                    if((row,col) == cur_pos):
                        next_called += 1
                else:
                    exam_room.matrix[row][col] = subjs[i][0] # Places Element
                    counts[subjs[i][0]] += 1 # Increments count of placed element
                    subjs[i] = (subjs[i][0], subjs[i][1]-1) # Deducts Amount of Available Element
                    i = rmv_sub(i, subjs) # Rmv Element if Amount is 0
                    break


    print(" ".join(f"{key}:{counts[key] * (2 if copy else 1)}" for key in counts))