import models

#ROOM Test
def test_room():
    type1 = models.Room(3, 4) # Including gap column + 1 
    text = "_ _   _ _ \n_ _   _ _ \n_ _   _ _ \n"

    if(str(type1) != text): return 0

    if(models.rooms[0].type != 1): return 0

    return 1

#ADD TEST FUNCTIONS HERE --CHECK END AND CONVERT--

#example
def test_branch():
    cy = models.Branch("CC", "24", 60) #change up parameters to random params
    print (cy) #check what this should return comparing models.py and using condtion return 0 if false 

# Tests Runner 
def run_tests():
    failed = []

    if(test_room() != 1): failed.append("Room")
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