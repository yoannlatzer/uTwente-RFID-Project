function makeAdmin(pid) {
    $.post('/admin/admin/make', JSON.stringify({pid: pid}))
}

function makeUser(pid) {
    $.post('/admin/admin/remove', JSON.stringify({pid: pid}))
}

function editUser(pid) {
    $.post('/admin/user/edit', JSON.stringify({pid: pid}))
}

function deleteUser(pid) {
    $.post('/admin/user/remove', JSON.stringify({pid: pid}))
}

function deleteKey(kid) {
    $.post('/admin/key/remove', JSON.stringify({kid: kid}))
}

function editCategory(cid) {

}

function removeCategory(cid) {

}

function editItem(iid) {

}

function removeItem(iid) {

}

function removeOrder(oid) {
    $.post('/admin/order/remove', JSON.stringify({oid: oid}))
}

function removeOrderItem(oid, iid) {
    $.post('/admin/orderitem/remove', JSON.stringify({oid: oid, iid: iid}))
}

