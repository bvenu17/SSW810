"""
@author: Venugopal Balaji CWID: 10446195
this program consists of classes which contains all information about the students and instructors
"""
import os as os
from typing import IO, DefaultDict, List, Any, Dict, Optional, Set, Tuple
from collections import defaultdict, Counter
from datetime import datetime, timedelta
from prettytable import PrettyTable
from HW08_Venugopal_Balaji import file_reader


class Students:
    """class to store the details of the student"""

    def __init__(self, cwid: str, name: str, major: str) -> None:
        """funtion to initialize constructor"""
        self.cwid: str = cwid
        self.name: str = name
        self.major: str = major
        self.allCourses: Dict[str, str] = dict()
        self.get_student_summary()

    def add_grade(self, course: str, grade: str) -> None:
        """function to add grade of student of each course"""
        self.allCourses[course] = grade

    def get_student_summary(self) -> Tuple[str, str, list]:
        """return the summary of student details for pretty table"""
        courses: List[str] = sorted(list(self.allCourses.keys()))
        return self.cwid, self.name, courses


class Instructors:
    """class to store the details of the instructor"""

    def __init__(self, cwid: str, name: str, department: str) -> None:
        """funtion to initialize constructor"""
        self.cwid: str = cwid
        self.name: str = name
        self.department: str = department
        self.course_count: Dict[str, int] = defaultdict(int)

    def cnt_students(self, course: str) -> None:
        """count the number of students in a course"""
        self.course_count[course] += 1

    def get_instructor_summary(self) -> list:
        """returns the summary of instructors for pretty table"""
        instructor_summary: List = list()
        for key, values in self.course_count.items():
            instructor_summary.append(
                [self.cwid, self.name, self.department, key, values])
        return instructor_summary


class University:
    def __init__(self, directory: str) -> None:
        """funtion to initialize constructor"""
        self.directory: str = directory
        self.students_details: Dict[str, Students] = dict()
        self.instructor_details: Dict[str, Instructors] = dict()
        self.get_student_details(os.path.join(self.directory, "students.txt"))
        self.get_instructor_details(os.path.join(
            self.directory, 'instructors.txt'))
        self.get_grades_details(os.path.join(self.directory, 'grades.txt'))

    def get_student_details(self, path: str) -> None:
        """reads the student file"""
        try:
            for cwid, name, major in file_reader(path, 3, '\t', False):
                self.students_details[cwid] = Students(cwid, name, major)
        except(FileNotFoundError) as e:
            print(e)

    def get_grades_details(self, path: str) -> None:
        """reads the grades file"""
        try:
            for student_cwid, course, grade, instructor_cwid in file_reader(path, 4, '\t', False):
                try:
                    self.students_details[student_cwid].add_grade(
                        course, grade)
                    self.instructor_details[instructor_cwid].cnt_students(
                        (course))
                except(KeyError):
                    print("Key details not found")
        except(FileNotFoundError, ValueError) as e:
            print(e)

    def get_student_table(self) -> None:
        """to display the summary of student details"""
        stable: PrettyTable = PrettyTable(
            field_names=["CWID", "Name", "Completed Courses"])
        for s_cwid in self.students_details.keys():
            stable.add_row(
                list(self.students_details[s_cwid].get_student_summary()))
        return stable

    def get_instructor_details(self, path: str) -> None:
        """reads the instructor file"""
        try:
            for cwid, name, dept in file_reader(path, 3, '\t', False):
                self.instructor_details[cwid] = Instructors(cwid, name, dept)
        except(FileNotFoundError, ValueError) as e:
            print(e)

    def get_instructors_table(self) -> None:
        """to display the summary of instructors details"""
        itable: PrettyTable = PrettyTable(field_names=["CWID", "Name", "Dept", "Course", "Students"])
        for instructor_cwid in self.instructor_details.keys():
            for details in self.instructor_details[instructor_cwid].get_instructor_summary():
                itable.add_row(details)
        return itable


def main():
    """ main program """
    # uni = University('/Users/venugopal/Documents/Fall20/SSW810/Week9/Files')
    uni: University = University(r'Files')
    print(uni.get_student_table())
    print(uni.get_instructors_table())


if __name__ == "__main__":
    main()
