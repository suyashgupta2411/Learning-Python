import globals

name = input('Enter student name: ')

if name in globals.student:
   del globals.student[name]
   globals.save_students(globals.student)
   print(name + " records successfully deleted")
else:
   print("Student not found")