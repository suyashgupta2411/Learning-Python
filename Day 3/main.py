print('Welcome to Student Management System')
print('\n')

i = 1  
while(i != 0):
    print('Choose one option: \n')
    print('1: Enter Student Info')
    print('2: Display Student Info')
    print('3: Remove Student Info')
    print('\n')
    print('Enter 0 to exit')
    
    try:
        i = int(input())  
        
        if(i == 1):
            exec(open('enterStudentInfo.py').read())
        elif(i == 2):
            exec(open('getStudentInfo.py').read())
        elif(i == 3):
            exec(open('delStudentInfo.py').read())
        elif(i == 0):
            print("Goodbye!")
            break
        else:
            print("Invalid option! Please choose 1, 2, or 0.")
    except ValueError:
        print("Please enter a valid number!")
    except FileNotFoundError as e:
        print(f"File not found: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")