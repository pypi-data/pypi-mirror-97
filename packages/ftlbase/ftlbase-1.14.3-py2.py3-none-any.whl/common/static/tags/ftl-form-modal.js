riot.tag2('ftl-form-modal', '<div class="modal" ref="editModal" role="dialog" aria-labelledby="ftl-form-modal" method="post" show="{opts.modal.isvisible}"> <div class="modal-dialog modal-lg" role="document"> <div class="modal-content"> <form ref="modalForm" class="form-group" method="POST" onsubmit="{submit}"> <div class="modal-header"> <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button> <h4 class="modal-title" ref="ftlmodaltitle">{opts.data.modaltitle}</h4> </div> <div class="modal-body"> <div ref="ftlmodalbody"></div> </div> <div class="modal-footer"> <input ref="contextMenuID" type="hidden" value=""> <input ref="contextMenuParent" type="hidden" value=""> <input ref="pk" type="hidden" riot-value="{opts.data.pk}"> <button each="{buttons}" type="{type}" name="{nome}" class="button {\'btn btn-\' + cls} btn-sm" onclick="{menuclick}"> {text} </button> </div> </form> </div> </div> </div> <ul ref="contextMenu" class="dropdown-menu" role="menu" style="display:none"> <li><a tabindex="-1">{opts.data.modaltitle}</a></li> <li class="divider"></li> <li><a ref="contextCreate" data-action="1" tabindex="-1" href="#">Criar Novo Registro</a></li> <li><a ref="contextAlter" data-action="2" tabindex="-1" href="#">Alterar</a></li> <li><a ref="contextDelete" data-action="3" tabindex="-1" href="#">Excluir</a></li> </ul>', '', '', function(opts) {
    self = this;
    self.buttons = [];

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

    this.menuclick = function(e) {

      if (e.target.name === 'cancel') {

        e.preventDefault();
      }

      $(self.refs.editModal).modal("toggle");
      return false;
    }.bind(this)

    this.popitupModal = function(pk, acao) {

      self.refs.contextMenuID.value = pk;
      self.refs.contextMenu.style.display = 'none';

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
    }.bind(this)

    self.on('mount', () => {
      if (!opts.modal) opts.modal = {isvisible: false, contextmenu: false, idtree: 'tree1' };
      if (!opts.data) opts.data = {pk: 1, action: 1, acaoURL: '/finan/contaContabil/', updateParent: '', modaltitle: 'Modal Title'};

      self.refs.ftlmodaltitle.innerHTML = opts.data.modaltitle;
      self.refs.pk = opts.data.pk;
      self.tree = $('#'+self.opts.modal.idtree);

      self.tree.tree({
          dragAndDrop: true,
          autoOpen: true,
          autoEscape: false,
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

          }
      });

      self.tree.bind(
          'tree.move',
          function(event) {

              event.preventDefault();
              var new_parent;
              if (event.move_info.position === 'inside') {

                  new_parent = event.move_info.target_node.id;

              }
              if (event.move_info.position === 'after') {

                  new_parent = event.move_info.target_node.parent.id;

              }

              if (new_parent !== event.move_info.moved_node.parent.id) {

                  $.post(self.opts.data.updateParent,
                  {
                      no: event.move_info.moved_node.id,
                      pai: new_parent
                  },
                  function(data, status, xhr){
                    if (xhr.status !== 200) {
                        alert("Status: >" + status+ "< \nxhr.status = >"+xhr.status+"<");
                    }

                    self.trigger("reloadTree", event.move_info.moved_node.id)
                  });
              }
          }
      );
      self.tree.bind(
        'tree.dblclick',
        function(event) {
          event.preventDefault();

          var node = event.node;
          self.refs.contextMenuID.value = node.id;
          self.popitupModal(node.id, '2');

        }
      );

      self.tree.bind(
        'tree.contextmenu',
        function(event) {

          var node = event.node;

          self.tree.tree('selectNode', node);
          self.refs.contextMenuID.value = (node.id);
          var nodeP = node.getPreviousNode();
          if (nodeP) {
            self.refs.contextMenuParent.value = (nodeP.id);
          }

          if (node.children.length > 0) {
              self.refs.contextDelete.style.display = 'none'
          } else {
              self.refs.contextDelete.style.display = 'block'
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

                        self.popitupModal(event.node.id, e.target.dataset.action);
                      });
        }
      )
    });

    self.close = () => {
      opts.modal.isvisible = false;
      self.trigger('close')
    };

    self.submit = (e) => {

      e.preventDefault();

      var $f = $(self.refs.modalForm);
      $f.find(":disabled").removeProp('disabled');
      var dados = $f.serialize();
      $.ajax({

          type: $f.attr('method'),
          url: $f.attr('action'),

          data: dados,
          success: function (data) {

              e.preventDefault();
              var pk = self.refs.contextMenuID.value;
              if (pk == null) {
                  pk = self.refs.contextMenuParent.value;
              }
              self.trigger("reloadTree", pk)

          },
          error: function(data) {
              console.log('Something went wrong: >'+data+'<')
          }
      });

      return false;
    };

    self.on('reloadTree', (selectedNode) => {
      self.tree.tree('reload', function() {
          var node = self.tree.tree('getNodeById', selectedNode);
          self.tree.tree('selectNode', node);
          self.tree.tree('openNode', node, false);

      })
    });
});


