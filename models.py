rooms = []
branches = []
exams = []

class Room:
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.type = len(rooms) + 1 # Room Type 1, Room Type 2
        rooms.append(self)
    
    def __str__(self):
        rows = '_ ' * (self.columns // 2) + '  ' + '_ ' * (self.columns // 2)
        return (rows + '\n') * self.rows
    
class Branch():
    def __init__(self, name, year, strength):
        self.name = name # String f:CS, CC, EE
        self.year = year # String f: 24, 23, 25, 'YY'
        self.strength = strength # Int
        self.identity = year + name
        branches.append(self)

    def __str__(self):
        return f"Branch: {self.identity}\nStrength: {self.strength}\n"

class Exam():
    def __init__(self, code, date, time, Branches):
        self.code = code # String "GMAT101"
        self.date = date # String f"dd/mm/yy"
        self.time = time # String f"xx:xx" 24 hr
        self.Branches = Branches
        exams.append(self)
    
    def __str__(self):
        return f"Code: {self.code} \nDate: {self.date} \nTime: {self.time}"
    
# Exam-Room Under Development
def addBranches():     
    branches_range = [] # ("24CC", '01', '10')
    while(True):
        for i in exams:
            print (i.code, end = " ")
        exam = input("\nSelect A Subject/Exam Code in f'GMAT101': ")
        for i in exam.Branches:
            print (i.code, end = " ")
        branch = input("Select Branch in f'YYBB': ")
        start = int(input("Enter Start Roll No f(int): "))
        end = int(input("Enter End Roll No f(int): "))

        branches_range.append((branch, start, end))
        
        cont = input("Add Another? (Y/N)")
        if (cont != 'Y'): break
    return branches_range
        
class ExamRoom():
    def __init__(self, type, addBranches):
        self.type = type
        self.branches_range = addBranches
