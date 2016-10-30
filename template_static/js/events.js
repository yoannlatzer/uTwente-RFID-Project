(function($, block) {
  block.fn.newUser = function() {
    this.actions(function(e, message){
      goto('newUser')
    });
  };

  block.fn.authenticatedUser = function() {
    this.actions(function(e, message){
      goto('authenticated')
    });
  };

  block.fn.logoutUser = function() {
    this.actions(function(e, message){
      goto('home')
    });
  };
})(jQuery, block);