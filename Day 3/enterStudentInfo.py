import globals
while True:
        student_name = input("Enter the student's name: ")
        if student_name.replace(' ', '').isalpha() and student_name.strip() != '':
            break
        else:
         print("Invalid name. Please use only alphabetic characters: ")
print('\n')
print('Enter '+student_name+"'s information")
print('\n')
while True:
        try:
            attendance=int(input("Enter "+student_name +"'s attendance: "))
            if(attendance<=100 and attendance>=0):
             break
        except ValueError:
            print("Invalid input! Please enter valid attendance: ")



while True:
    grade = input("Enter a grade (A-F): ").upper().strip()
        
    if len(grade) == 1 and grade in 'ABCDEF':
        break
    else:
        print("Invalid input. Please enter a single letter A, B, C, D, E, or F.")

while True:
        try:
            overall_performance_score=int(input("Enter"+student_name +"'s overall performance score: "))
            if(overall_performance_score>0 and overall_performance_score<=10):
             break
        except ValueError:
            print("Invalid input! Please enter valid score between 0 and 10")


student_info=[attendance,grade,overall_performance_score]
globals.student[student_name]=student_info

globals.save_students(globals.student)

print(f"\nSuccessfully stored information for {student_name}!")
print(f"Data: {student_info}")
print('\n \n')
