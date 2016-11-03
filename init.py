from eca import *
import eca.http
#import serial_listener as rfid
from authenticate import authenticateHash
import user_sql as userActions
import product_sql as itemActions
import userfr_sql as userFrontendActions
import exe_sql as sql
import fake
import ToCSV as csv
import demo as demo

def add_request_handlers(httpd):
  httpd.add_route('/login', eca.http.GenerateEvent('userPassLogin'), methods=["POST"])
  httpd.add_route('/stats', eca.http.GenerateEvent('getStats'), methods=["POST"])
  httpd.add_route('/fake/id', eca.http.GenerateEvent('fakescan'), methods=["POST"])
  httpd.add_route('/register', eca.http.GenerateEvent('register'), methods=["POST"])
  httpd.add_route('/categories/list', eca.http.GenerateEvent('categoriesList'), methods=["POST"])
  httpd.add_route('/items/list', eca.http.GenerateEvent('itemsList'), methods=["POST"])
  httpd.add_route('/items/select', eca.http.GenerateEvent('itemsSelect'), methods=["POST"])
  httpd.add_route('/items/remove', eca.http.GenerateEvent('itemsRemove'), methods=["POST"])
  httpd.add_route('/buy', eca.http.GenerateEvent('buyBasket'), methods=["POST"])
  httpd.add_route('/admin', eca.http.GenerateEvent('adminscreen'), methods=["POST"])
  httpd.add_route('/admin/page', eca.http.GenerateEvent('adminpage'), methods=["POST"])
  httpd.add_route('/admin/admin/make', eca.http.GenerateEvent('adminmake'), methods=["POST"])
  httpd.add_route('/admin/admin/remove', eca.http.GenerateEvent('adminremove'), methods=["POST"])
  httpd.add_route('/admin/user/edit', eca.http.GenerateEvent('useredit'), methods=["POST"])
  httpd.add_route('/admin/user/update', eca.http.GenerateEvent('userupdate'), methods=["POST"])
  httpd.add_route('/admin/user/remove', eca.http.GenerateEvent('userremove'), methods=["POST"])
  httpd.add_route('/admin/key/remove', eca.http.GenerateEvent('keyremove'), methods=["POST"])
  httpd.add_route('/admin/category/add', eca.http.GenerateEvent('addCategory'), methods=["POST"])
  httpd.add_route('/admin/category/edit', eca.http.GenerateEvent('categoryedit'), methods=["POST"])
  httpd.add_route('/admin/category/update', eca.http.GenerateEvent('categoryupdate'), methods=["POST"])
  httpd.add_route('/admin/category/remove', eca.http.GenerateEvent('categoryremove'), methods=["POST"])
  httpd.add_route('/admin/order/remove', eca.http.GenerateEvent('orderremove'), methods=["POST"])
  httpd.add_route('/admin/orderitem/remove', eca.http.GenerateEvent('orderitemremove'), methods=["POST"])
  httpd.add_route('/admin/item/add', eca.http.GenerateEvent('addItem'), methods=["POST"])
  httpd.add_route('/admin/item/edit', eca.http.GenerateEvent('itemedit'), methods=["POST"])
  httpd.add_route('/admin/item/update', eca.http.GenerateEvent('itemupdate'), methods=["POST"])
  httpd.add_route('/admin/item/remove', eca.http.GenerateEvent('itemremove'), methods=["POST"])
  httpd.add_route('/logout', eca.http.GenerateEvent('logout'), methods=["POST"])
  httpd.add_route('/admin/downloadcsv', eca.http.GenerateEvent('downloadcsv'), methods=["POST"])
  httpd.add_route('/admin/downloadsql', eca.http.GenerateEvent('downloadsql'), methods=["POST"])

@event('init')
def setup(ctx, e):
    sql.create_db()
    demo.demoData()
    sql.cur_tables()
    logoutUser(ctx, e)


@event('getStats')
def statsGet(ctx, e):
    emit('stats', {'data': userFrontendActions.getStats()})

@event('adminmake')
def makeAdmin(ctx, e):
    if ctx.person[4] == 1:
        userActions.makeAdmin(e.data['pid'])
        print('Make admin')
        emit('adminpage', {'page': 'adminList', 'data': userActions.adminList()})

@event('adminremove')
def removeAdmin(ctx, e):
    if ctx.person[4] == 1:
        userActions.removeAdmin(e.data['pid'])
        print('Remove admin')
        emit('adminpage', {'page': 'adminList', 'data': userActions.adminList()})

@event('useredit')
def editUserPage(ctx, e):
    if ctx.person[4] == 1:
        print('show edit user page')
        emit('adminpage', {'page': 'editUser', 'data': userActions.getUser(e.data['pid'])})

@event('userupdate')
def updateUser(ctx, e):
    if ctx.person[4] == 1:
        userActions.editUser(e.data['name'], e.data['balance'], e.data['sid'], e.data['pid'])
        print('Update user')
        emit('adminpage', {'page': 'userList', 'data': userActions.userList()})

@event('userremove')
def removeUser(ctx, e):
    if ctx.person[4] == 1:
        userActions.removeUser(e.data['pid'])
        print('Remove user')
        emit('adminpage', {'page': 'userList', 'data': userActions.userList()})

@event('orderitemremove')
def removeOrderItem(ctx, e):
    if ctx.person[4] == 1:
        userActions.removeOrderItem(e.data['oid'], e.data['iid'])
        print('Remove oder item')
        emit('adminpage', {'page': 'orderList', 'data': userActions.getFullOrders()})

@event('orderremove')
def removeOrder(ctx, e):
    if ctx.person[4] == 1:
        userActions.removeOrder(e.data['oid'])
        print('Remove oder')
        emit('adminpage', {'page': 'orderList', 'data': userActions.getFullOrders()})

@event('keyremove')
def removeKey(ctx, e):
    if ctx.person[4] == 1:
        userActions.removeKey(e.data['kid'])
        print('Remove key')
        emit('adminpage', {'page': 'keyList', 'data': userActions.keyList()})

@event('addCategory')
def newCategory(ctx, e):
    if ctx.person[4] == 1:
        itemActions.newCategory(e.data['name'])
        print('Category added', e.data['name'])
        emit('adminpage', {'page': 'categoryList', 'data': itemActions.categoriesList()})

    else:
        logoutUser(ctx, e)

@event('categoriesList')
def listCategories(ctx, e):
    emit('categories', {'data': itemActions.categoriesList()})
    print('List categories')

@event('categoryedit')
def editCategory(ctx, e):
    if ctx.person[4] == 1:
        print('Edit category')
        emit('adminpage', {'page': 'editCategory', 'data': itemActions.getCategory(e.data['cid'])})

@event('categoryupdate')
def updateCategory(ctx, e):
    if ctx.person[4] == 1:
        itemActions.editCategory(e.data['name'], e.data['cid'])
        print('Update category')
        emit('adminpage', {'page': 'categoryList', 'data': itemActions.categoriesList()})

@event('categoryremove')
def removeCategory(ctx, e):
    if ctx.person[4] == 1:
        itemActions.delCategory(e.data['cid'])
        print('Remove category')
        emit('adminpage', {'page': 'categoryList', 'data': itemActions.categoriesList()})

@event('adminscreen')
def openAdminScreen(ctx, e):
    if ctx.person[4] == 1:
        emit('admin', {'pid': ctx.person[0], 'type': ctx.person[4], 'name': ctx.person[1], 'sid': ctx.person[2]})
        print('Show admin screen')

@event('adminpage')
def showAdminPage(ctx, e):
    if ctx.person != None:
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
            if e.data['page'] == 'orderList':
                emit('adminpage', {'page': e.data['page'], 'data': userActions.getFullOrders()})

@event('addItem')
def newItem(ctx, e):
    if ctx.person[4] == 1:
        itemActions.newItem(e.data['name'], e.data['stock'], e.data['price'], e.data['image'], e.data['cid'])
        print('Item added', e.data['name'])
        emit('adminpage', {'page': 'productList', 'data': itemActions.getItems()})

    else:
        logoutUser(ctx, e)

@event('itemedit')
def editItem(ctx, e):
    if ctx.person[4] == 1:
        print('Edit item')
        emit('adminpage', {'page': 'editProduct', 'data': itemActions.getItem(e.data['iid']), 'categories': itemActions.categoriesList()})

@event('itemupdate')
def updateItem(ctx, e):
    if ctx.person[4] == 1:
        itemActions.editItem(e.data['name'], e.data['stock'], e.data['price'], e.data['image'], e.data['cid'], e.data['iid'])
        print('Update item')
        emit('adminpage', {'page': 'productList', 'data': itemActions.getItems()})

@event('itemsList')
def listItems(ctx, e):
    emit('items', {'data': itemActions.getFilterdItems(e.data['cid'])})
    print('List items')

@event('itemremove')
def removeItem(ctx, e):
    if ctx.person[4] == 1:
        itemActions.delItem(e.data['iid'])
        print('Remove Item')
        emit('adminpage', {'page': 'productList', 'data': itemActions.getItems()})

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
def removesItem(ctx, e):
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
        # Error no card known
        print("Error: No card active in system!")
        logoutUser(ctx, e)
    else:
        if not (e.data['sid']):
            # Error no student number given
            print("Error: No student number or name given!")
        else:
            if not e.data['name']:
                print("Error: No name given!")
            else:
                # card hash and student number known
                userActions.newUser(e.data['name'], e.data['sid'], e.data['pass'], ctx.currentHash, e.data['keyname'])
                # show logged in screen
                print('Successful registration!')
                user = authenticateHash(ctx.currentHash)
                ctx.person = user
                loginUser(ctx, e)

@event('userPassLogin')
def loginUserPass(ctx, e):
    person = userActions.loginUser(e.data['sid'], e.data['password'])
    if person == None:
        logoutUser(ctx, e)
    else:
        ctx.person = person
        loginUser(ctx, e)

def loginUser(ctx, e):
    if ctx.person != None:
        ctx.basket = []
        emit('authenticated', {'pid': ctx.person[0], 'type': ctx.person[4], 'name': ctx.person[1], 'sid': ctx.person[2], 'balance': ctx.person[3]})
        print('Successful login!')

@event('logout')
def logoutUser(ctx, e):
    ctx.person = None
    ctx.currentHash = None # CurrentHash cache scanned card hash (logged in hash)
    ctx.basket = []
    emit('logout', {})
    statsGet(ctx, e)
    print('Successful logged out!')

@event('fakescan')
def scan(ctx, e):
    ctx.currentHash = e.data['id']
    user = authenticateHash(ctx.currentHash)
    if user == False:
        emit('newUser', {})
    else:
        ctx.person = user
        # show logged in screen
        loginUser(ctx, e)

def realscan(ctx, hash):
    ctx.user = None
    ctx.currentHash = hash
    user = authenticateHash(ctx.currentHash)
    if user == False:
        emit('newUser', {})
    else:
        ctx.person = user
        # show logged in screen
        loginUser(ctx, {})

@event('downloadcsv')
def csvdownload(ctx,e):
    csv.getcsv()

@event('downloadsql')
def sqldownload(ctx,e):
    csv.getSQLDump()