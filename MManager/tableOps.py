import MManager.getStuff as getStuff


def deleteRow(conn , tableName , whereDelete,wheredeleteValue):
    delCursor = conn.cursor()

    query = f"DELETE FROM {tableName} WHERE {whereDelete} = {wheredeleteValue} ;"
    delCursor.execute(query)
    conn.commit()

def update(conn ,tableName, toUpdate , updateValue , where , whereValue):
    updateCur = conn.cursor()
    if type(updateValue) == str:
        query = f"UPDATE {tableName} SET {toUpdate} = '{updateValue}' WHERE {where} = {whereValue};"
    else:
        query = f"UPDATE {tableName} SET {toUpdate} = {updateValue} WHERE {where} = {whereValue};"
    updateCur.execute(query)
    conn.commit()

def insert(con , *args):

    insCursor = con.cursor()    

    tablename , thingies , *others = args
    #print ( tablename , args)
    temp = []
    # print(type(others) , others)
    if len(others) == 1:
        if type(others[0]) == str:
            query = f"INSERT INTO {tablename}{thingies} VALUES('{others[0]}');"
        else:
            query = f'INSERT INTO {tablename}{thingies} VALUES({others[0]});'
        insCursor.execute(query)
        con.commit()
        return

  
    insertvalues = tuple(others)
    # for i in args:
    #     print(i)
    print(insertvalues)
    query = f"INSERT INTO {tablename}{thingies} VALUES{insertvalues};"
    
    insCursor.execute(query)

    con.commit()
    
    return 

def logIncome(conn , *args):
    incomeCur = conn.cursor()
    income = int(input("\nLogging income now, enter income: "))
    
    if income < 0:
        print("Going Back")
        return    
    
    print("From which field: ")

    getAllIncomeFields = 'SELECT * FROM IncomeFields;'
    incomeFields = incomeCur.execute(getAllIncomeFields).fetchall()

    endstring = endstring = 'Enter your choice '
    index = 1
    idct = {}
    for field in incomeFields:
        print(f"{index} : {field[1]}")
        endstring += f"{index}|"
        idct[index] = field[0]
        index += 1

    endstring = endstring[:-1] + ": "

    while True:
        try:
            ifId = int(input(endstring))
            if ifId > int(endstring[-3]) or ifId == 0:
                raise
            elif ifId < 0:
                print("going back \n")
                return
            break
        except:
            print("enter a valid input \n ")
            continue
    cutSavings = incomeCur.execute('SELECT valSavings FROM currentAcc').fetchone()[0]
   
   #add year and date here
    insert(conn , 'IncomeLog' , '(amt , month , year , ifId)' , income, 3, 2024 , idct[ifId])



    leftincome = income
    
   
    savingsCut = leftincome * (cutSavings / 100)
    savings = int(incomeCur.execute("SELECT savings FROM currentAcc").fetchone()[0])
    savings += savingsCut
    update(conn , 'currentAcc' , 'savings' , savings , 'idx' , 1)

    #this comes after budget
    leftincome -= savingsCut
    update(conn , 'currentAcc' , 'budget' ,getStuff.getBudget(conn).fetchone()[0] + leftincome , 'idx' , 1 )

    
def setSavingsPercentage(conn):
    cursor = conn.cursor()
    print(f"The current value of your Savings percentage is {cursor.execute('SELECT valSavings FROM currentAcc').fetchone()[0]}")
    while True:
        percentage = float(input("Enter the percent value you want the Savings deduction to be set at: "))
        if percentage < 0:
            return
        break
    query = f'UPDATE currentAcc  SET valSavings = {percentage} WHERE idx = 1;'
    cursor.execute(query)
    conn.commit()
    print(f"New value set to {percentage}")


def setWishlistPercentage(conn):
    cursor = conn.cursor()
    print(f"The current value of your Wishlist percentage is {cursor.execute('SELECT valWishlist FROM currentAcc').fetchone()[0]}")
    while True:
        percentage = float(input("Enter the percent value you want the Wishlist deduction to be set at: "))
        if percentage < 0:
            return
        break
    query = f'UPDATE currentAcc SET valWishlist = {percentage} WHERE idx = 1;'
    cursor.execute(query)
    conn.commit()
    print(f"New value set to {percentage}")    

def changeIncomeStreams(conn):
    cursor = conn.cursor()
    getAllIncomeFields = 'SELECT * FROM IncomeFields;'
    incomeFields = cursor.execute(getAllIncomeFields).fetchall()
    
    
    print("""
1: Add new Field
2: Edit old Fields
""")

    while True: 
        choice = int(input("Enter your choice 1/2: "))
        if choice and choice <=2 and choice > 0:
            break
        elif choice > 2:
            print("Enter a valid input")
            continue
        else:
            print("Going back")
            break
    
    if choice == 2:
        endstring = 'Enter your choice '
        index = 1
        idct = {}
        for field in incomeFields:
            print(f"{index} : {field[1]}")
            endstring += f'{index}|'
            idct[index] = field[0]
            index += 1

        endstring = endstring[:-1] + ": "

        while True:
            try:
                ifId = int(input(endstring))
                if ifId > int(endstring[-3]) or ifId == 0:
                    raise
                elif ifId < 0:
                    print("going back \n")
                    return
                break
            except:
                print("enter a valid input \n ")
                continue
        
        print(f"The selected income field is: {ifId}-{cursor.execute(f'SELECT name FROM incomeFields WHERE ifId = {idct[ifId]};').fetchone()[0]}" )
        
        print("""
1:Update Field
2:Delete Field
    """)
        
        while True:
            operation = int(input("What do you want to do 1/2: "))
            if operation < 1 or operation > 2:
                print("enter a valid input")
                continue
            elif operation == -1:
                break
            elif operation == 1:
                while True:
                    upField = str(input("Enter the updated name field of the incomeField: "))
                    if not upField:
                        print("Enter a valid input please")
                        continue
                    else:
                        try:    
                            update(conn ,"incomeFields", "name" , f'{upField}' , "ifId" , idct[ifId])
                        except:
                            print("Somethings wrong")
                        print("Name of field has been updated! ")
                        break
                break

            else:
                while True:
                    print("""
Do you want to delete the field?
1: Confirm
2: Back
    """)
                    confirm = int(input("1/2: "))
                    if confirm < 1 or confirm > 2:
                        print("enter a valid input")
                        continue
                    elif confirm == 1:
                        deleteRow(conn , "incomeFields" , "ifId" , idct[ifId])
                        print("Field has been deleted! ")
                        break
                    elif confirm == 2:
                        break
                break
    elif choice == 1:
        #add an option to add income stream
        while True:
            newField = str(input("Enter the name of the new field: "))
            if not newField:
                print("Enter a valid input! ")
                continue
            else:
                break
        insert(conn , 'incomeFields' , '(name)' , newField)
        
def logExpense(conn):
    from datetime import date

    logExpenseCur = conn.cursor()
    print("""
1: Pay Fixed Expenses
2: Log some other expense
""")
    while True:
        choice = int(input("Enter your choice 1/2: "))

        if choice < 0:
            return
        elif choice >2:
            print("Enter a valid input! ")
            continue
        else:
            break
            
    if choice == 1:
        todaysDate = str(date.today()).split('-')

        unpaidFixedQ = f"SELECT * FROM FixedLast WHERE paid = 0"
        unpaidFixed = logExpenseCur.execute(unpaidFixedQ).fetchall()
        print(unpaidFixed)
        indexDict = {}
        indexToOwed = {}
        indexToName ={}
        index = 1
        print("Following stuff is not paid")
        endstring = 'Choose which field you want: '
        #check if due has passed for prev payment 
        for fixedExpense in unpaidFixed:
            indexDict[index] = fixedExpense
            getFixedExpenseQ = f"SELECT * FROM FixedExpenses WHERE iFixed = {fixedExpense[0]}"
            getFixedExpense = logExpenseCur.execute(getFixedExpenseQ).fetchone()

            indexToName[index] = getFixedExpense[1]
            indexToOwed[index] = getFixedExpense[2] * fixedExpense[5]

            print(f"{index}: {indexToName[index]} - {indexToOwed[index]}")
            endstring += f'{index}|'
            index += 1
        endstring = endstring[:-1] + ": "

        while True:
            try:
                iFixed = int(input(endstring))
                if iFixed > int(endstring[-3]) or iFixed == 0:
                    raise
                elif iFixed < 0:
                    print("going back \n")
                    return
                break
            except:
                print("enter a valid input \n ")
                continue
        
        print(f"selected {iFixed}: {indexToName[iFixed]} , owed- {indexToOwed[iFixed]}")
        
        payFrom = ""
        temp = 1
        id = {}
        #add option to pay from savings or expense budget
        if indexToOwed[iFixed] < getStuff.getSavings(conn).fetchone()[0] :
            payFrom += f"\n{temp} Savings - {getStuff.getSavings(conn).fetchone()[0]} "
            id[temp] = "savings"
            temp += 1
            
        if indexToOwed[iFixed] < getStuff.getBudget(conn).fetchone()[0] :
            payFrom += f"\n{temp} Budget - {getStuff.getBudget(conn).fetchone()[0]} "
            id[temp] = "budget"
        elif payFrom == "Pay from: ":
            print("You are broke! ")
            return
       
        print(payFrom)
        
        while True:
            payChoice = int(input("\nEnter index of where u want to pay: "))
            if payChoice < 0:
                return
            elif payChoice > temp:
                print("Enter a valid choice! ")
                continue
            else:
                break
        
       
        if id[payChoice] == "savings":
            update(conn , 'currentAcc' , 'savings' ,getStuff.getSavings(conn).fetchone()[0] - indexToOwed[iFixed] , 'idx' , 1 )
        else:
            update(conn , 'currentAcc' , 'budget' ,getStuff.getBudget(conn).fetchone()[0] - indexToOwed[iFixed] , 'idx' , 1 )


    return
#update(conn , 'currentAcc' , 'savings' ,getSavings(conn).fetchone()[0] - indexToOwed[iFixed] , 'idx' , 1 )