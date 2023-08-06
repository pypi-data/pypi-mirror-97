<ftl-context-menu>
  <ul ref="contextMenu" class="dropdown-menu contextMenu" role="menu" style="display:block">
    <li each={ item, index  in contextmenu_items }>
      <a data-action={ index } tabindex="-1" href="{ item.url }">{ item.text }</a>
    </li>
  </ul>

  <script>
    var self = this;

    self.target = $(opts.target);
    self.contextmenu_items = opts.contextmenu_items;

    // console.log("refs=", self.refs);
    // console.log("target=", self.target);
    // console.log("contextmenu_items=", self.contextmenu_items);

    // this.iconType = loading ? 'loading' : icon;
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
            // .off('click')
            .on('click', 'a', function () {
              $(self.refs.contextMenu).hide();
            });
        }
      );
      // Faz o hide do menu quando clica em um local qualquer do conteúdo
      self.target.on('click.loadContent', function () {
        $('.contextMenu').hide();
      });

    });

    // Tratamento de contextmenu
    self.getMenuPosition = (mouse, direction, scrollDir) => {
      var win = $(window)[direction](),
        scroll = $(window)[scrollDir](),
        menu = $(self.refs.contextMenu)[direction](),
        position = mouse + scroll;

      // opening menu would pass the side of the page
      if (mouse + menu > win && menu < mouse) {
        position -= menu;
      }

      return position;
    };

  </script>

</ftl-context-menu>
