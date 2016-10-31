# -*- coding: utf-8 -*-
"""
All product related sql Querries for the admin side to keep track and edit/delete/add items
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
    sql.cur.execute('INSERT INTO items (item_name,stock,current_price) VALUES (?,?,?)',[str(name),int(stock),float(price)] )
    sql.commit()
    sql.end()
    
def editItem(name,stock,price,iid):
    sql.begin()
    sql.cur.execute("UPDATE items SET item_name=?, stock=?, current_price=? WHERE iid=?",  [str(name),int(stock),float(price),int(iid)])
    sql.commit()
    sql.end
    
def delItem(iid):
    sql.begin()
    sql.cur.execute("DELETE FROM items WHERRE iid=?", [iid])
    sql.commit()
    sql.end()