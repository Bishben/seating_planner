rooms = []
branches = []
exams = []

class Room:
    def __init__(self, rows, columns, gap=0):
        self.rows = rows # int: rows in room
        self.columns = columns # int: columns in room
        self.gap = gap # int: specifies where gap is after
        self.type = len(rooms) + 1 # int: assigning a type number
        self.matrix = [["_"] * gap + [" "] + ["_"] * (columns-gap) for _ in range(rows)] if (gap!=0) else [["_"] * columns for _ in range(rows)] # list[list]: list of lists depicting rows and columns (columns x rows filled with '_')
        rooms.append(self)
    
    def __str__(self):
        return "\n".join(" ".join(row) for row in self.matrix)
    
class Branch():
    def __init__(self, name, year, strength):
        self.name = name # string: f CS, CC, EE
        self.year = year # string: f 24, 23, 25, 'YY'
        self.strength = strength # int: total number of students
        self.identity = year + name # string: concatenates year and name of branch to form unique identity
        branches.append(self)

    def __str__(self):
        return f"Branch: {self.identity}\nStrength: {self.strength}\n"

class Exam():
    def __init__(self, code, date, time, Branches):
        self.code = code # string: code of examination f"GMAT101"
        self.date = date # string: date of examination f"dd/mm/yy"
        self.time = time # string: time of examination f"xx:xx" 24 hr
        self.Branches = Branches # list: list of Object Branch that have this examination f[<&cs> , <&ce>]
        exams.append(self)
    
    def __str__(self):
        return f"Code: {self.code}\nDate: {self.date}\nTime: {self.time}\nBranches: {self.Branches}"
    
# Exam-Room

# Creates branches_range by adding Multiple Object Branch through User Input
def addBranches():     
    branches_range = [] # ("GMAT101", "24CC", '01', '10')
    while(True):
        for i in exams:
            print (i.code, end = " ")
        code = input("\nSelect A Subject/Exam Code in f'GMAT101': ").strip().upper()
        exam = find_exam_by_code(code)
        for i in exam.Branches:
            print (i.identity, end = " ")
        branch = input("\nSelect Branch in f'YYBB': ")
        start = int(input("Enter Start Roll No f(int): "))
        end = int(input("Enter End Roll No f(int): "))

        branches_range.append((code, branch, start, end))
        
        cont = input("Add Another? (Y/N)")
        if (cont != 'Y'): break
    return branches_range

# Finds exam by code(string) of exam by user input
def find_exam_by_code(code):
    for exam in exams:
        if(exam.code == code):
            return exam
    return None
        
class ExamRoom():
    def __init__(self, room, number, addBranches):
        self.room = room # Room: Object of Class Room
        self.number = number # int: room number
        self.matrix = room.matrix # list[list]: list of lists depicting rows and columns
        self.branches_range = addBranches # list: list of exams-branches-startRoll-endRoll occuring in ExamRoom f[("GMAT101", '23CS', 0, 10),]

    def displayInfo(self):
        return f"Type: {self.type}\nNumber: {self.number}\nBranches: {self.branches_range}\n"
    
    def __str__(self):
        return "\n".join(" ".join(row) for row in self.matrix)