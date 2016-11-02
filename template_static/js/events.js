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
      $('#authenticated').removeClass('screen')
      if ( typeof message.pid != 'undefined') {
        $('#authenticated_name').text(message.name)
        $('#authenticated_sid').text(message.sid)
        $('#authenticated_balance').text(message.balance)
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
      if (typeof message.data != 'undefined' ) {

        $('#basketList').empty();
        $ul = $('#basketList');
        message.data.map(function (item) {
          $('<li/>')
              .text('Item: ' + item.name + ' Price: ' + item.price + ' Quantity: ' + item.quantity + ' Total: ' + Math.round(((item.quantity * item.price) * 100)) / 100 + ' [x]')
              .attr('onClick', 'removeItem(' + item.iid + ')')
              .appendTo($ul)
        });

        $('#authItems').removeClass('screen');
      }
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
            $div = $('#' + currentAdminPage + 'Content');
            message.data.map(function(item) {
              $info = $('<div>')
                  .addClass('col-md-7')
                  .text('pid:' + item[0] + ", student#: " + item[2] + ", name: " + item[1] + ", balance: " + item[3])

              $user = $('<div>')
                  .text('Make User')
                  .attr('onClick', 'makeUser(' + item[0] + ')')
              $edit = $('<div>')
                  .text('edit')
                  .attr('onClick', 'editUser(' + item[0] + ')')
              $delete = $('<div>')
                  .text('delete')
                  .attr('onClick', 'deleteUser(' + item[0] + ')')
              $actions = $('<div>')
                  .addClass('col-md-5')
                  .append($user)
                  .append($edit)
                  .append($delete)
              $subDiv = $('<div>')
                  .addClass('row')
                  .append($info)
                  .append($actions)
                  .appendTo($div)

            });
          break;
        // get user list
        case 'userList':
          $('#' + currentAdminPage + 'Content').empty()
            $div = $('#' + currentAdminPage + 'Content');
            message.data.map(function(item) {
              $info = $('<div>')
                  .addClass('col-md-7')
                  .text('pid:' + item[0] + ", student#: " + item[2] + ", name: " + item[1] + ", balance: " + item[3])
              $user = $('<div>')
                  .text('Make Admin')
                  .attr('onClick', 'makeAdmin(' + item[0] + ')')
              $edit = $('<div>')
                  .text('edit')
                  .attr('onClick', 'editUser(' + item[0] + ')')
              $delete = $('<div>')
                  .text('delete')
                  .attr('onClick', 'deleteUser(' + item[0] + ')')
              $actions = $('<div>')
                  .addClass('col-md-5')
                  .append($user)
                  .append($edit)
                  .append($delete)
              $subDiv = $('<div>')
                  .addClass('row')
                  .append($info)
                  .append($actions)
                  .appendTo($div)
            });
          break;
        // get key list
        case 'keyList':
           $('#' + currentAdminPage + 'Content').empty()
            $div = $('#' + currentAdminPage + 'Content');
            message.data.map(function(item) {
              $info = $('<div>')
                  .addClass('col-md-7')
                  .text('Key id: ' + item[0] + ", Person id: " + item[1])
              $delete = $('<div>')
                  .text('delete key')
                  .attr('onClick', 'deleteKey(' + item[0] + ')')
              $actions = $('<div>')
                  .addClass('col-md-5')
                  .append($delete)
              $subDiv = $('<div>')
                  .addClass('row')
                  .append($info)
                  .append($actions)
                  .appendTo($div)
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

  block.fn.thankyou = function() {
    this.actions(function(e, message) {
      $('#authenticated').addClass('screen');
      $('#authItems').addClass('screen');
      $('#thankyou').removeClass('screen')
      setTimeout(function() {
        $.post('/logout', JSON.stringify({}))
      }, 3000);
    });
  };

  block.fn.logoutUser = function() {
    this.actions(function(e, message) {
      $('#basketList').empty();
      $('#photo').removeClass('screen')
      $('#events').removeClass('screen')
      $('#news').removeClass('screen')
      $('#statistics').removeClass('screen')
      $('#authenticated').addClass('col-md-4')
      $('#authenticated').addClass('screen')
      $('#admin_link').addClass('screen');
      $('#authCategories').addClass('screen');
      $('#thankyou').addClass('screen');
      $('#authItems').addClass('screen');
      goto('home')
    });
  };
})(jQuery, block);