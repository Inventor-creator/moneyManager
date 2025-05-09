import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

import MManager.tableOps

connection = sqlite3.connect('MoneyDB.db')

basedir = os.path.abspath(os.path.dirname(__file__))
filename = "MoneyDB.db"
#connections
connection = sqlite3.connect(os.path.join(basedir, filename))

MManager.tableOps.insert(connection , 'IncomeLog' , '(amt , month , year)' , 1000, 3, 2024)




connection.close()