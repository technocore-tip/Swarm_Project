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
    sql_query="INSERT INTO `swarms` (`swarm_id`, `name`) VALUES (NULL, 'a')"
    cursor = connection.cursor()
    cursor.execute(sql_query)
    cursor.execute('select LAST_INSERT_ID()')
    records=cursor.fetchall()
    print(records[0][0])
    cursor.close() 
    connection.close()
except Error as e:
    print("Error connecting to database",e)