# -*- coding: utf-8 -*-
"""
Created on Fri Oct 28 18:07:53 2016

@author: Luuk
"""

import exe_sql as sql

def new_user(name,sid): #user will not be created under a new name if SID already exists due to UNIQUE CONSTRAINT
    sql.begin()
    sql.cur.execute("INSERT INTO person (name,sid,usertype) VALUES(?,?,0)", [name,sid])
    sql.end()
    
def y():
    pass

print ("lolol")
new_user("Piet",1235984)
sql.cur_tables()
sql.useless()