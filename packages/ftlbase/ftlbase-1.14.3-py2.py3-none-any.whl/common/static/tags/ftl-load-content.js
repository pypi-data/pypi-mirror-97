riot.tag2('ftl-load-content', '<ul ref="contextMenu" class="dropdown-menu" role="menu" style="display:block"> <li each="{item, index  in contextmenu_items}"> <a data-action="{index}" tabindex="-1" href="{item.url}">{item.text}</a> </li> </ul> <div ref="loadContent" class="{classList}"></div>', '', '', function(opts) {
    var self = this;

    self.classList = opts.classList === undefined ? 'ftl-load-content' : opts.classList;
    self.url = opts.url;
    self.safe = opts.safe === undefined ? false : opts.safe;
    self.contextmenu_items = opts.contextmenu_items;
    if (self.contextmenu_items !== undefined) {

    }

    console.log("refs=", self.refs);
    console.log("url=", self.url);
    console.log("safe=", self.safe);

    self.on('mount', function () {
      riot.mount(self.refs.loadContent, 'ftl-include', {include: {url: self.url, safe: self.safe}});

      self.conteudo = $(self.refs.loadContent);
      self.conteudo.on('contextmenu', function (event) {
          event.preventDefault();
          $(self.refs.contextMenu).show()
            .css({
              position: "absolute",
              left: self.getMenuPosition(event.clientX, 'width', 'scrollLeft'),
              top: self.getMenuPosition(event.clientY, 'height', 'scrollTop')
            })

            .on('click', 'a', function (e) {
              $(self.refs.contextMenu).hide();
            });
        }
      );

      self.conteudo.on('click.loadContent', function (e) {
        $(self.refs.contextMenu).hide();
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
