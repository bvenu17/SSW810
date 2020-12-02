"""
@author: Venugopal Balaji CWID: 10446195
this program consists of classes which contains all information about the students and instructors
"""
import os as os
import sqlite3
from typing import IO, DefaultDict, List, Any, Dict, Optional, Set, Tuple
from collections import defaultdict, Counter
from datetime import datetime, timedelta
from prettytable import PrettyTable
from HW08_Venugopal_Balaji import file_reader


class Students:
    """class to store the details of the student"""

    def __init__(self, cwid: str, name: str, major: str, required_courses: List[str], elective_courses: List[str]) -> None:
        """funtion to initialize constructor"""
        self.cwid: str = cwid
        self.name: str = name
        self.major: str = major
        self.required_courses: List[str] = [] + required_courses
        self.elective_courses: List[str] = elective_courses
        self.electives: List[str] = list()
        self.allCourses: Dict[str, float] = dict()
        self.completedCourses: Dict[str, float] = dict()
        self.get_student_summary()

    def add_grade(self, course: str, grade: str) -> None:
        """function to add grade of student of each course"""
        gpa: Dict[str, float] = {"A": 4.0, "A-": 3.75, "B+": 3.25, "B": 3.0,
                                 "B-": 2.75, "C+": 2.25, "C": 2.0, "C-": 0, "D+": 0, "D": 0, "D-": 0, "F": 0}

        grade_point = gpa[grade]
        if grade_point > 0:
            self.completedCourses[course] = grade_point
        self.allCourses[course] = grade_point

        if grade_point > 0:
            if course in self.required_courses:
                self.required_courses.remove(course)

        if grade_point > 0 and course in self.elective_courses:
            self.electives = []
        else:
            self.electives = self.elective_courses

    def get_student_summary(self) -> Tuple[str, str, list]:
        """return the summary of student details for pretty table"""

        gpa: float = 0.0

        if self.allCourses:
            gpa = sum(self.allCourses.values())/len(self.allCourses)

        courses: List[str] = sorted(list(self.completedCourses.keys()))

        return self.cwid, self.name, courses, self.required_courses, self.electives, round(gpa, 2)


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


class Majors:
    """this class stores information for required course and electives for each major"""

    def __init__(self) -> None:
        """function to initialize constructor"""
        self.required_courses: List[str] = list()
        self.elective_courses: List[str] = list()

    def set_major_details(self, flag: str, courses: str) -> None:
        """function to save required and electives for each major"""
        if flag == 'R':
            self.required_courses.append(courses)
        if flag == 'E':
            self.elective_courses.append(courses)

    def get_required_courses(self) -> List[str]:
        return self.required_courses

    def get_elective_courses(self) -> List[str]:
        return self.elective_courses


class University:
    """this class is the repository for all information related to students and instructors"""

    def __init__(self, directory: str) -> None:
        """funtion to initialize constructor"""
        self.directory: str = directory
        self.students_details: Dict[str, Students] = dict()
        self.instructor_details: Dict[str, Instructors] = dict()
        self.major_details: Dict[str, Majors] = dict()
        self.get_majors_details(os.path.join(self.directory, "majors.txt"))
        self.get_student_details(os.path.join(self.directory, "students.txt"))
        self.get_instructor_details(os.path.join(
            self.directory, 'instructors.txt'))
        self.get_grades_details(os.path.join(self.directory, 'grades.txt'))
        self.query: str = """select s.Name,s.CWID,g.Course,g.Grade,i.Name from students as s join grades as g join instructors as i where s.CWID=g.StudentCWID and g.InstructorCWID=i.CWID order by s.Name;"""

    def get_majors_details(self, path: str) -> None:
        """reads the majors file"""
        try:
            for major, flag, course in file_reader(path, 3, '\t', True):
                if major in self.major_details:
                    self.major_details[major].set_major_details(flag, course)
                else:
                    self.major_details[major] = Majors()
                    self.major_details[major].set_major_details(flag, course)
        except(FileNotFoundError, ValueError) as e:
            print(e)

    def get_student_details(self, path: str) -> None:
        """reads the student file"""
        try:
            for cwid, name, major in file_reader(path, 3, '\t', True):
                if major in self.major_details:
                    self.students_details[cwid] = Students(cwid, name, major, self.major_details[major].get_required_courses(
                    ), self.major_details[major].get_elective_courses())
                else:
                    print("no details found for this major in the majors.txt file")
        except(FileNotFoundError) as e:
            print(e)

    def get_grades_details(self, path: str) -> None:
        """reads the grades file"""
        try:
            for student_cwid, course, grade, instructor_cwid in file_reader(path, 4, '\t', True):
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
            field_names=["CWID", "Name", "Completed Courses", "Remaining Required", "Remaining Elective", "GPA"])
        for s_cwid in self.students_details.keys():
            stable.add_row(
                list(self.students_details[s_cwid].get_student_summary()))
        return stable

    def get_instructor_details(self, path: str) -> None:
        """reads the instructor file"""
        try:
            for cwid, name, dept in file_reader(path, 3, '\t', True):
                self.instructor_details[cwid] = Instructors(cwid, name, dept)
        except(FileNotFoundError, ValueError) as e:
            print(e)

    def get_instructors_table(self) -> None:
        """to display the summary of instructors details"""
        itable: PrettyTable = PrettyTable(
            field_names=["CWID", "Name", "Dept", "Course", "Students"])
        for instructor_cwid in self.instructor_details.keys():
            for details in self.instructor_details[instructor_cwid].get_instructor_summary():
                itable.add_row(details)
        return itable

    def get_majors_table(self) -> None:
        """to display the summary of majors table"""
        mtable: PrettyTable = PrettyTable(
            field_names=["Major", "Required Courses", "Electives"]
        )
        for major in self.major_details.keys():
            mtable.add_row([major, self.major_details[major].get_required_courses(
            ), self.major_details[major].get_elective_courses()])
        return mtable

    def student_grades_details_db(self, db_path):
        """to display table for grades of students from sqlite db"""
        try:
            db: sqlite3.Connection = sqlite3.connect(db_path)
        except sqlite3.OperationalError as e:
            print(e)
        else:
            result: List[Tuple[str]] = []
            try:
                for row in db.execute(self.query):
                    result.append(row)
                db.close()
                return result
            except sqlite3.OperationalError as e:
                print(e)

    def student_grades_table_db(self, db_path):
        """to display table for grades of students from sqlite db"""
        try:
            db: sqlite3.Connection = sqlite3.connect(db_path)
        except sqlite3.OperationalError as e:
            print(e)
        else:
            pt: PrettyTable = PrettyTable(
                field_names=["Name", "CWID", "Course", "Grade", "Instructor"])
            try:
                for row in db.execute(self.query):
                    pt.add_row(row)
                db.close()
                return pt
            except sqlite3.OperationalError as e:
                print(e)


def main():
    """ main program """
    # uni = University('/Users/venugopal/Documents/Fall20/SSW810/Week9/Files')
    uni: University = University(r'Files')
    print(uni.get_student_table())
    print(uni.get_instructors_table())
    print(uni.get_majors_table())
    print(uni.student_grades_table_db(
        "Student_Repository_Venugopal_Balaji.sqlite"))


if __name__ == "__main__":
    main()
