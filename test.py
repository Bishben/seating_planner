import models

# TEST ROOM
def test_room():
    type1 = models.Room(3, 4) # Including gap column + 1 
    text = "_ _   _ _ \n_ _   _ _ \n_ _   _ _ \n"

    if(str(type1) != text): return 0

    if(models.rooms[0].type != 1): return 0

    rooms = []
    return 1

# TEST BRANCH
def test_branch():
    test_cases = [
        ("CC", "24", 60, "Branch: 24CC\nStrength: 60\n"),
        ("CS", "23", 100, "Branch: 23CS\nStrength: 100\n"),
        ("EE", "25", 40, "Branch: 25EE\nStrength: 40\n")
    ]

    models.branches.clear()
    
    for name, year, strength, expected in test_cases:
        branch = models.Branch(name, year, strength)
        if str(branch) != expected:
            return 0
        
    if len(models.branches) != len(test_cases):
        return 0
    
    for i in range(len(test_cases)):
        expected_identity = test_cases[i][1] + test_cases[i][0]
        if models.branches[i].identity != expected_identity:
            return 0 
    
    models.branches = []
    return 1

# Test Exams
def test_exam():
    test_cases = [
        ("CC", "24", 60),
        ("CS", "23", 100)]
    
    CC = models.Branch(test_cases[0][0], test_cases[0][1], test_cases[0][2])
    CS = models.Branch(test_cases[1][0], test_cases[1][1], test_cases[1][2])
    
    math = models.Exam("GMAT101","22/11/2003","09:30",[CC,CS])
    
    expectedBranches = [CC,CS] 
    expectedStr = f"Code: GMAT101\nDate: 22/11/2003\nTime: 09:30\nBranches: {expectedBranches}"
    
    if str(math) != expectedStr:
        return 0
    
    models.branches = []
    models.exams = []
    return 1

# Test ExamRoom
def test_examRoom():
    test_cases = [
        ("CC", "24", 60),
        ("CS", "23", 100),
        ("EE", "25", 40)
    ]
    
    CC = models.Branch(test_cases[0][0], test_cases[0][1], test_cases[0][2])
    CS = models.Branch(test_cases[1][0], test_cases[1][1], test_cases[1][2])
    EE = models.Branch(test_cases[2][0], test_cases[2][1], test_cases[2][2])

    type1 = models.Room(3, 4)
    
    math = models.Exam("GMAT101", "29/12/2003", "09:30", [CC, CS])
    chem = models.Exam("CHEM101", "30/12/2003", "09:30", [CC, CS])
    math2 = models.Exam("GMAT201", "30/12/2003", "09:30", [EE])
    chem2 = models.Exam("CHEM201", "29/12/2003", "09:30", [EE])

    room707 = models.ExamRoom(1, 707, [('23CS', 0, 10), ('24CC', 0, 5), ('25EE', 30, 40)])
    expected = "Type: 1\nNumber: 707\nBranches: [('23CS', 0, 10), ('24CC', 0, 5), ('25EE', 30, 40)]\n"

    if(str(room707) != expected): return 0

    models.exams = []
    models.rooms = []
    models.branches = []
    return 1

# Tests Runner 
def run_tests():
    failed = []

    if(test_room() != 1): failed.append("Room")
    if(test_branch() != 1): failed.append("Branch")
    if(test_exam() != 1): failed.append("Exam") 
    if(test_examRoom() != 1): failed.append("ExamRoom")
    # ADD OTHER TEST CASES HERE


    # If failed[] has no elemtents; there are no failed tests
    if(len(failed)  != 0):
        fail_text = "Failed Test Objects: "
        for i in failed:
            fail_text += (i + " ")
        print(fail_text)
        return 0

    print("All Test Cases Passed")
    return 1