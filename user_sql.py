# -*- coding: utf-8 -*-
"""
Created on Fri Oct 28 18:07:53 2016

@author: Luuk
"""

import exe_sql as sql

def newUser(name,sid, hash): # user will not be created under a new name if SID already exists due to UNIQUE CONSTRAINT
    sql.begin()
    # insert card
    sql.cur.execute("INSERT INTO key (keyhash) VALUES(?)", [hash])
    sql.commit()
    kid = sql.lastId()

    # insert user
    sql.cur.execute("INSERT INTO person (name,sid,usertype) VALUES(?,?,0)", [name, sid])
    sql.commit()
    pid = sql.lastId()

    # link user to card
    sql.cur.execute("INSERT INTO KPL (kid, pid) VALUES(?,?)", [kid, pid])
    sql.commit()
    sql.end()

def makeAdmin(pid):
    sql.begin()
    sql.cur.execute("UPDATE person SET usertype=1 WHERE pid=?", [pid])
    sql.commit()
    sql.end()

def keyList():
    sql.begin()
    result = sql.cur.execute("SELECT * FROM key")
    print(result.fetchall())
    sql.end()

def keyUserList():
    sql.begin()
    result = sql.cur.execute("SELECT * FROM KPL")
    print(result.fetchall())
    sql.end()

def userList():
    sql.begin()
    result = sql.cur.execute("SELECT * FROM person")
    print(result.fetchall())
    sql.end()

def y():
    pass

#print ("lolol")
#newUser("Piet",1235984)
#sql.cur_tables()
#sql.useless()