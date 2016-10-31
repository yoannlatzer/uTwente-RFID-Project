# -*- coding: utf-8 -*-
"""
Created on Mon Oct 31 14:47:54 2016

@author: Luuk
"""
import exe_sql as sql


def UserCheck(keyhash):
    sql.begin()
    result = sql.cur.execute("""SELECT person.name,person.sid,person.balance
                            from  person, KPL, key
                            WHERE keyhash = ?
                            AND key.kid = KPL.kid
                            AND KPL.pid= person.pid""", [keyhash])
    res = result.fetchall()
    sql.end()
    return res

def getUsers():
    sql.begin()
    result = sql.cur.execute('''SELECT keyhash, key.kid, person.pid, person.name,person.sid,person.balance, usertype
                            from person, KPL, key
                            Where key.kid = KPL.kid
                            AND KPL.pid= person.pid''')
    res = result.fetchall()
    sql.end()
    return res