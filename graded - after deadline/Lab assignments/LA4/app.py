from flask import Flask
from flask import render_template
from flask import request
import matplotlib.pyplot as plt
from statistics import mean
import csv

with open("data.csv", "r") as f:
    data = list(csv.DictReader(f))
fields = [field for field in data[0].keys()]
stu_id_list = [d[fields[0]] for d in data]
course_id_list = [d[fields[1]].strip() for d in data]


def get_stu_details(stu_id):
    if stu_id in stu_id_list:
        student_data = []
        total_marks = 0
        for d in data:
            if d[fields[0]] == stu_id:
                student_data.append(d)
                total_marks += int(d[fields[2]])
        return student_data, total_marks
    else:
        return "wrong inputs"

def get_course_details(course_id):
    if course_id in course_id_list:
        course_marks = []
        for d in data:
            if d[fields[1]].strip() == course_id:
                course_marks.append(int(d[fields[2]]))

        # Generate histogram for course_marks
        plt.hist(course_marks)
        plt.xlabel("Marks")
        plt.ylabel("Frequency")
        plt.savefig('static/histogram.png')

        # Return avg_marks and max_marks
        return mean(course_marks), max(course_marks)
    else:
        return "wrong inputs"


app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])

def awesome():
    if request.method == "GET":
        return render_template("index.html")

    elif request.method == "POST":
        id = request.form.get("ID", None)
        if id == "student_id":
            stu_id = request.form["id_value"]
            try:
                student_data, total_marks = get_stu_details(stu_id)
                return render_template("student_details.html", student_data=student_data, total_marks=total_marks, fields=fields)
            except:
                return render_template("error_page.html")

        elif id == "course_id":
            course_id = request.form["id_value"]
            try:
                avg_marks, max_marks = get_course_details(course_id)
                return render_template("course_details.html", avg_marks=avg_marks, max_marks=max_marks)
            except:
                return render_template("error_page.html")
        else:
            return render_template("error_page.html")


if __name__=="__main__":
    app.run()
