# -*- coding: utf-8 -*-
"""
Created on Mon Oct 31 14:47:54 2016

@author: Luuk
"""
import exe_sql as sql


def UserCheck(keyhash):
    sql.begin()
    result = sql.cur.execute("""SELECT person.name,person.sid,person.balance
                            from  person, KPL, key
                            WHERE keyhash = ?
                            AND key.kid = KPL.kid
                            AND KPL.pid= person.pid""", [keyhash])
    res = result.fetchall()
    sql.end()
    return res

    #items should be set up as a (list of) tuple (iid, quant) for easier inserts
def CreateTransAndBask(pid,item): #should update the pid to become keyhash from user scan, or we return value of pid gotten above?
    sql.begin()
    sql.cur.execute("""INSERT INTO basket (pid,date) VALUES(?,CURRENT_TIMESTAMP)""", [pid])
    bid = sql.lastId()
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
            sql.cur.execute("""INSERT INTO transactions (bid,iid,quantity,price) VALUES (?,?,?,?) """,[bid,iid,quant,x[0]])
            z -= 1
            sql.cur.execute("UPDATE items SET stock=stock-? WHERE iid=?",[quant,iid])
            
            #TODO: CATCH ERROR LATER IF AN ERROR OCCURS LATER ON AND WE  NEED A ROLLBACK SO BASKETID does not
            #keep adding up all the time             
            
            
    some = sql.cur.execute("""SELECT round(SUM(price*quantity),2) FROM transactions where bid=?""",[bid])
    rex = some.fetchone()
    print (rex[0], pid)
#sql.cur.execute("UPDATE items SET item_name=?, stock=?, current_price=? WHERE iid=?",  [str(name),int(stock),float(price),int(iid)])
    sql.cur.execute("UPDATE person SET balance=balance+? WHERE pid=?",[rex[0],pid])
    sql.cur.execute("UPDATE basket SET total=? WHERE bid=?",[rex[0],bid])    
    result = sql.cur.execute("SELECT total FROM basket WHERE bid=?",[bid])
    res= result.fetchone() #should allways only return one
    sql.commit()
    sql.end()
    print (res)    
    return res
    

#quick debug function for getting stuff
def getUsers():
    sql.begin()
    result = sql.cur.execute('''SELECT keyhash, key.kid, person.pid, person.name,person.sid,person.balance, usertype
                            from person, KPL, key
                            Where key.kid = KPL.kid
                            AND KPL.pid= person.pid''')
    res = result.fetchall()
    sql.end()
    return res