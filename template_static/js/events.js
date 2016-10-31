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
    });
  };

  block.fn.logoutUser = function() {
    this.actions(function(e, message){
      $('#admin_link').addClass('screen');
      goto('home')
    });
  };
})(jQuery, block);