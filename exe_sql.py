# -*- coding: utf-8 -*-
"""
To create your own version of the DB, just run this file in your CLI/command window

Created on Thu Oct 27 22:48:13 2016

@author: Luuk
"""
                                 #For explanation: look on Blackboard given links and search the internet

import sqlite3 as sql            #import the sqlite3 library, set as sql (we don't use another version right now)

global con
global cur

def ExepHand(query):
    """For all user input we check if corret DataType INSIDE querry and catch Exceptions"""
    try:
        result = cur.execute(query)
    except ValueError as msg:  #trying to store s1234567 as sid shouldn't work, sid = integer, we check with python in querry
        print ("msg") #possibly use a return to send back an error?
    return result
    
def begin():
    """Start connection and return global vars con and cur"""
    global cur
    global con    
    con = sql.connect('snack.db')     #connect to given filename, if unexistent it will be created
    cur = con.cursor()
    


def exeScriptFile(filename):
    """Opens a .sql file and executes the SQL querries written in the file (.sql --> .db)"""
    # Open and read the file as a single buffer
    try:
        fd = open(filename, 'r')
        sqlFile = fd.read()
        fd.close()
    except FileNotFoundError as msg:
        print ('an error occurd' + msg)


    #We want to try and catch the OperationalError if it happens by sending a msg
    try:
        cur.executescript(sqlFile)
    except sql.OperationalError as msg:
        print ("A problem was encountered trying to execute the Querry", msg)
        
def cur_tables():
    """Shows all info for current tables (not yet db independent due to fetching of Tables)"""
    begin()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")    
    x = [tup[0] for tup in cur.fetchall()]
    for table in x:
        result = cur.execute("SELECT * FROM %s;" % table)
        
            # Get all rows.
        rows = result.fetchall()
        cur.execute("SELECT * FROM %s" % table)
        col_name = [tuple[0] for tuple in cur.description]
        
            # \n represents an end-of-line
        print ("\n--- TABLE ", table)
        print (col_name)
        print (rows)
    end()

def lastId():
    """Get last inserted id"""
    return cur.lastrowid

def commit():
    """Commit changes"""
    con.commit()

def end():
    """End the connection we have made"""
    con.close()

def create_db():
    """create a connection, exe script, and end the connection"""
    begin()
    exeScriptFile('snack_create.sql')
    commit()
    end()

def rollback():
    con.rollback()
#create_db()

def useless():
    print ('only to test correct calls from other documents')