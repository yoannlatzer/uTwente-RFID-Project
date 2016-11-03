function makeAdmin(pid) {
    $.post('/admin/admin/make', JSON.stringify({pid: pid}))
}

function makeUser(pid) {
    $.post('/admin/admin/remove', JSON.stringify({pid: pid}))
}

function editUser(pid) {
    $.post('/admin/user/edit', JSON.stringify({pid: pid}))
}

function updateUser() {
    $.post('/admin/user/update', JSON.stringify({
        pid: $('#editUserPid').val(),
        name: $('#editUserName').val(),
        balance: $('#editUserBalance').val(),
        sid: $('#editUserSid').val()
    }))
}

function deleteUser(pid) {
    $.post('/admin/user/remove', JSON.stringify({pid: pid}))
}

function deleteKey(kid) {
    $.post('/admin/key/remove', JSON.stringify({kid: kid}))
}

function editCategory(cid) {
    $.post('/admin/category/edit', JSON.stringify({cid: cid}))
}

function updateCategory() {
    $.post('/admin/category/update', JSON.stringify({
        cid: $('#editCategoryCid').val(),
        name: $('#editCategoryName').val()
    }))
}
function deleteCategory(cid) {
    $.post('/admin/category/remove', JSON.stringify({cid: cid}))
}

function editItem(iid) {
    $.post('/admin/item/edit', JSON.stringify({iid: iid}))
}

function updateItem() {
    $.post('/admin/item/update', JSON.stringify({
        iid: $('#editItemIid').val(),
        name: $('#editItemName').val(),
        cid: $('#editItemCategory').val(),
        price: $('#editItemPrice').val(),
        stock: $('#editItemStock').val(),
        image: $('#editItemUrl').val()
    }))
}
function deleteItem(iid) {
    $.post('/admin/item/remove', JSON.stringify({iid: iid}))
}

function removeOrder(oid) {
    $.post('/admin/order/remove', JSON.stringify({oid: oid}))
}

function removeOrderItem(oid, iid) {
    $.post('/admin/orderitem/remove', JSON.stringify({oid: oid, iid: iid}))
}

function downloadcsv1() {
    $.post('/admin/downloadcsv',JSON.stringify({}))
}

function downloadsql1() {
    $.post('/admin/downloadsql',JSON.stringify({}))
}