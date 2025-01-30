rooms = []
branches = []
exams = []

class Room:
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.type = len(rooms) + 1 # Room Type 1, Room Type 2
        #self.matrix = [['_' * columns] * rows]]
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
        return f"Code: {self.code}\nDate: {self.date}\nTime: {self.time}\nBranches: {self.Branches}"
    
# Exam-Room Under Development
def addBranches():     
    branches_range = [] # ("24CC", '01', '10')
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

        branches_range.append((branch, start, end))
        
        cont = input("Add Another? (Y/N)")
        if (cont != 'Y'): break
    return branches_range

def find_exam_by_code(code):
    for exam in exams:
        if(exam.code == code):
            return exam
    return None
        
class ExamRoom():
    def __init__(self, type, number, addBranches):
        self.type = type
        self.number = number
        self.branches_range = addBranches

    def __str__(self):
        return f"Type: {self.type}\nNumber: {self.number}\nBranches: {self.branches_range}\n"