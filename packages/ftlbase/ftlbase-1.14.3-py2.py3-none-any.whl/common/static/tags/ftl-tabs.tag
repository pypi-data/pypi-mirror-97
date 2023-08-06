<ftl-tabs>
  <ul if={ routes.length } class="nav nav-tabs" role="tablist">
    <li each={ route, index in routes } role="presentation" class={ active: route.active }>
      <a href="#{ route.ref }" id="#{ route.ref }-href" role="tab" onclick={ clickChange }
         data-toggle="tab" aria-controls="{ route.nome }" style="padding-top: 3px; padding-bottom: 3px;">
         { route.nome }
         &nbsp;</a>
     <span ref="#{ route.ref }-close" onclick={ clickClose } title="Remove essa página"><i class="fa fa-times"></i></span>
    </li>
  </ul>
  <div if={small.length != 0} class="container-fluid"><h4 if={ small } class={ color } align="center">{ small }</h4></div>
  <div class="tab-content panel-body">
    <div each={ route, index in routes } role="tabpanel" ref={ route.ref } id={ route.ref } class="tab-pane { active: route.active }"></div>
  </div>

  <style>
    :scope { display: block }

    .nav-tabs > li > span {
      display: none;
      cursor: pointer;
      position: absolute;
      right: 6px;
      top: 1px;
      color: #d73925;
    }

    .nav-tabs > li:hover > span {
      display: inline-block;
      opacity: 0.8;
    }

    .container {
      padding-bottom: 0px;
    }

    .container > h4 {
      margin-bottom: 0px;
      padding-bottom: 0px;
    }
  </style>

  <script>
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
        // Se a página não está carregada ou se a base da URL é diferente
        if (!r.loaded) {
          if (tag.debug) console.log('ftl-tabs: updated: ftl-include');
          var tags = riot.mount(tag.refs[r.ref], 'ftl-include',
                                { 'include': { 'url': tag.current_url, 'safe': true }});
          tags[0].on('loaded', function() {
            tag.loaded_ftlinclude(r, this) // tags[0] === this
          });
          r.loaded=true
        }
      })

      if (tag.debug) console.log('ftl-tabs: updated: end')
    })

    // Para evitar duplo disparo, assume que a URL já está alterada, pois é chamada originalmente do tratamento de route.
    // Então faz o tratamento se a página é para ser recarregada ou não
    tag.on('updateRoute', (key, nome, current_url, small, reload) => {
      if (tag.debug) console.log('ftl-tabs: updateRoute', key, nome, current_url, small);

      // Função em execução: '', 'Inclusão', 'Alteração', 'Exclusão'
      tag.small = nome + ' - ' + small;
      // Especifica cor do h4. Usa riot-style="color: { color } ou class={ color }
      if (current_url.endsWith('/add/'))         tag.color = 'text-primary'; // '#367fa9'  // Bootstrap Primary
      else if (current_url.split("/")[4] == '2') tag.color = 'text-warning'; // '#d58512'  // Bootstrap Warning hoover border
      else if (current_url.split("/")[4] == '3') tag.color = 'text-danger'; // '#d73925'  // Bootstrap Danger
      else tag.small = small;

      // Ativa tab conforme key de routes solicitada
      tag.routes.forEach(function(r) {
        r.active = (r.key === key)
      });

      // Filtra só os tabs ativos
      var filtered_routes = tag.routes.filter(function(r) {
        return (r.active)
      });

      // Se não existe tab ativo, então insere novo tab
      if (filtered_routes.length === 0) {
        // inclui novo tab
        tag.routes.push({ 'key': key, 'nome': nome,
                          'active': true, 'loaded': false,
                          'ref': tag.prefix+'-'+key,
                          'url': current_url, 'small': small,
                          'reload': reload });
      } else {
        // Mesmo que o tab tenha sido carregado anteriormente, mas a URL é diferente, então força o reload
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

    // Fecha tab específico passado como parâmetro
    tag.on('closeTab', (tab, goto) => {
      if (tag.debug) console.log('ftl-tabs: closeTab:', tab)

      tag.routes.forEach(function(r, key) {
        // Se a página não está carregada ou se a base da URL é diferente
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

    clickClose(e) {
//      e.preventDefault()
//      e.preventUpdate = true // your tag will not update automatically

      if (tag.debug) console.log('ftl-tabs: clickClose', e)

//      e.preventUpdate = true // your tag will not update automatically

      // RiotJS:
      //  e.currentTarget points to the element where the event handler is specified.
      //  e.target is the originating element. This is not necessarily the same as currentTarget.
      //  e.which is the key code in a keyboard event (keypress, keyup, etc…).
      //  e.item is the current element in a loop (each)

      // Deleta tab fechado
      tag.routes.splice(e.item.index, 1)

      // Se for o atual é o fechado e há mais de um tab então ativa o anterior
//      var act = ((tag.routes.length > 1) && (e.item.route.active))
      // Ativa tab anterior ao excluído
      if ((e.item.route.active) && (tag.routes.length > 0)) {
        var j = e.item.index - 1
        if (j < 0) j = 0
        tag.routes[j].active = true
//        route('/' + e.item.route.current_url)
      }

      // Filtra só os tabs ativos
      var filtered_routes = tag.routes.filter(function(r) {
        return (r.active)
      })

      if (filtered_routes.length > 0) {
        // Altera a url corrente
        filtered_routes.forEach(function(r) {
          if (r.active) {
            if (tag.debug) console.log('ftl-tabs: clickClose: route:', r.url)
            route('/' + r.url)
          }
        })
      } else { route('/') }

      if (tag.debug) console.log('ftl-tabs: clickClose: end')

    }

    clickChange(e) {
      if (tag.debug) console.log('ftl-tabs: clickChange', e)

      e.preventUpdate = true // your tag will not update automatically

      // Previne evento realizado junto com o clickClose, mantendo o elemento anterior que foi deletado
      if (tag.routes[e.item.index] === e.item.route) {
        tag.routes.forEach(function(r) {
          r.active = false
        })

        e.item.route.active = true

        if (tag.debug) console.log('ftl-tabs: clickChange: route:', e.item.route.url)
        route('/' + e.item.route.url)

      }
      if (tag.debug) console.log('ftl-tabs: clickChange: end')
    }

    loaded_ftlinclude(r, tag_ftlinclude) {
      if (tag.debug) console.log('ftl-tabs: loaded_ftlinclude', r, tag_ftlinclude)
      configuraPagina()
      // Faz a atualização do data-toggle=tab incluindo key
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
    }

  </script>
</ftl-tabs>
