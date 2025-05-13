
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
    
    for i in others:
        temp.append(i)
    insertvalues = tuple(temp)
    # for i in args:
    #     print(i)
    
    query = f"INSERT INTO {tablename}{thingies} VALUES{insertvalues};"
    
    insCursor.execute(query)

    con.commit()
    
    return 

def logIncome(conn , *args):
    incomeCur = conn.cursor()
    income = int(input("\n Logging income now, enter income: "))
        
    if income < 0:
        print("Going Back")
        return    
    
    print("From which field: ")

    getAllIncomeFields = 'SELECT * FROM IncomeFields;'
    incomeFields = incomeCur.execute(getAllIncomeFields).fetchall()

    endstring = 'Enter your choice '

    for field in incomeFields:
        print(f"{field[0]} : {field[1]}")
        endstring += f'{field[0]}|'

    endstring = endstring[:-1] + ": "

    while True:
        try:
            ifId = int(input(endstring))
            if ifId > int(endstring[-3]):
                raise
            elif ifId < 0:
                print("going back \n")
                return
            break
        except:
            print("enter a valid input \n ")
            continue
    cutSavings = incomeCur.execute('SELECT valSavings FROM currentAcc').fetchone()[0]
   
    insert(conn , 'IncomeLog' , '(amt , month , year , ifId)' , income, 3, 2024 , ifId)

    #fixed expenses here
    #add date checker and then check another table to get if fixed expense has already been paid 
    #for the month
    getFixed = "SELECT * FROM FixedExpenses;"

    fixed = incomeCur.execute(getFixed).fetchall()
    leftincome = income
    for item in fixed:
        leftincome -= item[2]

    #this shit comes after fixed expenses
    savingsCut = leftincome * (cutSavings / 100)
    savings = int(incomeCur.execute("SELECT savings FROM currentAcc").fetchone()[0])
    savings += savingsCut
    update(conn , 'currentAcc' , 'savings' , savings , 'idx' , 1)
    #this comes after budget
    leftincome -= savingsCut

    
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
    
    #add an option to add income stream

    endstring = 'Enter your choice '

    for field in incomeFields:
        print(f"{field[0]} : {field[1]}")
        endstring += f'{field[0]}|'

    endstring = endstring[:-1] + ": "

    while True:
        try:
            ifId = int(input(endstring))
            if ifId > int(endstring[-3]):
                raise
            elif ifId < 0:
                print("going back \n")
                return
            break
        except:
            print("enter a valid input \n ")
            continue
    
    print(f"The selected income field is: {ifId}-{cursor.execute(f'SELECT name FROM incomeFields WHERE ifId = {ifId};').fetchone()[0]}" )
    
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
                        update(conn ,"incomeFields", "name" , f'{upField}' , "ifId" , ifId)
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
                    deleteRow(conn , "incomeFields" , "ifId" , ifId)
                    print("Field has been deleted! ")
                    break
                elif confirm == 2:
                    break
            break
                    


