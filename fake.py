import user_sql as userActions
import exe_sql as sql
import sys
import hashlib
if sys.version_info < (3, 6):
    import sha3

def generateHash(id):
    s = hashlib.sha3_512()
    s.update(id)
    return s.hexdigest()

def hash(id):
    return generateHash('b\'{}\''.format(id))