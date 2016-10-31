(function($, block) {
  block.fn.newUser = function() {
    this.actions(function(e, message){
      goto('newUser')
    });
  };

  block.fn.authenticatedUser = function() {
    this.actions(function(e, message){
      $('#authenticated_name').text('Name: ' + message.name)
      $('#authenticated_sid').text('Student#: ' + message.sid)
      $('#authenticated_type').text('Type: ' + message.type)
      $('#authenticated_balance').text('Balance: ??')
      if (message.type == 1) {
        // is admin
        $('#admin_link').removeClass('screen');

      }
      goto('authenticated')
    });
  };

  block.fn.admin = function() {
    this.actions(function(e, message){
      $('#admin_link').addClass('screen');
      goto('admin')
    });
  };

  block.fn.adminpage = function() {
    var currentAdminPage = 'adminList'
    $('#' + currentAdminPage).removeClass('screen');

    this.actions(function(e, message){
      $('#' + currentAdminPage).addClass('screen');
      $('#' + message.page).removeClass('screen');
      currentAdminPage = message.page

      switch(currentAdminPage) {
        // get admin list
        case 'adminList':
            $('#' + currentAdminPage + 'Content').empty()
            $ul =  $('#' + currentAdminPage + 'Content').append('<ul>');
            message.data.map(function(item) {
              $li = $('<li/>')
                .text('pid:' + item[0] + ", student#: " + item[2] + ", name: " + item[1] + ", balance: " + item[4] + " - [ Make user | edit | Delete ]")
                .appendTo($ul)
            });
          break;
        // get user list
        case 'userList':
          $('#' + currentAdminPage + 'Content').empty()
          $ul =  $('#' + currentAdminPage + 'Content').append('<ul>');
          message.data.map(function(item) {
            $li = $('<li/>')
                .text('pid:' + item[0] + ", student#: " + item[2] + ", name: " + item[1] + ", balance: " + item[4] + " - [ Make admin | edit | Delete ]")
                .appendTo($ul)
          });
          break;
        // get key list
        case 'keyList':
          $('#' + currentAdminPage + 'Content').empty()
          $ul =  $('#' + currentAdminPage + 'Content').append('<ul>');
          message.data.map(function(item) {
            console.log(item)
            $li = $('<li/>')
                .text('key id:' + item[1] + " <--> person id:" + item[0] + " - [ Delete key ]")
                .appendTo($ul)
          });
          break
        // get product list
        case 'productList':

          break
        // get product add page
        case 'productAdd':

          break
      }
    });
  };

  block.fn.logoutUser = function() {
    this.actions(function(e, message){
      $('#admin_link').addClass('screen');
      goto('home')
    });
  };
})(jQuery, block);