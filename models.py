rooms = []
branches = []

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
    
    def __str__(self):
        return f"Code: {self.code} \nDate: {self.date} \nTime: {self.time}"
