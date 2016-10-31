# -*- coding: utf-8 -*-
"""
Created on Fri Oct 28 18:07:53 2016

@author: Luuk
"""

import exe_sql as sql
import random

def newUser(name,sid, hash): # user will not be created under a new name if SID already exists due to UNIQUE CONSTRAINT
    sql.begin()
    # insert card
    sql.cur.execute("INSERT INTO key (keyhash) VALUES(?)", [hash])
    sql.commit()
    kid = sql.lastId()

    # insert user
    sql.cur.execute("INSERT INTO person (name,sid,usertype,balance) VALUES(?,?,0,?)", [name, sid,round(random.uniform(1,20),2)])
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

def removeAdmin(pid):
    sql.begin()
    sql.cur.execute("UPDATE person SET usertype=0 WHERE pid=?", [pid])
    sql.commit()
    sql.end()

def adminList():
    sql.begin()
    result = sql.cur.execute("SELECT name,sid,usertype FROM person WHERE usertype=1")
    res = result.fetchall()
    sql.end()
    return res

def keyList():
    sql.begin()
    result = sql.cur.execute("SELECT kid, keyhash FROM key")
    res = result.fetchall()
    sql.end()
    return res

def keyUserList():
    sql.begin()
    result = sql.cur.execute("SELECT kid, pid FROM KPL")
    res = result.fetchall()
    sql.end()
    return res

def userList():
    sql.begin()
    result = sql.cur.execute("SELECT pid, name, sid, balance, usertype FROM person WHERE usertype=0")
    res = result.fetchall()
    sql.end()
    return res