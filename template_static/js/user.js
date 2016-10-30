function register() {
    var studentNumber = $('#register_studentnr').val();
    var name = $('#register_name').val();
    $.post('/register', JSON.stringify({sid: studentNumber, name: name}));
}

function logout() {
    $.post('/logout', JSON.stringify({}));
}