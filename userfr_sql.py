# -*- coding: utf-8 -*-
"""
Created on Mon Oct 31 14:47:54 2016

@author: Luuk
"""
import exe_sql as sql


def UserCheck(kid):
    """Select user data from keyhash recieved"""
    sql.begin()
    result = sql.cur.execute("""SELECT persons.name,persons.sid,persons.balance
                            from  persons, keys
                            WHERE kid = ?
                            AND keys.pid = persons.pid""", [kid])
    res = result.fetchall()
    sql.end()
    return res


    # the items list should be set up as a (list of) tuple (iid, quant) for easier inserts :: [(iid,quantity),(iid,quantity)]
def CreateTransAndBask(pid,item): #should update the pid to become keyhash from user scan, or we return value of pid gotten above?
    """Create the basket and Transactions of different items and update userbalance, stock accordingly"""
    sql.begin()
    sql.cur.execute("""INSERT INTO orders (pid,date) VALUES(?,CURRENT_TIMESTAMP)""", [pid])
    oid = sql.lastId()
    print (len(item))
    if len(item)>=1:
        for i in [item]:
            z = len(i)-1
            while z >= 0:
                x = sql.cur.execute("SELECT current_price FROM items WHERE iid=?",[i[z][0]])
                x = x.fetchone()
                #print for every item (z), oid, itemid, amount(int), price
                
                iid = i[z][0]
                quant = i[z][1]
                print (z, oid, iid, quant , x[0])
                #technically you wouldn't expect multiple entries of the same iid, so we don't have to catch those
                sql.cur.execute("""INSERT INTO orderitems (oid,iid,quantity,price) VALUES (?,?,?,?) """,[oid,iid,quant,x[0]])
                z -= 1
                sql.cur.execute("UPDATE items SET stock=stock-? WHERE iid=?",[quant,iid])
                
                #TODO: CATCH ERROR LATER IF AN ERROR OCCURS LATER ON AND WE  NEED A ROLLBACK SO BASKETID does not
                #keep adding up all the time             
                
                
        some = sql.cur.execute("""SELECT round(SUM(price*quantity),2) FROM orderitems where oid=?""",[oid])
        rex = some.fetchone()
        print (rex[0], pid)
    #sql.cur.execute("UPDATE items SET item_name=?, stock=?, current_price=? WHERE iid=?",  [str(name),int(stock),float(price),int(iid)])
        sql.cur.execute("UPDATE persons SET balance=balance+? WHERE pid=?",[rex[0],pid])
        sql.cur.execute("UPDATE orders SET total=? WHERE oid=?",[rex[0],oid])    
        result = sql.cur.execute("SELECT total FROM orders WHERE oid=?",[oid])
        res= result.fetchone() #should allways only return one
        sql.commit()        #only commit after everything has been inserted on the right place
        sql.end()
        print (sql.cur_tables())
        print (res)    
        return res
#    else:
#        sql.rollback()  #otherwise destroy the false try
#    sql.rollback()
    sql.end()
    

#quick debug function for getting stuff
def getUsers():
    """Mainly debug for quick overview of data to test allowed inputs for other queries"""
    sql.begin()
    result = sql.cur.execute('''SELECT kid, persons.pid, persons.name,persons.sid,persons.balance, usertype
                            FROM persons,  keys
                            WHERE keys.pid = persons.pid ''')
    res = result.fetchall()
    sql.end()
    return res
    
def getStats():
    """Return should be: most sold item, least sold item, cheapest item, average money spend, most items of most sold, number of different snacks"""
    """
    First (iid,item_name,quant) is Most sold
    Second (iid,item_name,quant) is least sold
    Third (iid,item_name,current_price) is cheapest item
    Fourth (average order price) is avg_order_price
    Fifth (pid, username, quant) user who ate most of most sold item
    Sixth (number of different items in system)
    """
    res = []  
    sql.begin()
    result = sql.cur.execute("""SELECT items.iid, item_name, SUM(orderitems.quantity) as quant
                                FROM items, orderitems, orders
                                WHERE items.iid = orderitems.iid
                                AND orders.oid = orderitems.oid
                                GROUP by items.iid
                                order by quant desc
                                """)
    res.append((result.fetchone()))
    x = res[0][0]
    result = sql.cur.execute("""SELECT items.iid, item_name, SUM(orderitems.quantity) as quant
                                FROM items, orderitems, orders
                                WHERE items.iid = orderitems.iid
                                AND orders.oid = orderitems.oid
                                GROUP by items.iid
                                order by quant asc
                                """)
    res.append((result.fetchone()))
    result = sql.cur.execute("""SELECT iid, item_name, MIN(current_price)
                                FROM items                                
                                """)
    res.append((result.fetchone()))
    result = sql.cur.execute("""SELECT AVG(total)
                                FROM orders
                                """)
    res.append((result.fetchone()))
    result = sql.cur.execute("""SELECT persons.pid, persons.name, SUM(orderitems.quantity) as quantitem
                                FROM persons, orders, orderitems
                                WHERE persons.pid = orders.pid
                                AND orderitems.iid = ?
                                AND orders.oid = orderitems.oid
                                GROUP BY persons.pid
                                order by quantitem desc
                                """,[x])
    res.append((result.fetchone()))
    result = sql.cur.execute("SELECT COUNT(iid) FROM items")    
    res.append((result.fetchone()))
    sql.end()
    return res