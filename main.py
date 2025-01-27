areimport numpy as np
import datetime as dt

class Room:
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
    
    def __str__(self):
        rows = '_ ' * (self.columns // 2) + '  ' + '_ ' * (self.columns // 2)
        return (rows + '\n') * self.rows


# ('_ ' * columns + \n) * rows

# _ _ _ _ 
# _ _ _ _ 

type1 = Room(6, 10) # Including gap column + 1 
print(type1)

class Branch():
    def __init__(self, name, year, strength):
        self.name = name # String f:CS, CC, EE
        self.year = year # String f: 24, 23, 25, 'YY'
        self.strength = strength # Int

    def __str__(self):
        return f"Branch: {self.name} \nYear: 20{self.year} \nStrength: {self.strength}"

class Exam():
    def __init__(self, code, date, time, Branches):
        self.code = code # String "GMAT101"
        self.date = date # String f"dd/mm/yy"
        self.time = time # String f"xx:xx" 24 hr
        self.Branches = Branches
    
    def __str__(self):
        return f"Code: {self.code} \nDate: {self.date} \nTime: {self.time}"

cy = Branch("CC", "24", 60)
print (cy)

math_cy = Exam("GMAT101", "10/12/24", "09:30")
print (math_cy)

# 24 23 22 21
# 25 24 23 22
# 26 25 24 23