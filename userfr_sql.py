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
    bid = sql.lastId()
    print (len(item))
    if len(item)>=1:
        for i in [item]:
            z = len(i)-1
            while z >= 0:
                x = sql.cur.execute("SELECT current_price FROM items WHERE iid=?",[i[z][0]])
                x = x.fetchone()
                #print for every item (z), bid, itemid, amount(int), price
                
                iid = i[z][0]
                quant = i[z][1]
                print (z, bid, iid, quant , x[0])
                #technically you wouldn't expect multiple entries of the same iid, so we don't have to catch those
                sql.cur.execute("""INSERT INTO orderitems (bid,iid,quantity,price) VALUES (?,?,?,?) """,[bid,iid,quant,x[0]])
                z -= 1
                sql.cur.execute("UPDATE items SET stock=stock-? WHERE iid=?",[quant,iid])
                
                #TODO: CATCH ERROR LATER IF AN ERROR OCCURS LATER ON AND WE  NEED A ROLLBACK SO BASKETID does not
                #keep adding up all the time             
                
                
        some = sql.cur.execute("""SELECT round(SUM(price*quantity),2) FROM orderitems where bid=?""",[bid])
        rex = some.fetchone()
        print (rex[0], pid)
    #sql.cur.execute("UPDATE items SET item_name=?, stock=?, current_price=? WHERE iid=?",  [str(name),int(stock),float(price),int(iid)])
        sql.cur.execute("UPDATE persons SET balance=balance+? WHERE pid=?",[rex[0],pid])
        sql.cur.execute("UPDATE orders SET total=? WHERE bid=?",[rex[0],bid])    
        result = sql.cur.execute("SELECT total FROM orders WHERE bid=?",[bid])
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
                            from persons,  keys
                            WHERE keys.pid = persons.pid ''')
    res = result.fetchall()
    sql.end()
    return res