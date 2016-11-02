# -*- coding: utf-8 -*-
"""
For all your query needs to do with users!
"""

import exe_sql as sql
import random

def newUser(name,sid, hash): # user will not be created under a new name if SID already exists due to UNIQUE CONSTRAINT
    """Create a new keyhash entry, new persons (pid) and link these in KPL"""
    sql.begin()
    hash = str(hash)
    # insert card
    sql.cur.execute("INSERT INTO keys (kid) VALUES(?)",[hash])
    sql.commit()
    
    x = sql.cur.execute("SELECT * FROM persons WHERE sid=?",[sid])
    res = x.fetchone()
    if res == None:
        # insert user
        sql.cur.execute("INSERT INTO persons (name,sid,usertype,balance) VALUES(?,?,0,?)", [name, sid,round(random.uniform(1,20),2)])
        sql.commit()
        pid = sql.lastId()
        print ("this")
    print ("that")
    sql.cur.execute("UPDATE keys SET pid=? WHERE kid=?",[pid,hash])    
    sql.commit()
    sql.end()

def makeAdmin(pid):
    """Up someones usertype"""
    sql.begin()
    sql.cur.execute("UPDATE persons SET usertype=1 WHERE pid=?", [pid])
    sql.commit()
    sql.end()

def removeAdmin(pid):
    """Down someones usertype"""
    if len(adminList()) > 1:
        sql.begin()
        sql.cur.execute("UPDATE persons SET usertype=0 WHERE pid=?", [pid])
        sql.commit()
        sql.end()

def adminList():
    """Get list of all current admins"""
    sql.begin()
    result = sql.cur.execute("SELECT pid,name,sid,usertype FROM persons WHERE usertype=1")
    res = result.fetchall()
    sql.end()
    return res

def keyList():
    """Get list of all keys in system (mainly unreadable hashes)"""
    sql.begin()
    result = sql.cur.execute("SELECT kid, pid FROM keys")
    res = result.fetchall()
    sql.end()
    return res

    #this should work as kid is now the hashed cardID
def removeKey(kid):
    """Remove a key, can be based on selection"""
    sql.begin()
    sql.cur.execute("DELETE FROM keys WHERE kid=?", [str(kid)])
    sql.commit()
    sql.end()

def keyUserList():
    """Get list of kid and pid in Tables"""
    sql.begin()
    result = sql.cur.execute("SELECT kid, pid FROM keys")
    res = result.fetchall()
    sql.end()
    return res

def userList():
    """Fetch list of /normal/ users"""
    sql.begin()
    result = sql.cur.execute("SELECT pid, name, sid, balance, usertype FROM persons WHERE usertype=0")
    res = result.fetchall()
    sql.end()
    return res
    
def resetUserBalance(pid):
    """Sets one users balance to 0, useful for "system clean" after invoices"""
    sql.begin()
    sql.cur.execute("UPDATE persons SET balance = 0.00 where pid=?",[pid])   
    sql.commit()
    sql.end()

def removeUser(pid):
    """Removes users and all activity linked to that user"""
    sql.begin()
    result = sql.cur.execute("SELECT balance from persons WHERE pid=?",[pid])    
    res = result.fetchone()
    print (res[0])
    # not removing if balance is positive?
    if res[0] <= 0:
        sql.cur.execute("DELETE FROM keys WHERE pid=?",[pid])
        result = sql.cur.execute("SELECT bid FROM basket WHERE pid=?",[pid])        
        res = result.fetchall()
        print ([res])
        for i in [res]:
            z = len(i)-1
            while z >= 0:
                removeOrderItems(i[z][0])
                z -= 1
        removeOrders(pid)
        sql.cur.execute("DELETE FROM persons WHERE pid=?",[pid]) #first we delete the persons themselves

def removeOrders(pid):
    sql.begin()
    sql.cur.execute("DELETE FROM orders WHERE pid=?",[pid]) 
    sql.commit()
    sql.end()
    
def removeOrderItems(bid):
    sql.begin()
    sql.cur.execute("DELETE FROM orderitems WHERE bid=?",[bid])
    sql.commit()
    sql.end()
    
def getOrders():
    """Get all orders and their information"""
    sql.begin()
    result = sql.cur.execute("SELECT bid, total, date, pid FROM orders")
    res = result.fetchall()
    sql.end()
    return res
    
def getOrders2(oid):
    """Get all orders and their information"""
    sql.begin()
    result = sql.cur.execute("SELECT bid, total, date, pid FROM orders WHERE bid=?",[oid])
    res = result.fetchall()
    sql.end()
    return res
    
def getOrderItems(oid):
    """Get all items for an oid"""
    sql.begin()
    result = sql.cur.execute("""SELECT bid, orderitems.iid,items.item_name, quantity, price
                       FROM items, orderitems
                       WHERE orderitems.bid = ?
                       and items.iid = orderitems.iid""",[oid])
    res = result.fetchall()
    sql.end()                       
    return res