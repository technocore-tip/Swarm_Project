# -*- coding: utf-8 -*-
"""
Created on Thu May 28 02:23:09 2020

@author: Paul Vincent Nonat
"""

import mysql.connector
from mysql.connector import Error

try:
    connection = mysql.connector.connect(host='localhost',
                                     database='nonat',
                                     user='nonat',
                                     password='password')
    sql_query="delete from swarms;ALTER TABLE swarms AUTO_INCREMENT = 1;"
    cursor = connection.cursor()
    cursor.execute(sql_query,multi=True)
    cursor.close() 
    connection.close()
except Error as e:
    print("Error connecting to database",e)