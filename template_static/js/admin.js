function makeAdmin(pid) {
    $.post('/admin/admin/make', JSON.stringify({pid: pid}))
}

function makeUser(pid) {
    console.log(pid)
    $.post('/admin/admin/remove', JSON.stringify({pid: pid}))
}

function editUser(pid) {
    $.post('/admin/user/edit', JSON.stringify({pid: pid}))
}

function deleteUser(pid) {
    $.post('/admin/user/remove', JSON.stringify({pid: pid}))
}