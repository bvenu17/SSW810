from flask import Flask, render_template
import sqlite3
from Student_Repository_Venugopal_Balaji import University
app: Flask = Flask(__name__)

@app.route('/')
def home() -> str:
    return render_template('base.html',title='Student Repository')

@app.route('/students')
def student_grades():
    query: str = """select s.Name,s.CWID,g.Course,g.Grade,i.Name from students as s join grades as g join instructors as i where s.CWID=g.StudentCWID and g.InstructorCWID=i.CWID order by s.Name;"""
    uni: University = University(r"Files")
    # print(uni.student_grades_details_db("Student_Repository_Venugopal_Balaji.sqlite"))
    details = uni.student_grades_details_db("Student_Repository_Venugopal_Balaji.sqlite")

    return render_template('student_grades.html', title='Student Repository - Grades',
                           students=details)

app.run(debug=True)