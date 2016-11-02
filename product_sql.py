# -*- coding: utf-8 -*-
"""
All product related sql Queries for the admin side to keep track and edit/delete/add items
"""

import exe_sql as sql

def categoriesList():
    sql.begin()
    result = sql.cur.execute('SELECT cid, name FROM categories')
    res = result.fetchall()
    sql.end()
    return res

def newCategory(name):
    sql.begin()
    sql.cur.execute('INSERT INTO categories (name) VALUES (?)', [name])
    sql.commit()
    sql.end()

def editCategory(cid):
    sql.begin()
    sql.cur.execute("UPDATE categories SET name=? WHERE cid=?", [cid])
    sql.commit()
    sql.end()

def delCategory(cid):
    sql.begin()
    sql.cur.execute("DELETE FROM categories WHERE cid=?", [cid])
    sql.commit()
    sql.end()

#get data and store for a new item
def getItems():
    """Gives an array of all items :: [(a,b,c),(a,b,c)]"""
    sql.begin()
    result = sql.cur.execute('SELECT iid, item_name, stock, current_price, pic_url, cid FROM items')
    res = result.fetchall()
    sql.end()
    return res

def getFilterdItems(cid):
    """Gives an array of all items :: [(a,b,c),(a,b,c)]"""
    sql.begin()
    result = sql.cur.execute('SELECT iid, item_name, stock, current_price, pic_url, cid FROM items WHERE cid=?', [int(cid)])
    res = result.fetchall()
    sql.end()
    return res

def getItem(iid):
    """Gives an array of all items :: [(a,b,c),(a,b,c)]"""
    sql.begin()
    result = sql.cur.execute('SELECT iid, item_name, stock, current_price, pic_url, cid FROM items WHERE iid=?', [int(iid)])
    res = result.fetchone()
    sql.end()
    return res

def newItem(name, stock, price, image, cid):
    """Insert new item, iid should be created automatically by the DB"""    
    sql.begin()
    sql.cur.execute('INSERT INTO items (item_name, stock, current_price, pic_url, cid) VALUES (?, ?, ?, ?, ?)',
                    [str(name), int(stock), price, str(image), int(cid)])
    sql.commit()
    sql.end()
    
def editItem(name, stock, price, image, cid, iid):
    #TODO: make sure checking with previous results of normal select query that at least ONE field has changed
    """edit an item based on the iid that is given in the submit/POST"""
    sql.begin()
    sql.cur.execute("UPDATE items SET item_name=?, stock=?, current_price=?, pic_url=?, cid=? WHERE iid=?",
                    [str(name), int(stock), float(price), str(image), int(cid), int(iid)])
    sql.commit()
    sql.end()
    
def delItem(iid):
    """deletes an Item, based on iid given in the submit/POST"""
    sql.begin()
    sql.cur.execute("DELETE FROM items WHERE iid=?", [iid])
    sql.commit()
    sql.end()