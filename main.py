
import sqlite3
import os
import MManager.tableOps as tableOps
import MManager.getStuff as getStuff
import MManager.datastuff as dataStuff
import matplotlib.pyplot as plt


basedir = os.path.abspath(os.path.dirname(__file__))
filename = "moneyDB.db"
#connections
connection = sqlite3.connect(os.path.join(basedir, filename))

# MManager.tableOps.insert(connection , 'IncomeLog' , '(amt , month , year)' , 1000, 3, 2024)

while True:
    print("""
1: Get Current Savings
2: Get Current Expense Budget
3: Get Stats
4: Increase / Decrease Expense Budget
5: Log income
0: Exit
""")
    
    print("What do you want to do (1/2/3/4/5/0): " , end='')
    try:
        cmd = int(input())
        if cmd == 0:
            break
        if cmd > 5 or cmd < 0:
            raise 
    except:
        print("Enter a valid answer")
    
    try:
        match cmd:
            case 1:
                print("Your Savings are: " ,getStuff.getSavings(connection).fetchall()[0])
            case 2:
                print("Your Expense budget is: " ,getStuff.getBudget(connection).fetchall()[0])
            case 3:
                print("""
1: Get income per income stream
2: Get expenses summary      
""")
                choice = int(input("What do you want: "))
                if choice == 1:
                    dataStuff.graphIncomePerIncomeStream(connection)
                elif choice ==2:
                    dataStuff.expenseSummary(connection)
            case 5:
                income, ifId = tableOps.logIncome(connection)
                tableOps.insert(connection , 'IncomeLog' , '(amt , month , year , ifId)' , income, 3, 2024 , ifId)
            case _:
                print("something went wrong")          
    except :

        print("you havent added anything as of yet ")    

    
    break

connection.close()