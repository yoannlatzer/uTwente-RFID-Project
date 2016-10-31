# -*- coding: utf-8 -*-
"""
Created on Mon Oct 31 13:22:45 2016

@author: Luuk
"""

import exe_sql as sql


    #get data and store for a new item
def getItems():
    sql.begin()
    result = sql.cur.execute('SELECT * FROM items')
    res = result.fetchall()
    sql.end()
    return res

def newItem(name,stock,price):
    sql.begin()
    sql.cur.execute('INSERT INTO items (item_name,stock,current_price,) VALUES (?,?,?)',[str(name),int(stock),float(price)] )
    sql.commit()
    sql.end()
    
def editItem(name,stock,price,iid):
    sql.begin()
    sql.cur.execute("UPDATE items SET item_name=?, stock=?, current_price=?WHERE iid=?",  [str(name),int(stock),float(price),int(iid)])
    sql.commit()
    sql.end
    
def delItem(iid):
    pass