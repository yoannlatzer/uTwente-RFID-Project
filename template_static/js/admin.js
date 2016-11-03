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

}

function deleteCategory(cid) {
    $.post('/admin/category/remove', JSON.stringify({cid: cid}))
}

function editItem(iid) {

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

