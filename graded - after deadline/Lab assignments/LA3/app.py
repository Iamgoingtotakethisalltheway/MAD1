from statistics import mean
from jinja2 import Template
import matplotlib.pyplot as plt
import sys

# Handle data.csv file
fields = []
rows = []
with open("data.csv", 'r') as f:
	fields = [h.strip() for h in f.readline().split(',')]
	for row in f.readlines():
		rows.append([i.strip() for i in row.split(',')])

st_data = [{fields[0]:row[0], fields[1]:row[1], fields[2]:row[2]} for row in rows]
st_ids = [d["Student id"] for d in st_data]
co_ids = [d["Course id"] for d in st_data]

def get_student_details(st_id):
    selected_students = []
    for d in st_data:
        if d["Student id"] == st_id:
            selected_students.append(d)
    return selected_students

def get_course_details(co_id):
    course_details = dict()
    course_marks = []
    for d in st_data:
        if d["Course id"] == co_id:
            course_marks.append(int(d["Marks"]))
    course_details["course_marks"] = course_marks
    course_details["avg_marks"] = mean(course_marks)
    course_details["max_marks"] = max(course_marks)
    return course_details


# Create three templates for three html pages

student_data_template = '''<!DOCTYPE html>
                            <html lang="en-US">
                            <head>
                                <meta charset="UTF-8">
                                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                                <title>Student Data</title>
                            </head>
                            <body>
                                <h1>Student Details</h1>
                                <table border=1px>
                                    <thead>
                                        <tr>
                                            <th>Student id</th>
                                            <th>Course id</th>
                                            <th>Marks</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {% for item in st_data %}
                                        <tr>
                                            <td>{{ item[fields[0]] }}</td>
                                            <td>{{ item[fields[1]] }}</td>
                                            <td>{{ item[fields[2]] }}</td>
                                        </tr>
                                        {% endfor %}
                                        <tr>
                                            <td colspan="2" style="text-align:center;">Total Marks</td>
                                            <td>{{ total_marks }}</td>
                                        </tr>
                                    </tbody>
                                </table>
                            </body>
                            </html>'''

course_data_template = '''<!DOCTYPE html>
                            <html lang="en-US">
                            <head>
                                <meta charset="UTF-8">
                                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                                <title>Course Data</title>
                            </head>
                            <body>
                                <h1>Course Details</h1>
                                <table border=1px>
                                    <thead>
                                        <tr>
                                            <th>Average Marks</th>
                                            <th>Maximum Marks</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr>
                                            <td>{{ course_details["avg_marks"] }}</td>
                                            <td>{{ course_details["max_marks"] }}</td>
                                        </tr>
                                    </tbody>
                                </table>
                                <img src="histogram.png" alt="Histogram of course scores" width="500" height="400">
                            </body>
                            </body>
                            </html>'''

error_page_template = '''<!DOCTYPE html>
                            <html lang="en-US">
                            <head>
                                <meta charset="UTF-8">
                                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                                <title>Something Went Wrong</title>
                            </head>
                            <body>
                                <h1>Wrong Inputs</h1>
                                <p>Something went wrong</p>
                            </body>
                            </html>'''

def main():
    sd_template = Template(student_data_template)
    cd_template = Template(course_data_template)
    err_template = Template(error_page_template)

    content = err_template.render()

    # Handle command line arguments
    arguments = sys.argv
    if len(arguments) > 2:
        if arguments[1] == "-s":
            st_id = arguments[2]
            if st_id in st_ids:
                student_data=get_student_details(st_id)
                sum_marks = sum([int(d["Marks"]) for d in student_data])
                content = sd_template.render(st_data=student_data, total_marks=sum_marks, fields=fields)
        elif arguments[1] == "-c":
            co_id = arguments[2]
            if co_id in co_ids:
                course_data = get_course_details(co_id)
                marks = course_data["course_marks"]
                plt.hist(marks)
                plt.xlabel("Marks")
                plt.ylabel("Frequency")
                # plt.show()
                plt.savefig('histogram.png')
                content = cd_template.render(course_details=course_data)

    # Write output.html file
    with open("output.html", "w") as f:
        f.write(content)

    
if __name__ == "__main__":
    main()
