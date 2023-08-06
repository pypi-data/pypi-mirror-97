<ftl-form-modal>

  <div class="modal" ref="editModal" role="dialog" aria-labelledby="ftl-form-modal" method="post" show="{ opts.modal.isvisible }">
    <div class="modal-dialog modal-lg" role="document">
      <div class="modal-content">
       <form ref="modalForm" class="form-group" method="POST" onsubmit={ submit }>
        <div class="modal-header">
          <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
          <h4 class="modal-title" ref="ftlmodaltitle">{ opts.data.modaltitle }</h4>
        </div>
        <div class="modal-body">
          <div ref='ftlmodalbody'></div>
        </div>
        <div class="modal-footer">
          <input ref="contextMenuID" type="hidden" value="">
          <input ref="contextMenuParent" type="hidden" value="">
          <input ref="pk" type="hidden" value="{ opts.data.pk }">
          <button each="{ buttons }" type="{ type }" name="{ nome }" class="button { 'btn btn-' + cls } btn-sm" onclick="{ menuclick }">
            { text }
          </button>

        </div>
      </form>
      </div>
    </div>
  </div>
  <ul ref="contextMenu" class="dropdown-menu" role="menu" style="display:none">
    <li><a tabindex="-1">{ opts.data.modaltitle }</a></li>
    <li class="divider"></li>
    <li><a ref="contextCreate" data-action='1' tabindex="-1" href="#">Criar Novo Registro</a></li>
    <li><a ref="contextAlter"  data-action='2' tabindex="-1" href="#">Alterar</a></li>
    <li><a ref="contextDelete" data-action='3' tabindex="-1" href="#">Excluir</a></li>
  </ul>


  <script>
    self = this;
    self.buttons = [];

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

    menuclick(e) {
      // self.popitupModal(self.refs.contextMenuID.value, '2')
      if (e.target.name === 'cancel') {
        // Não faz nada
        e.preventDefault();
      }
      // } else if (e.target.name == 'DELETE') {
      //   // Executa request de deleção
      // } else if (e.target.name == 'save') {
      //   // Executa request de update
      // }
      // console.log(e.target.name)
      $(self.refs.editModal).modal("toggle");
      return false;
    }

    popitupModal(pk, acao) {
      // $btnSave = $("#modal-button-save");
      // $btnDELETE = $("#modal-button-delete");
      // if (acao == 1 || acao == 2){
      //   $btnSave.show();
      //   $btnDELETE.hide();
      // }
      // else {
      //   $btnSave.hide();
      //   $btnDELETE.show();
      // };
      //$modal.find('.modal-title').text('Alteração do ID ' + pk);
      // não precisa pois faz o update polo riot. self.refs.editModal.find('.modal-title').text(self.opts.data.modaltitle); // tinha que ser o modaltitle
      self.refs.contextMenuID.value = pk;
      self.refs.contextMenu.style.display = 'none'; // self.refs.contextMenu.hide();

      if (acao === undefined) {
        return false;
      }

      self.buttons = [];
      if (acao === '1' || acao === '2'){
        self.buttons.push({ type: 'submit', nome: 'save', cls:  'primary', text: 'Salvar' });
      } else {
        self.buttons.push({ type: 'submit', nome: 'DELETE', cls:  'danger', text: 'Confirmar exclusão do registro' });
      }
      self.buttons.push({type: 'button', nome: 'cancel', cls:  'default', text: 'Cancelar' });

      var url = self.opts.data.acaoURL+pk+'/'+acao+'/'+self.opts.data.pk+'/';
      $(self.refs.modalForm).attr('action', url);
      $(self.refs.ftlmodalbody).load(
        url,
        null,
        function(response, status, xhr){
            if (xhr.status !== 200) {
                alert("Status: >" + status+ "< \nxhr.status = >"+xhr.status+"<");
            }
            else{
              configuraPagina();
            }
        }
      );
      self.update();
      $(self.refs.editModal).modal("toggle");
      return false;
    }

    self.on('mount', () => {
      if (!opts.modal) opts.modal = {isvisible: false, contextmenu: false, idtree: 'tree1' };
      if (!opts.data) opts.data = {pk: 1, action: 1, acaoURL: '/finan/contaContabil/', updateParent: '', modaltitle: 'Modal Title'};

      self.refs.ftlmodaltitle.innerHTML = opts.data.modaltitle;
      self.refs.pk = opts.data.pk;
      self.tree = $('#'+self.opts.modal.idtree);

      self.tree.tree({
          dragAndDrop: true,
          autoOpen: true, // false deixa tudo fechado, 0 deixa só o primeiro nível aberto
          autoEscape: false, // deixa o html que vier do json disponível para ser executado
          slide: false,
          onLoading: function(is_loading, node, $el) {
              var $body = $("body");
              if (is_loading) {
                  $body.addClass("loading");
              } else {
                  $body.removeClass("loading");
              }
          },
          onLoadFailed: function(response) {
              //
          }
      });

      self.tree.bind(
          'tree.move',
          function(event) {
              //console.log('moved_node', event.move_info.moved_node);
              //console.log('target_node', event.move_info.target_node);
              //console.log('position', event.move_info.position);
              //console.log('previous_parent', event.move_info.previous_parent);
              // var updateParentText="{{ updateParent }}";
              event.preventDefault();
              var new_parent;
              if (event.move_info.position === 'inside') {
                  // Movendo para um item, novo parent = target
                  new_parent = event.move_info.target_node.id;
                  //alert('Movendo para inside de um item, novo parent = target');
              }
              if (event.move_info.position === 'after') {
                  // Movendo para um item, novo parent = target.parent, se target.parent é null então está na raiz
                  new_parent = event.move_info.target_node.parent.id;
                  //alert('Movendo para after de um item, novo parent = target.parent');
              }
              //var txt = event.move_info.moved_node.id + " - " + new_parent;
              //$("#teste").val(txt);
              if (new_parent !== event.move_info.moved_node.parent.id) {
                  // Novo parent diferente do parent original, então faz a atualização de parent
                  $.post(self.opts.data.updateParent,
                  {
                      no: event.move_info.moved_node.id,
                      pai: new_parent
                  },
                  function(data, status, xhr){
                    if (xhr.status !== 200) {
                        alert("Status: >" + status+ "< \nxhr.status = >"+xhr.status+"<");
                    }
                    // Após o post, faz reload da tree e vai para o node que foi movido
                    self.trigger("reloadTree", event.move_info.moved_node.id)
                  });
              }
          }
      );
      self.tree.bind(
        'tree.dblclick',
        function(event) {
          event.preventDefault();
          // event.node is the clicked node
          var node = event.node;
          self.refs.contextMenuID.value = node.id;
          self.popitupModal(node.id, '2'); // Duplo click força edição do registro = '2'
          //alert(node.name);
          //console.log(event.node);
        }
      );

      self.tree.bind(
        'tree.contextmenu',
        function(event) {
          // The clicked node is 'event.node'
          var node = event.node;
          // $(event.target).tree('selectNode', node);
          self.tree.tree('selectNode', node);
          self.refs.contextMenuID.value = (node.id);
          var nodeP = node.getPreviousNode();
          if (nodeP) {
            self.refs.contextMenuParent.value = (nodeP.id);
          }
          //$contextMenuParent.val(node.parent.id);
          //pk = node.id;
          if (node.children.length > 0) {
              self.refs.contextDelete.style.display = 'none' //$(self.refs.contextDelete).hide();
          } else {
              self.refs.contextDelete.style.display = 'block' //$(self.refs.contextDelete).show();
          }
          $(self.refs.contextMenu).show()
                      .css({
                        position: "absolute",
                        left: self.getMenuPosition(event.click_event.clientX, 'width', 'scrollLeft'),
                        top:  self.getMenuPosition(event.click_event.clientY, 'height', 'scrollTop')
                      })
                      .off('click')
                      .on('click', 'a', function (e) {
                        e.preventDefault();
                        // var node = event.node;
                        // self.refs.contextMenuID.value = node.id;
                        // self.refs.contextMenu.style.display = 'none' // self.refs.contextMenu.hide();
                        // self.popitupModal(event.node.id, event.target.dataset.action); // Duplo click é edição do registro
                        self.popitupModal(event.node.id, e.target.dataset.action); // Duplo click é edição do registro
                      });
        }
      )
    });

    self.close = () => {
      opts.modal.isvisible = false;
      self.trigger('close')
    };

    self.submit = (e) => {
      // var pk = self.refs.pk.value;
      e.preventDefault();
      // console.log('submit')
      var $f = $(self.refs.modalForm);
      $f.find(":disabled").removeProp('disabled');
      var dados = $f.serialize();
      $.ajax({
          // type: $f.attr('method'),
          // url: $f.attr('action'),
          type: $f.attr('method'),
          url: $f.attr('action'),
          //url: acaoURL+pk+'/4/',
          data: dados,
          success: function (data) {
              // console.log('success')
              // Após o post, faz reload da tree e vai para o node que foi movido
              e.preventDefault();
              var pk = self.refs.contextMenuID.value;
              if (pk == null) {
                  pk = self.refs.contextMenuParent.value;
              }
              self.trigger("reloadTree", pk)
              // self.tree.tree('reload', function() {
              //     //console.log('data is loaded');
              //     var pk = self.refs.contextMenuID.value;
              //     if (pk == null) {
              //         pk = self.refs.contextMenuParent.value;
              //     }
              //     var node = self.tree.tree('getNodeById', pk);
              //     self.tree.tree('selectNode', node);
              //     self.tree.tree('openNode', node, false);
              // });
          },
          error: function(data) {
              console.log('Something went wrong: >'+data+'<')
          }
      });
      // $f.modal("toggle");
      return false;
    };

    self.on('reloadTree', (selectedNode) => {
      self.tree.tree('reload', function() {
          var node = self.tree.tree('getNodeById', selectedNode); //pk
          self.tree.tree('selectNode', node);
          self.tree.tree('openNode', node, false);
          //$tree.tree('scrollToNode', node);
      })
    });
  </script>

</ftl-form-modal>


