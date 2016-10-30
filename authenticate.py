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
    user = sql.cur.fetchone()
    sql.end()
    return user
