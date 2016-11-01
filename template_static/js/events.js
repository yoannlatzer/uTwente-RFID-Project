(function($, block) {
  block.fn.newUser = function() {
    this.actions(function(e, message) {
      goto('newUser')
    });
  };

  block.fn.authenticatedUser = function() {
    this.actions(function(e, message) {
      $('#photo').addClass('screen')
      $('#events').addClass('screen')
      $('#news').addClass('screen')
      $('#statistics').addClass('screen')
      $('#authenticated').removeClass('col-md-4')
      if ( typeof message.pid != 'undefined') {
        $('#authenticated_name').text('Name: ' + message.name)
        $('#authenticated_sid').text('Student#: ' + message.sid)
        $('#authenticated_type').text('Type: ' + message.type)
        $('#authenticated_balance').text('Balance: ' + message.balance)
      }
      if ($('#authCategories').hasClass('screen') == true && $('#authItems').hasClass('screen') == true) {
        $('#authCategories').removeClass('screen');
        $.post('/categories/list', JSON.stringify({}));
      }
      if (message.type == 1) {
        // is admin
        $('#admin_link').removeClass('screen');
      }
      goto('authenticated')
    });
  };

  block.fn.categories = function() {
    this.actions(function(e, message) {
      $('#authItems').addClass('screen');
      $('#categoriesLink').addClass('screen');
      $('#authCategories').removeClass('screen');
      $('#authCategories').empty();
      $div =  $('#authCategories');
      message.data.map(function(cat) {
        $('<div/>')
            .attr('onClick', 'setCategory(' + cat[0] + ')')
            .text(cat[1])
            .appendTo($div)
        });
    })
  };

  block.fn.items = function() {
    this.actions(function(e, message) {
      $('#authCategories').addClass('screen');
      $('#categoriesLink').removeClass('screen');
      $('#authItems').empty();
      $div =  $('#authItems');
      message.data.map(function(i) {
        $('<div/>')
            .attr('onClick', 'selectItem(' + i[0] + ')')
            .text(i[1] + ' Price: ' + i[3])
            .appendTo($div)
      });
      $('#authItems').removeClass('screen');
    })
  }

  block.fn.basket = function() {
    this.actions(function(e, message) {
      $('#basketList').empty();
      $ul =  $('#basketList');
      message.data.map(function(item) {
        $('<li/>')
            .text('Item: ' + item.name + ' Price: ' + item.price + ' Quantity: ' + item.quantity + ' Total: ' + Math.round(((item.quantity * item.price)*100))/100 + ' [x]')
            .attr('onClick', 'removeItem('+item.iid+')')
            .appendTo($ul)
      });
      $('#authItems').removeClass('screen');
    })
  }

  block.fn.admin = function() {
    this.actions(function(e, message) {
      $('#admin_link').addClass('screen');
      goto('admin')
    });
  };

  block.fn.adminpage = function() {
    var currentAdminPage = 'adminList'
    $('#' + currentAdminPage).removeClass('screen');

    this.actions(function(e, message) {
      $('#' + currentAdminPage).addClass('screen');
      $('#' + message.page).removeClass('screen');
      currentAdminPage = message.page

      switch(currentAdminPage) {
        // get admin list
        case 'adminList':
            $('#' + currentAdminPage + 'Content').empty()
            $ul =  $('#' + currentAdminPage + 'Content').append('<ul>');
            message.data.map(function(item) {
              $('<li/>')
                .text('pid:' + item[0] + ", student#: " + item[2] + ", name: " + item[1] + ", balance: " + item[4] + " - [ Make user | edit | Delete ]")
                .appendTo($ul)
            });
          break;
        // get user list
        case 'userList':
          $('#' + currentAdminPage + 'Content').empty()
          $ul =  $('#' + currentAdminPage + 'Content').append('<ul>');
          message.data.map(function(item) {
            $('<li/>')
                .text('pid:' + item[0] + ", student#: " + item[2] + ", name: " + item[1] + ", balance: " + item[4] + " - [ Make admin | edit | Delete ]")
                .appendTo($ul)
          });
          break;
        // get key list
        case 'keyList':
          $('#' + currentAdminPage + 'Content').empty()
          $ul =  $('#' + currentAdminPage + 'Content').append('<ul>');
          message.data.map(function(item) {
            $('<li/>')
                .text('key id: ' + item[1] + " <--> person id: " + item[0] + " - [ Delete key ]")
                .appendTo($ul)
          });
          break
        // get category list
        case 'categoryList':
          $('#' + currentAdminPage + 'Content').empty()
          $ul =  $('#' + currentAdminPage + 'Content').append('<ul>');
          message.data.map(function(item) {
            $('<li/>')
                .text('id: ' + item[0] + " Name: " + item[1] + " - [ Edit | Delete ]")
                .appendTo($ul)
          });
          break
        // get product list
        case 'productList':
          $('#' + currentAdminPage + 'Content').empty()
          $ul =  $('#' + currentAdminPage + 'Content').append('<ul>');
          message.data.map(function(item) {
            $('<li/>')
                .text('id: ' + item[0] + " Name: " + item[1] + " - [ Edit | Delete ]")
                .appendTo($ul)
          });
          break
        // get product add page
        case 'productAdd':
          $('#addItemCategory').empty()
          $select =  $('#addItemCategory')
          message.data.map(function(item) {
            $('<option/>')
                .attr('value', item[0])
                .text(item[1])
                .appendTo($select)
          });
          break
      }
    });
  };

  block.fn.logoutUser = function() {
    this.actions(function(e, message) {
      $('#photo').removeClass('screen')
      $('#events').removeClass('screen')
      $('#news').removeClass('screen')
      $('#statistics').removeClass('screen')
      $('#authenticated').addClass('col-md-4')
      $('#admin_link').addClass('screen');
      $('#authCategories').addClass('screen');
      $('#authItems').addClass('screen');
      goto('home')
    });
  };
})(jQuery, block);