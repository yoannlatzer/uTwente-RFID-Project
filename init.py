from eca import *
import eca.http
import serial_listener as rfid
import user_sql as userActions
import product_sql as itemActions
import userfr_sql as userFrontendActions
import exe_sql as sql
import fake
import json


def add_request_handlers(httpd):
  httpd.add_route('/fake/id', eca.http.GenerateEvent('fakescan'), methods=["POST"])
  httpd.add_route('/register', eca.http.GenerateEvent('register'), methods=["POST"])
  httpd.add_route('/categories/list', eca.http.GenerateEvent('categoriesList'), methods=["POST"])
  httpd.add_route('/items/list', eca.http.GenerateEvent('itemsList'), methods=["POST"])
  httpd.add_route('/items/select', eca.http.GenerateEvent('itemsSelect'), methods=["POST"])
  httpd.add_route('/items/remove', eca.http.GenerateEvent('itemsRemove'), methods=["POST"])
  httpd.add_route('/buy', eca.http.GenerateEvent('buyBasket'), methods=["POST"])
  httpd.add_route('/admin', eca.http.GenerateEvent('adminscreen'), methods=["POST"])
  httpd.add_route('/admin/page', eca.http.GenerateEvent('adminpage'), methods=["POST"])
  httpd.add_route('/admin/item/add', eca.http.GenerateEvent('addItem'), methods=["POST"])
  httpd.add_route('/admin/category/add', eca.http.GenerateEvent('addCategory'), methods=["POST"])
  httpd.add_route('/logout', eca.http.GenerateEvent('logout'), methods=["POST"])

@event('init')
def setup(ctx, e):
    sql.create_db()
    logoutUser(ctx, e)
    userActions.newUser('Admin', 1000000, fake.hash(0))
    userActions.makeAdmin(1)
    userActions.newUser('User 1', 1000001, fake.hash(1))
    sql.cur_tables()
    rfid.listen()

@event('adminscreen')
def openAdminScreen(ctx, e):
    if ctx.person[4] == 1:
        emit('admin', {'pid': ctx.person[0], 'type': ctx.person[4], 'name': ctx.person[1], 'sid': ctx.person[2]})
        print('Show admin screen')

@event('adminpage')
def showAdminPage(ctx, e):
    if ctx.person[4] == 1:
        if e.data['page'] == 'keyList':
            emit('adminpage', {'page': e.data['page'], 'data': userActions.keyList()})
        if e.data['page'] == 'userList':
            emit('adminpage', {'page': e.data['page'], 'data': userActions.userList()})
        if e.data['page'] == 'adminList':
            emit('adminpage', {'page': e.data['page'], 'data': userActions.adminList()})
        if e.data['page'] == 'categoryAdd':
            emit('adminpage', {'page': e.data['page']})
        if e.data['page'] == 'categoryList':
            emit('adminpage', {'page': e.data['page'], 'data': itemActions.categoriesList()})
        if e.data['page'] == 'productList':
            emit('adminpage', {'page': e.data['page'], 'data': itemActions.getItems()})
        if e.data['page'] == 'productAdd':
            emit('adminpage', {'page': e.data['page'], 'data': itemActions.categoriesList()})

@event('addItem')
def newItem(ctx, e):
    if ctx.person[4] == 1:
        itemActions.newItem(e.data['name'], e.data['stock'], e.data['price'], e.data['image'], e.data['cid'])
        print('Item added', e.data['name'])
        emit('adminpage', {'page': 'productList', 'data': itemActions.getItems()})

    else:
        logoutUser()

@event('addCategory')
def newCategory(ctx, e):
    if ctx.person[4] == 1:
        itemActions.newCategory(e.data['name'])
        print('Category added', e.data['name'])
        emit('adminpage', {'page': 'categoryList', 'data': itemActions.categoriesList()})

    else:
        logoutUser()

@event('categoriesList')
def listCategories(ctx, e):
    emit('categories', {'data': itemActions.categoriesList()})
    print('List categories')

@event('itemsList')
def listItems(ctx, e):
    emit('items', {'data': itemActions.getFilterdItems(e.data['cid'])})
    print('List items')

@event('itemsSelect')
def selectItem(ctx, e):
    ctx.basket = addBasketItem(ctx.basket, e.data['iid'])
    emit('basket', {'data': ctx.basket})
    print('Select Item')

def addBasketItem(basket, iid):
    itemInfo = itemActions.getItem(iid)
    for item in basket:
        if item['iid'] == iid:
            item['quantity'] += 1
            return basket
    item = {'iid': int(iid), 'quantity': 1, 'price': itemInfo[3], 'name': itemInfo[1]}
    basket.append(item)
    return basket

@event('itemsRemove')
def removeItem(ctx, e):
    ctx.basket = removeBasketItem(ctx.basket, e.data['iid'])
    emit('basket', {'data': ctx.basket})
    print('Remove Item')

def removeBasketItem(basket, iid):
    for item in basket:
        if item['iid'] == iid:
            item['quantity'] -= 1
            if item['quantity'] == 0:
                basket.remove(item)
            return basket

@event('buyBasket')
def buy(ctx, e):
    itemTuple = []
    for item in ctx.basket:
        itemTuple.append((item['iid'], item['quantity']))
    userFrontendActions.CreateTransAndBask(ctx.person[0], itemTuple)
    print('Items bought')
    emit('thankyou', {})

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
        emit('authenticated', {'pid': ctx.person[0], 'type': ctx.person[4], 'name': ctx.person[1], 'sid': ctx.person[2], 'balance': ctx.person[3]})
        print('Successful login!')

@event('logout')
def logoutUser(ctx, e):
    ctx.person = None
    ctx.currentHash = None # CurrentHash cache scanned card hash (logged in hash)
    ctx.basket = []
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