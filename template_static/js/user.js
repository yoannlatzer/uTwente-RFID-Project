function register() {
    var studentNumber = $('#register_studentnr').val();
    var name = $('#register_name').val();
    var password = $('#register_password').val();
    $.post('/register', JSON.stringify({sid: studentNumber, name: name, pass: password}));
}

function login() {
    var sid = $('#loginsid').val();
    var password = $('#loginpassword').val();
    $.post('/login', JSON.stringify({sid: sid, password: password}));
}

function logout() {
    $.post('/logout', JSON.stringify({}));
}