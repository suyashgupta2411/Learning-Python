import json
from datetime import datetime, timedelta
import os
from random import randint, seed
# -------------------- Account Class --------------------
class Account:
    def __init__(self,account_number,name,type):
        self.__account_number= account_number
        self.__name=name
        self.__type=type

    def showDetails(self):
        for data in f"[account_number]":
            print(data)
    
    def deleteAccount(self):
        del f"[account_number]"
    
    def getAccountNumber(self):
        return self.__account_number
    
# -------------------- Account Holder Class --------------------
class AccountHolder:
    def openAccount():
        
#savings currents account
#you can start from here
def main():
    account = Account()
    accountHolder = AccountHolder()
    while True:
        print("Welcome To The Bank")
        print("Type 1 To Show Account Details")
        print("Type 2 To Create A Bank Account")
        print("Type 3 To Delete A Bank Account")
        print("Type 4 To Exit The Bank")
        choice = input("Enter choice: ")
        if choice == "1":
            account.showDetails()
        elif choice == "2":
            account.getAccountNumber()
        elif choice == "3":
            account.deleteAccount()
        elif choice == "4":
            break
        else:
            print("Please enter a valid option.")
    print("Exited.")