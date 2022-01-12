import sys

arguments = sys.argv

print(arguments)

d = {"-c": "course_ID", "-s": "student_ID"}

print(f"{d[arguments[1]]} = {arguments[2]}")
