# -*- coding: utf-8 -*-
"""
Created on Mon Oct 31 20:49:25 2016

@author: Luuk
"""

import exe_sql as sql

def spendingsByUser():
    """Get list of spendings per user for last time since RESET"""
    sql.begin()
    result = sql.cur.execute("""SELECT person.pid, person.name,person.balance
                                FROM person
                                """)
    res = result.fetchall()
    sql.end()
    return res

def spendingsByUserTotal():
    """Spendings by ALL users in system since start of system"""
    sql.begin()
    result = sql.cur.execute("""SELECT DISTINCT basket.pid, person.name, SUM(basket.total)
                                FROM basket, person
                                where person.pid = basket.pid
                                GROUP BY basket.pid
                                """)
    res = result.fetchall()
    sql.end()
    return res

def spendingsTotal():
    """The total spending from the system since last RESET"""
    sql.begin()
    result = sql.cur.execute("""SELECT SUM(balance) FROM person""")
    res = result.fetchone()
    sql.end()
    return res                              
    
def spendingsTotalStart():
    """The total spending from the system since start"""
    sql.begin()
    result = sql.cur.execute("""SELECT SUM(total) FROM basket""")
    res = result.fetchone()
    sql.end()
    return res

    #date is expected to be in YYYY-MM-DD HH:MM:SS
def CheckInsOuts(date)    :
    """Check what has gone in (stock) and what has gone out (from transactions since x date)"""
    sql.begin()
    result = sql.cur.execute("""SELECT items.stock, SUM(transactions.quantity)
                                FROM items, transactions
                                WHERE items.iid = transactions.iid
                                AND date >= datetime(?)
                                GROUP BY items.iid"""[date])
    res = result.fetchone()
    sql.end()
    return res