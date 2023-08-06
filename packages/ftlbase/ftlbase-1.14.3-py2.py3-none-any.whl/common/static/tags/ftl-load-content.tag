<ftl-load-content>
  <ul ref="contextMenu" class="dropdown-menu" role="menu" style="display:block">
    <li each={ item, index  in contextmenu_items }>
      <a data-action={ index } tabindex="-1" href="{ item.url }">{ item.text }</a>
    </li>
  </ul>
  <div ref="loadContent" class="{ classList }"></div>

  <script>
    var self = this;
    // self.id = opts.id === undefined ? '_' + Math.random().toString(36).substr(2, 9) : opts.id;
    self.classList = opts.classList === undefined ? 'ftl-load-content' : opts.classList;
    self.url = opts.url;
    self.safe = opts.safe === undefined ? false : opts.safe;
    self.contextmenu_items = opts.contextmenu_items;
    if (self.contextmenu_items !== undefined) {
      // contextmenu_items contém algo assim:
      // '{ [ {"text": "Opção 1", "url": "#/course/content/322/2/"},{"text": "Opção 2", "url": "#/course/content/323/2/"}] }'
      // Faz o bind do right-click
    }
    // self.href = opts.href
    // self.aria = opts.aria
    // self.icon = '<i class="fa fa-plus-square fa-fw" style="color:#ffffff;"></i>'
    // self.icon = opts.icon === undefined ? '' : opts.icon
    // self.iconStyle = opts.iconStyle === undefined ? 'color:#ffffff;' : opts.iconStyle
    // self.style = "padding-bottom: 5px; padding-top: 5px;color:#ffffff;"

    console.log("refs=", self.refs);
    console.log("url=", self.url);
    console.log("safe=", self.safe);

    // this.iconType = loading ? 'loading' : icon;
    self.on('mount', function () {
      riot.mount(self.refs.loadContent, 'ftl-include', {'include': {'url': self.url, 'safe': self.safe}});

      self.conteudo = $(self.refs.loadContent);
      self.conteudo.on('contextmenu', function (event) {
          event.preventDefault();
          $(self.refs.contextMenu).show()
            .css({
              position: "absolute",
              left: self.getMenuPosition(event.clientX, 'width', 'scrollLeft'),
              top: self.getMenuPosition(event.clientY, 'height', 'scrollTop')
            })
            // .off('click')
            .on('click', 'a', function (e) {
              $(self.refs.contextMenu).hide();
            });
        }
      );
      // Faz o hide do menu quando clica em um local qualquer do conteúdo
      self.conteudo.on('click.loadContent', function (e) {
        $(self.refs.contextMenu).hide();
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

    // self.conteudo = $(self.refs.loadContent);

    // self.conteudo.bind(
    //   'contextmenu',
    //   function (event) {
    //     $(self.refs.contextMenu).show()
    //       .css({
    //         position: "absolute",
    //         left: self.getMenuPosition(event.click_event.clientX, 'width', 'scrollLeft'),
    //         top: self.getMenuPosition(event.click_event.clientY, 'height', 'scrollTop')
    //       })
    //       .off('click')
    //       .on('click', 'a', function (e) {
    //         console.log(e);
    //         // e.preventDefault();
    //         // var node = event.node;
    //         // self.refs.contextMenuID.value = node.id;
    //         // self.refs.contextMenu.style.display = 'none' // self.refs.contextMenu.hide();
    //         // self.popitupModal(event.node.id, e.target.dataset.action); // Duplo click é edição do registro
    //       });
    //   }
    // );

  </script>

</ftl-load-content>
