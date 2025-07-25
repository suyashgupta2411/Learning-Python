import globals

name = input('Enter name: ').strip()


if name in globals.student:
    print(f"{name}'s attendance: {globals.student[name][0]}")
    print(f"{name}'s grade: {globals.student[name][1]}")
    print(f"{name}'s overall performance score: {globals.student[name][2]}")
else:
    print(f"Student '{name}' not found in database.")
    if globals.student:  
        print("Available students:", list(globals.student.keys()))

print('\n \n \n')