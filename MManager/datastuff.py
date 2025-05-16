
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def graphIncomePerIncomeStream(conn):
    cursor = conn.cursor()
    query = "SELECT ifId,SUM(amt) FROM IncomeLog GROUP BY ifId;"
    gipis = cursor.execute(query).fetchall()
    
    ids = []
    incomePerId = []
    for i in gipis:
        query = f"SELECT name FROM incomeFields WHERE ifId = {i[0]};"
        try:
            nameField = cursor.execute(query).fetchone()[0]
            ids.append(nameField)
            incomePerId.append(i[1])
        except:
            print("Field not found")

    plt.bar(ids , incomePerId)
    plt.xlabel("Streams")
    plt.ylabel("Income")
    plt.title("Income per stream")

    plt.show()
    


def expenseSummary(conn , *args):

    cursor = conn.cursor()
    
    #list all prev expenses
    #get expenses per 'For'
    return  