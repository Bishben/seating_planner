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
    
    for name, year, strength, expected in test_cases:
        branch = models.Branch(name, year, strength)
        if str(branch) != expected:
            return 0

    return 1

# Tests Runner 
def run_tests():
    failed = []

    if(test_room() != 1): failed.append("Room")
    if(test_branch() != 1): failed.append("Branch")
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


# COONVERT THESE INTO TEST FUNCTIONS --SEPERATE FOR EACH--  --FOLLOW NAMING CONVENTION--
# cy = Branch("CC", "24", 60)
# print (cy)

# print(branches[0].identity)

# cs = Branch("CS", "24", 120)
# print (cs)

# print(branches)
# print(branches[1].identity)

# math_cy = Exam("GMAT101", "10/12/24", "09:30", [cy, cs])
# print (math_cy)