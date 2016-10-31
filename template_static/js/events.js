(function($, block) {
  block.fn.newUser = function() {
    this.actions(function(e, message){
      goto('newUser')
    });
  };

  block.fn.authenticatedUser = function() {
    this.actions(function(e, message){
      console.log(message)
      $('#authenticated_name').text('Name: ' + message.name)
      $('#authenticated_sid').text('Student#: ' + message.sid)
      $('#authenticated_type').text('Type: ' + message.type)
      $('#authenticated_balance').text('Balance: ??')
      goto('authenticated')
    });
  };

  block.fn.logoutUser = function() {
    this.actions(function(e, message){
      goto('home')
    });
  };
})(jQuery, block);