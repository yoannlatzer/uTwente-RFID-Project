# -*- coding: utf-8 -*-
"""
Created on Mon Oct 31 20:49:25 2016

@author: Luuk
"""

import exe_sql as sql

def spendingsByUser():
    """Get list of spendings per user for last time since RESET"""
    sql.begin()
    result = sql.cur.execute("""SELECT persons.pid, persons.name,persons.balance
                                FROM persons
                                """)
    res = result.fetchall()
    sql.end()
    return res

def spendingsByUserTotal():
    """Spendings by ALL users in system since start of system"""
    sql.begin()
    result = sql.cur.execute("""SELECT DISTINCT orders.pid, persons.name, SUM(orders.total)
                                FROM orders, persons
                                where persons.pid = orders.pid
                                GROUP BY orders.pid
                                """)
    res = result.fetchall()
    sql.end()
    return res

def spendingsTotal():
    """The total spending from the system since last RESET"""
    sql.begin()
    result = sql.cur.execute("""SELECT SUM(balance) FROM persons""")
    res = result.fetchone()
    sql.end()
    return res                              
    
def spendingsTotalStart():
    """The total spending from the system since start"""
    sql.begin()
    result = sql.cur.execute("""SELECT SUM(total) FROM orders""")
    res = result.fetchone()
    sql.end()
    return res

    #date is expected to be in YYYY-MM-DD HH:MM:SS
    #function hasn't been correctly tested yet
def CheckInsOuts(date)    :
    """Check what has gone in (stock) and what has gone out (from transactions since x date)"""
    sql.begin()
    result = sql.cur.execute("""SELECT items.stock, SUM(transactions.quantity)
                                FROM items, orderitems
                                WHERE items.iid = orderitems.iid
                                AND date >= datetime(?)
                                GROUP BY items.iid"""[date])
    res = result.fetchone()
    sql.end()
    return res