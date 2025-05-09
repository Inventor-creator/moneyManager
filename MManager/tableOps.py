import sqlite3
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