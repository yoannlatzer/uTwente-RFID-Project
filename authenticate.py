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
    sql.cur.execute("SELECT kid FROM key WHERE keyhash=?", [hash])
    key = sql.cur.fetchone()
    if key == None:
        sql.end()
        return None
    else:
        sql.cur.execute("SELECT pid FROM KPL WHERE kid=?", [key[0]])
        pid = sql.cur.fetchone()
        if pid == None:
            sql.end()
            return None
        else:
            sql.cur.execute("SELECT * FROM person WHERE pid=?", [pid[0]])
            person = sql.cur.fetchone()

    sql.end()
    return person
