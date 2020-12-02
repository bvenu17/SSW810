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
        self.assertEqual(uni.students_details["10183"].get_student_summary(
        ), ('10183', 'Musk, E', ['SSW 555', 'SSW 810'], ['SSW 540'], ['CS 501', 'CS 546'], 4.0))
        self.assertEqual(uni.instructor_details["98764"].get_instructor_summary(), [
                         ['98764', 'Cohen, R', 'SFEN', 'CS 546', 1]])
        self.assertEqual(uni.major_details['SFEN'].get_required_courses(), [
                         'SSW 540', 'SSW 810', 'SSW 555'])
        self.assertEqual(uni.major_details['SFEN'].get_elective_courses(), [
                         'CS 501', 'CS 546'])
        self.assertEqual(uni.student_grades_details_db("Student_Repository_Venugopal_Balaji.sqlite"), [('Bezos, J', '10115', 'SSW 810', 'A', 'Rowland, J'), ('Bezos, J', '10115', 'CS 546', 'F', 'Hawking, S'), ('Gates, B', '11714', 'SSW 810', 'B-', 'Rowland, J'), ('Gates, B', '11714', 'CS 546', 'A', 'Cohen, R'), (
            'Gates, B', '11714', 'CS 570', 'A-', 'Hawking, S'), ('Jobs, S', '10103', 'SSW 810', 'A-', 'Rowland, J'), ('Jobs, S', '10103', 'CS 501', 'B', 'Hawking, S'), ('Musk, E', '10183', 'SSW 555', 'A', 'Rowland, J'), ('Musk, E', '10183', 'SSW 810', 'A', 'Rowland, J')])


if __name__ == '__main__':
    unittest.main(exit=False, verbosity=1)
