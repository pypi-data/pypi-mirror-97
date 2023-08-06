<ftl-modal>

  <div class="modal" ref="editModal" role="dialog" aria-labelledby="ftl-modal" method="post" show="{ opts.modal.isvisible }">
    <div class="modal-dialog { opts.modal.cls }" role="document">
      <div class="modal-content">
       <form ref="modalForm" class="form-group" method="POST" onsubmit={ submit }>
        <div class="modal-header">
          <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
          <h4 class="modal-title" ref="ftlmodaltitle"><strong>{ opts.data.modaltitle }</strong></h4>
        </div>
        <div class="modal-body">
          <div ref='ftlmodalbody'></div>
        </div>
        <div class="modal-footer">
          <input ref="pk" type="hidden" value="{ opts.data.pk }">
          <button each="{ buttons }" type="{ type }" name="{ nome }" class="button { 'btn btn-' + cls } btn-sm" onclick="{ menuclick }">
            { text }
          </button>

        </div>
      </form>
      </div>
    </div>
  </div>

  <script>
    self = this;
    self.buttons = [];

    self.on('popup', () => {
      if (opts.data.acao === undefined) {
        return false;
      }

      self.buttons = [];
      if (opts.data.acao === '1' || opts.data.acao === '2'){
        self.buttons.push({ type: 'submit', nome: 'save', cls:  'primary', text: 'Salvar' });
      }
      if (opts.data.acao === '3') {
        self.buttons.push({ type: 'submit', nome: 'DELETE', cls:  'danger', text: 'Confirmar exclusão do registro' });
      }
      self.buttons.push({type: 'button', nome: 'cancel-modal', cls:  'default', text: 'Cancelar' });

      $(self.refs.modalForm).attr('action', opts.data.acaoURL);

      riot.mount(self.refs.ftlmodalbody,'ftl-include',{ 'include': { 'url': opts.data.acaoURL, 'safe': true}});

      self.update();
      $(self.refs.editModal).modal("toggle");
      return false;
    });

    self.on('mount', () => {
      if (!opts.modal) opts.modal = {isvisible: false, contextmenu: false, cls: 'modal-lg'};
      if (!opts.data) opts.data = {pk: 1, acao: '1', acaoURL: '/finan/contaContabil/', modaltitle: 'Modal Title'};

      // self.refs.ftlmodaltitle.innerHTML = opts.data.modaltitle; // Precisa, uma vez que o riot faz o update da variável opts.data.modaltitle?
      self.refs.pk = opts.data.pk;

      self.trigger('popup', { acao: opts.data.acao, acaoURL: self.opts.data.acaoURL});

      // $(self.refs.editModal).modal("toggle");
    });

    menuclick(e) {
      // self.popitupModal(self.refs.contextMenuID.value, '2')
      if (e.target.name === 'cancel-modal') {
        // Não faz nada
        e.preventDefault()
      }
      // } else if (e.target.name == 'DELETE') {
      //   // Executa request de deleção
      // } else if (e.target.name == 'save') {
      //   // Executa request de update
      // }
      // console.log(e.target.name)
      $(self.refs.editModal).modal("toggle");
      return false
    }

    self.close = () => {
      opts.modal.isvisible = false;
      self.trigger('close');
    }

  </script>

</ftl-modal>


