from eca import *
import eca.http
import serial_listener as rfid
import user_sql as userActions
import exe_sql as sql
import fake

def add_request_handlers(httpd):
  httpd.add_route('/fake/id', eca.http.GenerateEvent('fakescan'), methods=["POST"])
  httpd.add_route('/register', eca.http.GenerateEvent('register'), methods=["POST"])
  httpd.add_route('/logout', eca.http.GenerateEvent('logout'), methods=["POST"])

@event('init')
def setup(ctx, e):
    sql.create_db()
    userActions.newUser('Admin', 's0000000', fake.hash(0))
    userActions.newUser('User 1', 's0000001', fake.hash(1))
    sql.cur_tables()
    ctx.currentHash = None # CurrentHash cache scanned card hash (logged in hash)
    rfid.listen()

@event('register')
def registerUser(ctx, e):
    if ctx.currentHash == None:
        # todo: error feedback to user
        # Error no card known
        print("Error: No card active in system!")
    else:
        if not (e.data['sid']):
            # Error no student number given
            print("Error: No student number or name given!")
        else:
            if not e.data['name']:
                print("Error: No name given!")
            else:
                # card hash and student number known
                userActions.newUser(e.data['name'], e.data['sid'], ctx.currentHash)
                # show logged in screen
                print('Successful registration!')
                loginUser(ctx, e)

def loginUser(ctx, e):
    # TODO: user data in event name, student#, balance, type
    emit('authenticated', {})
    print('Successful login!')

@event('logout')
def logoutUser(ctx,e):
    ctx.currentHash = None
    emit('logout', {})
    print('Successful logged out!')

@event('fakescan')
def scan(ctx, e):
    ctx.currentHash = fake.hash(e.data['id'])
    user = rfid.sendFakeHash(ctx.currentHash)
    if user == False:
        emit('newUser', {})
    else:
        # show logged in screen
        loginUser(ctx, e)