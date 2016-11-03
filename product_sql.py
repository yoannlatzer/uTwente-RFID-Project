# -*- coding: utf-8 -*-
"""
All product related sql Queries for the admin side to keep track and edit/delete/add items
"""

import exe_sql as sql

#Category
def categoriesList():
    """Returns list of all categories :: [(a,b)(a,b)]"""
    sql.begin()
    result = sql.cur.execute('SELECT cid, name FROM categories')
    res = result.fetchall()
    sql.end()
    return res

def newCategory(name):
    """Creates new category"""
    sql.begin()
    sql.cur.execute('INSERT INTO categories (name) VALUES (?)', [name])
    sql.commit()
    sql.end()

def getCategory(cid):
    sql.begin()
    result = sql.cur.execute('SELECT cid, name FROM categories WHERE cid=?', [int(cid)])
    res = result.fetchone()
    sql.end()
    return res

def editCategory(name, cid):
    """Edit the name of a category"""
    sql.begin()
    sql.cur.execute("UPDATE categories SET name=? WHERE cid=?", [name, cid])
    sql.commit()
    sql.end()

def delCategory(cid):
    """Deletes category"""
    sql.begin()
    sql.cur.execute("DELETE FROM categories WHERE cid=?", [int(cid)])
    sql.commit()
    sql.end()

#Items
def getItems():
    """Gives an array of all items :: () -> [(a,b,c),(a,b,c)]"""
    sql.begin()
    result = sql.cur.execute('SELECT iid, item_name, stock, current_price, pic_url, cid FROM items')
    res = result.fetchall()
    sql.end()
    return res

def getFilterdItems(cid):
    """Gives an array of all items based on Category:: int(f) -> [(a,b,c,d,e,f),(a,b,c,d,e,f)]"""
    sql.begin()
    result = sql.cur.execute('SELECT iid, item_name, stock, current_price, pic_url, cid FROM items WHERE cid=?', [int(cid)])
    res = result.fetchall()
    sql.end()
    return res

def getItem(iid):
    """Gives info of One item:: int(a) -> (a, b, c, d, e, f)"""
    sql.begin()
    result = sql.cur.execute('SELECT iid, item_name, stock, current_price, pic_url, cid FROM items WHERE iid=?', [int(iid)])
    res = result.fetchone()
    sql.end()
    return res

def newItem(name, stock, price, image, cid):
    """Insert new item, iid should be created automatically by the DB::(name, stock, price, image, cid)"""    
    sql.begin()
    sql.cur.execute('INSERT INTO items (item_name, stock, current_price, pic_url, cid) VALUES (?, ?, ?, ?, ?)',
                    [str(name), int(stock), price, str(image), int(cid)])
    sql.commit()
    sql.end()
    
#TODO: make sure checking with previous results of normal select query that at least ONE field has changed
def editItem(name, stock, price, image, cid, iid):
    """edit an item based on the iid that is given in the submit/POST::(name, stock, price, image, cid, iid)"""
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