def showSavingOptions(s):
    idx=1
    for val in s:
        print(idx,val)
        idx=idx+1

def InputGathering(income,expenses,savings_goals):
    savings_goals_selected_option=-1
    flag=""
    income=int(input('\nEnter your salary -> '))
    expenses=int(input('\nEnter your expenses -> '))
    if(income<expenses):
        print('Income cannot be less than expenses.')
        exit()
    print("\nAmount available for investment = ",income - expenses)
    showSavingOptions(savings_goals)
    while(savings_goals_selected_option<0 or savings_goals_selected_option>5):
         savings_goals_selected_option=int(input('\n\nEnter the '+flag+' index of your option -> '))
         flag="appropriate"
    return savings_goals_selected_option-1
    