# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 22:48:13 2016

@author: Luuk
"""
                                            #For explanation: look on Blackboard given links and search the internet

import sqlite3 as sql                        #import the sqlite3 library, set as sql (we don't use another version right now)


con = sql.connect('example.db')             #connect to given filename, if unexistent it will be created
cur = con.cursor()


def executeScriptsFromFile(filename):
    # Open and read the file as a single buffer
    fd = open(filename, 'r')
    sqlFile = fd.read()
    fd.close()


    #We want to try and catch the OperationalError if it happens by sending a msg
    try:
        cur.executescript(sqlFile)
    except sql.OperationalError as msg:
        print ("A problem was encountered trying to execute the Querry", msg)
        
#WIP for a quick overview to see if all data was added correctly

#def cur_tables():
#    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
#    x = cur.fetchall()
#    print(x)
#    for table in [x]:
#        result = cur.execute("SELECT * FROM %s;" % table);
#        
#            # Get all rows.
#        rows = result.fetchall();
#        
#            # \n represents an end-of-line
#        print ("\n--- TABLE ", table, "\n")
        
    
    #ALWAYS be sure to commit or you might get DB errors if multiple files try to access the same connection
def end():
    con.commit()