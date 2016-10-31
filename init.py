from eca import *
import eca.http
import serial_listener as rfid
import user_sql as userActions
import exe_sql as sql
import fake
import json


def add_request_handlers(httpd):
  httpd.add_route('/fake/id', eca.http.GenerateEvent('fakescan'), methods=["POST"])
  httpd.add_route('/register', eca.http.GenerateEvent('register'), methods=["POST"])
  httpd.add_route('/admin', eca.http.GenerateEvent('adminscreen'), methods=["POST"])
  httpd.add_route('/admin/page', eca.http.GenerateEvent('adminpage'), methods=["POST"])
  httpd.add_route('/logout', eca.http.GenerateEvent('logout'), methods=["POST"])

@event('init')
def setup(ctx, e):
    sql.create_db()
    userActions.newUser('Admin', 1000000, fake.hash(0))
    userActions.makeAdmin(1)
    userActions.newUser('User 1', 1000001, fake.hash(1))
    sql.cur_tables()
    ctx.person = None
    ctx.currentHash = None # CurrentHash cache scanned card hash (logged in hash)
    rfid.listen()

@event('adminscreen')
def openAdminScreen(ctx, e):
    if ctx.person[4] == 1:
        emit('admin', {'pid': ctx.person[0], 'type': ctx.person[4], 'name': ctx.person[1], 'sid': ctx.person[2]})
        print('Show admin screen')

@event('adminpage')
def showAdminPage(ctx, e):
    if ctx.person[3] == 1:
        if e.data['page'] == 'keyList':
            emit('adminpage', {'page': e.data['page'], 'data': userActions.keyList()})
        if e.data['page'] == 'userList':
            emit('adminpage', {'page': e.data['page'], 'data': userActions.userList()})
        if e.data['page'] == 'adminList':
            emit('adminpage', {'page': e.data['page'], 'data': userActions.adminList()})

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
                user = rfid.sendFakeHash(ctx.currentHash)
                ctx.person = user
                loginUser(ctx, e)

def loginUser(ctx, e):
    # TODO: balance
    if ctx.person != None:
        emit('authenticated', {'pid': ctx.person[0], 'type': ctx.person[4], 'name': ctx.person[1], 'sid': ctx.person[2]})
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
        print(user)
        ctx.person = user
        # show logged in screen
        loginUser(ctx, e)