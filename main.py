
import sqlite3
import os

from matplotlib import table
import MManager.tableOps as tableOps
import MManager.getStuff as getStuff
import MManager.datastuff as dataStuff
import matplotlib.pyplot as plt


basedir = os.path.abspath(os.path.dirname(__file__))
filename = "moneyDB.db"
#connections
connection = sqlite3.connect(os.path.join(basedir, filename))

# MManager.tableOps.insert(connection , 'IncomeLog' , '(amt , month , year)' , 1000, 3, 2024)
# cursor = connection.cursor()
# print(cursor.execute("SELECT savings FROM currentAcc").fetchone())

while True:
    print("""
1: Savings and expense budget
2: Log Expenses and Fixed Expenses *
3: Get Stats
4: Edit Spread Settings For Wishlist and Savings
5: Log income
6: Income stream actions
7: Wishlist actions *
0: Exit
""")
    
    print("What do you want to do (1/2/3/4/5/6/7/0): " , end='')
    try:
        cmd = int(input())
        if cmd == 0:
            break
        if cmd > 7 or cmd < 0:
            raise 
    except:
        print("Enter a valid answer")
    
    try:
        match cmd:
            case 1:
                print("Your Savings are: " ,getStuff.getSavings(connection).fetchone()[0])
                print("Your Expense budget is: " ,getStuff.getBudget(connection).fetchone()[0])
            case 2:
                #add edit fixed expenses
                tableOps.logExpense(connection)
            case 3:
                print("""
1: Get income per income stream
2: Get expenses summary      
""")            
                while True:
                    choice = int(input("What do you want 1/2: "))
                    if choice == 1:
                        dataStuff.graphIncomePerIncomeStream(connection)
                        break
                    elif choice == 2:
                        dataStuff.expenseSummary(connection)
                        break
                    elif choice < 0:
                        break
                    else:
                        print("print a valid input")
                        continue
            case 4:
                print("""
1: Edit percentage of income going to savings
2: Edit percentage of income going to wishlist 
""")
                while True:
                    choice = int(input("What do you want 1/2: "))
                    if choice == 1:
                        tableOps.setSavingsPercentage(connection)
                        break
                    elif choice == 2:
                        tableOps.setWishlistPercentage(connection)
                        break
                    elif choice < 0:
                        break
                    else:
                        print("print a valid input")
                        continue
            case 5:
                tableOps.logIncome(connection)
            case 6:
                tableOps.changeIncomeStreams(connection)
            case _:
                print("something went wrong")          
    except :

        print("you havent added anything as of yet ")    
    
    

connection.close()

# UPDATE currentAcc  SET valWishlist = 50 WHERE idx = 1;