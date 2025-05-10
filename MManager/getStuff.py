
def getTable(conn,tableName , *args):

    getTablecur = conn.cursor()
    getTableq = f"SELECT * FROM {tableName};"
    table = getTablecur.execute(getTableq).fetchall()

    return table

def getSavings(conn):
    getSavingscur = conn.cursor()
    query = "SELECT savings FROM currentAcc;"
    return getSavingscur.execute(query)

def getBudget(conn):
    getBudgetcur = conn.cursor()
    query = "SELECT budget FROM currentAcc;"
    return getBudgetcur.execute(query)
