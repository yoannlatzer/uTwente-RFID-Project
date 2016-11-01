import exe_sql as sql

def authenticateHash(hash):
    # Check if hash exist in db
    # if not prompt login screen
    # if is login show order screen
    user = getUserId(hash)
    if user == None: # no user for rfid hash found
        return False
    else:
        return user

def getUserId(hash):
    sql.begin()
    sql.cur.execute("SELECT pid FROM keys WHERE kid=?", [hash])
    pid = sql.cur.fetchone()
    if pid == None:
        sql.end()
        return None
    else:
        print (pid[0])
        sql.cur.execute("SELECT * FROM persons WHERE pid=?", [pid[0]])
        person = sql.cur.fetchone()

    sql.end()
    return person
