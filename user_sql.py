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

def getUser(pid):
    sql.begin()
    result = sql.cur.execute("SELECT pid, sid, name FROM persons where pid=?",[pid])
    res = result.fetchone()
    sql.end()
    return res
    
def resetUserBalance(pid):
    """Sets one users balance to 0, useful for "system clean" after invoices"""
    sql.begin()
    sql.cur.execute("UPDATE persons SET balance = 0.00 where pid=?",[pid])   
    sql.commit()
    sql.end()

def addUserBalance(pid, add):
    """Sets one users balance to 0, useful for "system clean" after invoices"""
    sql.begin()
    sql.cur.execute("UPDATE persons SET balance = balance - ? where pid=?", [add, pid])
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
        result = sql.cur.execute("SELECT oid FROM basket WHERE pid=?",[pid])        
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
    
def removeOrderItems(oid):
    sql.begin()
    sql.cur.execute("DELETE FROM orderitems WHERE oid=?",[oid])
    sql.commit()
    sql.end()

def removeOrder(oid):
    sql.begin()
    order = sql.cur.execute("SELECT total, pid FROM orders WHERE oid=?", [oid])
    order = order.fetchone()
    addUserBalance(order[1], order[0])
    sql.begin()
    sql.cur.execute("DELETE FROM orders WHERE oid=?",[oid])
    sql.commit()
    sql.end()
    removeOrderItems(oid)

def removeOrderItem(oid, iid):
    sql.begin()
    pid = sql.cur.execute("SELECT pid FROM orders WHERE oid=?", [oid])
    pid = pid.fetchone()
    res = sql.cur.execute("SELECT quantity, price FROM orderitems WHERE oid=? AND iid=?", [oid, iid])
    res = res.fetchone()
    totalRemoved = res[0] * res[1]
    addUserBalance(pid[0], totalRemoved)
    sql.begin()
    sql.cur.execute("UPDATE orders SET total = total - ? WHERE oid=?", [totalRemoved, oid])
    sql.commit()
    sql.cur.execute("DELETE FROM orderitems WHERE oid=? AND iid=?", [oid, iid])
    sql.commit()
    sql.end()

def getOrders():
    """Get all orders and their information"""
    sql.begin()
    result = sql.cur.execute("SELECT oid, total, date, pid FROM orders")
    res = result.fetchall()
    sql.end()
    return res
    
def getFullOrders():
    orders = getOrders()
    result = []
    for i in [orders]:
        z = len(i) - 1
        while z >= 0:
            items = getOrderItems(orders[z][0])
            person = getUser(orders[z][3])
            result.append({'oid': orders[z][0], 'total': orders[z][1], 'date': orders[z][2], 'items': items, 'person': person})
            z -= 1
    return result    
    
def getOrders2(oid):
    """Get all orders and their information"""
    sql.begin()
    result = sql.cur.execute("SELECT oid, total, date, pid FROM orders WHERE oid=?",[oid])
    res = result.fetchall()
    sql.end()
    return res
    
def getOrderItems(oid):
    """Get all items for an oid"""
    sql.begin()
    result = sql.cur.execute("""SELECT oid, orderitems.iid,items.item_name, quantity, price
                       FROM items, orderitems
                       WHERE orderitems.oid = ?
                       and items.iid = orderitems.iid""",[oid])
    res = result.fetchall()
    sql.end()                       
    return res