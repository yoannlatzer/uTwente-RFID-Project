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
    print(str(hash))
    sql.cur.execute("SELECT pid FROM keys WHERE kid=?", [str(hash)])
    pid = sql.cur.fetchone()
    print(pid)
    if pid == None:
        sql.end()
        return None
    else:
        sql.cur.execute("SELECT * FROM persons WHERE pid=?", [pid[0]])
        person = sql.cur.fetchone()
    print(person)
    sql.end()
    return person
