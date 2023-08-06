riot.tag2('ftl-context-menu', '<ul ref="contextMenu" class="dropdown-menu contextMenu" role="menu" style="display:block"> <li each="{item, index  in contextmenu_items}"> <a data-action="{index}" tabindex="-1" href="{item.url}">{item.text}</a> </li> </ul>', '', '', function(opts) {
    var self = this;

    self.target = $(opts.target);
    self.contextmenu_items = opts.contextmenu_items;

    self.on('mount', function () {
      self.target.on('contextmenu', function (event) {
          event.preventDefault();
          $('.contextMenu').hide();
          $(self.refs.contextMenu).show()
            .css({
              position: "absolute",
              left: self.getMenuPosition(event.clientX, 'width', 'scrollLeft'),
              top: self.getMenuPosition(event.clientY, 'height', 'scrollTop')
            })

            .on('click', 'a', function () {
              $(self.refs.contextMenu).hide();
            });
        }
      );

      self.target.on('click.loadContent', function () {
        $('.contextMenu').hide();
      });

    });

    self.getMenuPosition = (mouse, direction, scrollDir) => {
      var win = $(window)[direction](),
        scroll = $(window)[scrollDir](),
        menu = $(self.refs.contextMenu)[direction](),
        position = mouse + scroll;

      if (mouse + menu > win && menu < mouse) {
        position -= menu;
      }

      return position;
    };

});
