#CPT: Insert Game Title Here
# Authors : Idara & Arun
# Course: ICS-3U
# Date: 2019/01/29

"""Unit testing in pygame is weird, I tried running a test case, and somehow, I have to add the rect information yet the program won't take them"""

# Imports
import unittest
import breakfastBattles

#class which tests all function in the program
class MyFileTest(unittest.TestCase):
    blueFlag = True
    rect.x = 0
    rect.y = 0
    #Functions beginning with "test_" will be tested
    def test_dropFlag(self):
        self.assertEqual(breakfastBattles.Player.dropFlag(self, "blue"), newBlueFlag)
        
    def test_(self):
        pass
        
#Main
if __name__ == "__main__":
    unittest.main()