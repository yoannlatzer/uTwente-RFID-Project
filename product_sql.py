# -*- coding: utf-8 -*-
"""
All product related sql Querries for the admin side to keep track and edit/delete/add items
"""

import exe_sql as sql



    #get data and store for a new item
def getItems():
    """Gives an array of all items :: [(a,b,c),(a,b,c)]"""
    sql.begin()
    result = sql.cur.execute('SELECT iid, item_name, stock, current_price, pic_url FROM items')
    res = result.fetchall()
    sql.end()
    return res

def newItem(name,stock,price):
    """Insert new item, iid should be created automatically by the DB"""    
    sql.begin()
    sql.cur.execute('INSERT INTO items (item_name,stock,current_price) VALUES (?,?,?)',[str(name),int(stock),float(price)] )
    sql.commit()
    sql.end()
    
def editItem(name,stock,price,iid):
    #TODO: make sure checking with previous results of normal select query that at least ONE field has changed
    """edit an item based on the iid that is given in the submit/POST"""
    sql.begin()
    sql.cur.execute("UPDATE items SET item_name=?, stock=?, current_price=? WHERE iid=?",  [str(name),int(stock),float(price),int(iid)])
    sql.commit()
    sql.end
    
def delItem(iid):
    """deletes an Item, based on iid given in the submit/POST"""
    sql.begin()
    sql.cur.execute("DELETE FROM items WHERRE iid=?", [iid])
    sql.commit()
    sql.end()