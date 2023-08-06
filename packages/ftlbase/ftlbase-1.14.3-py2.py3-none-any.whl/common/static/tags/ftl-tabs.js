riot.tag2('ftl-tabs', '<ul if="{routes.length}" class="nav nav-tabs" role="tablist"> <li each="{route, index in routes}" role="presentation" class="{active: route.active}"> <a href="#{route.ref}" id="#{route.ref}-href" role="tab" onclick="{clickChange}" data-toggle="tab" aria-controls="{route.nome}" style="padding-top: 3px; padding-bottom: 3px;"> {route.nome} &nbsp;</a> <span ref="#{route.ref}-close" onclick="{clickClose}" title="Remove essa página"><i class="fa fa-times"></i></span> </li> </ul> <div if="{small.length != 0}" class="container-fluid"><h4 if="{small}" class="{color}" align="center">{small}</h4></div> <div class="tab-content panel-body"> <div each="{route, index in routes}" role="tabpanel" ref="{route.ref}" id="{route.ref}" class="tab-pane {active: route.active}"></div> </div>', 'ftl-tabs,[data-is="ftl-tabs"]{ display: block } ftl-tabs .nav-tabs > li > span,[data-is="ftl-tabs"] .nav-tabs > li > span{ display: none; cursor: pointer; position: absolute; right: 6px; top: 1px; color: #d73925; } ftl-tabs .nav-tabs > li:hover > span,[data-is="ftl-tabs"] .nav-tabs > li:hover > span{ display: inline-block; opacity: 0.8; } ftl-tabs .container,[data-is="ftl-tabs"] .container{ padding-bottom: 0px; } ftl-tabs .container > h4,[data-is="ftl-tabs"] .container > h4{ margin-bottom: 0px; padding-bottom: 0px; }', '', function(opts) {
    var tag = this;
    tag.debug = false;
    tag.prefix = 'ftl-tab';
    tag.routes = [];
    tag.current_url = '';
    tag.small = '';
    tag.color = '';

    tag.on('updated', () => {
      if (tag.debug) console.log('ftl-tabs: updated');

      tag.routes.forEach(function(r, key) {

        if (!r.loaded) {
          if (tag.debug) console.log('ftl-tabs: updated: ftl-include');
          var tags = riot.mount(tag.refs[r.ref], 'ftl-include',
                                { 'include': { 'url': tag.current_url, 'safe': true }});
          tags[0].on('loaded', function() {
            tag.loaded_ftlinclude(r, this)
          });
          r.loaded=true
        }
      })

      if (tag.debug) console.log('ftl-tabs: updated: end')
    })

    tag.on('updateRoute', (key, nome, current_url, small, reload) => {
      if (tag.debug) console.log('ftl-tabs: updateRoute', key, nome, current_url, small);

      tag.small = nome + ' - ' + small;

      if (current_url.endsWith('/add/'))         tag.color = 'text-primary';
      else if (current_url.split("/")[4] == '2') tag.color = 'text-warning';
      else if (current_url.split("/")[4] == '3') tag.color = 'text-danger';
      else tag.small = small;

      tag.routes.forEach(function(r) {
        r.active = (r.key === key)
      });

      var filtered_routes = tag.routes.filter(function(r) {
        return (r.active)
      });

      if (filtered_routes.length === 0) {

        tag.routes.push({ 'key': key, 'nome': nome,
                          'active': true, 'loaded': false,
                          'ref': tag.prefix+'-'+key,
                          'url': current_url, 'small': small,
                          'reload': reload });
      } else {

        filtered_routes.forEach(function(r) {
          if ((r.url !== current_url) || (r.reload)) {
            r.url = current_url;
            r.loaded = false;
          }
        })
      }

      tag.current_url = current_url

      tag.update()

      if (tag.debug) console.log('ftl-tabs: updateRoute: end')
    })

    tag.on('closeTab', (tab, goto) => {
      if (tag.debug) console.log('ftl-tabs: closeTab:', tab)

      tag.routes.forEach(function(r, key) {

        if (r.nome === tab) {
          if (tag.debug) console.log('ftl-tabs: closeTab: close')
          tag.refs['#' + r.ref + '-close'].click()
        }
      })

      if (goto != undefined) {
        window.location.href=goto
      }

      if (tag.debug) console.log('ftl-tabs: closeTab: end')
    })

    this.clickClose = function(e) {

      if (tag.debug) console.log('ftl-tabs: clickClose', e)

      tag.routes.splice(e.item.index, 1)

      if ((e.item.route.active) && (tag.routes.length > 0)) {
        var j = e.item.index - 1
        if (j < 0) j = 0
        tag.routes[j].active = true

      }

      var filtered_routes = tag.routes.filter(function(r) {
        return (r.active)
      })

      if (filtered_routes.length > 0) {

        filtered_routes.forEach(function(r) {
          if (r.active) {
            if (tag.debug) console.log('ftl-tabs: clickClose: route:', r.url)
            route('/' + r.url)
          }
        })
      } else { route('/') }

      if (tag.debug) console.log('ftl-tabs: clickClose: end')

    }.bind(this)

    this.clickChange = function(e) {
      if (tag.debug) console.log('ftl-tabs: clickChange', e)

      e.preventUpdate = true

      if (tag.routes[e.item.index] === e.item.route) {
        tag.routes.forEach(function(r) {
          r.active = false
        })

        e.item.route.active = true

        if (tag.debug) console.log('ftl-tabs: clickChange: route:', e.item.route.url)
        route('/' + e.item.route.url)

      }
      if (tag.debug) console.log('ftl-tabs: clickChange: end')
    }.bind(this)

    this.loaded_ftlinclude = function(r, tag_ftlinclude) {
      if (tag.debug) console.log('ftl-tabs: loaded_ftlinclude', r, tag_ftlinclude)
      configuraPagina()

      var link = $('#'+r.ref)
      if (tag.debug) console.log('ftl-tabs: loaded_ftlinclude 2', link)
      if (tag.debug) console.log('ftl-tabs: loaded_ftlinclude 3', link.find('[data-toggle="tab"]'))
      link.find('[data-toggle="tab"]')
        .each(function() {
          this.href = this.href.replace("#","#" + r.key);
        })
      if (tag.debug) console.log('ftl-tabs: loaded_ftlinclude 4', link.find('div > .tab-pane'))
      link.find('div > .tab-pane')
        .each(function() {
          this.id = r.key + this.id;
        })
    }.bind(this)

});
