

#connection, table name, and args
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

    print("\n Logging income now, enter income: " )
    income = int(input())
    print("From which field: ")

    getAllIncomeFields = 'SELECT * FROM IncomeFields;'
    incomeFields = incomeCur.execute(getAllIncomeFields).fetchall()

    endstring = 'Enter your choice '

    for field in incomeFields:
        print(f"{field[0]} : {field[1]}")
        endstring += f'{field[0]}|'
    

    endstring = endstring[:-1] + ": "

    print(endstring , end='')
    while True:
        try:
            ifId = int(input())
            if ifId < 0 or ifId > int(endstring[-3]):
                raise

            break
        except:
            print("enter a valid input \n ")


    return income , ifId