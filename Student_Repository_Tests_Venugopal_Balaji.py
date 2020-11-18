"""
@author: Venugopal Balaji CWID: 10446195
this class is used to create unit tests for all the functions
"""
import unittest
from typing import List, Any, Tuple
from Student_Repository_Venugopal_Balaji import University

class TestFraction(unittest.TestCase):
    """Class for testing  the university class"""

    def test_university(self):
        """function to test the univerity class"""
        uni: University = University(r"Files")
        self.assertEqual(uni.students_details["11714"].get_student_summary(), ('11714', 'Morton, A', ['SYS 611','SYS 645']))
        self.assertEqual(uni.students_details["10172"].get_student_summary(), ('10172', 'Forbes, I', ['SSW 555','SSW 567']))
        self.assertEqual(uni.instructor_details["98765"].get_instructor_summary(), ([['98765', 'Einstein, A', 'SFEN', 'SSW 567', 4], ['98765', 'Einstein, A', 'SFEN', 'SSW 540', 3]]))
        self.assertNotEqual(uni.instructor_details["98765"].get_instructor_summary(), ([['98763', 'Newton, I', 'SFEN', 'SSW 567', 1]]))

if __name__ == '__main__':
    unittest.main(exit=False, verbosity=1)

