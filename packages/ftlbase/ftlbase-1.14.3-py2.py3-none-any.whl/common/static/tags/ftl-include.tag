<ftl-include>
  <div>
    { responseText }
    <div ref='dados'></div>
    <div ref='prog'></div>
    <!-- <ftl-error-message></ftl-error-message> -->
  </div>

  <script>
    // Observable:
    //   ftl-include.pre-submit: antes do submit dos forms associados

    var self = this;
    self.debug = false;
    self.loading_timeout = null;

    function scriptExecute(extrajavascript) {
      if (extrajavascript !== undefined) {
        // Associa da self.refs.prog ao retorno do $('<script>') pois o div prog é perdido quando da atualização
        eval(extrajavascript);
      }
    }

    const fetch = () => {
      $.ajax({
        url: opts.include.url,
        xhrFields: {
          withCredentials: true
        },
        beforeSend: function (xhr, settings) {
          xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken')); //csrftoken);
          xhr.setRequestHeader("HTTP_X_CSRFTOKEN", getCookie('csrftoken')); //csrftoken);
          self.trigger('loading');
        },
        success: function (data) {
          self.trigger('updateContent', data);
          self.trigger('loaded', data);
          return false;
        },
        error: function (xhr, status, error) {
          if (self.debug) console.log("Something went wrong: >" + xhr + "< >" + status + '< >' + error + '<');
          if (xhr.status === 403) {
            // Forbiden - Não tem permissão
            alert('Desculpe, mas você não tem permissão!');
            window.history.back()
            // } else if ((xhr.status === 500) && (xhr.responseURL !== undefined)) {
            //   window.location = xhr.responseURL;
          } else {
            alert('Request failed.  Returned status of ' + xhr.status);
            document.open();
            document.write(xhr.responseText);
            document.close();
          }
          return false;
        }
      });
    };

    self.on('mount', () => {
      if (self.debug) console.log('ftl-include: mount:', opts.include.url);
      fetch();
    });

    self.on('loading', () => {
      if (self.debug) console.log('ftl-include: loading');

      document.getElementById('ftl-page-load').value = 'loading';

      // Vai mostrar a mensagem de carregando se houver demora na resposta
      self.loading_timeout = setTimeout(function () {
        // Não pode ser block, pois perde centralização horizontal e vertical. Tem que ser grid.
        document.getElementById('ftl-loading').style.display = "grid";
      }, 500);
    });

    self.on('loaded', (data) => {
      if (self.debug) console.log('ftl-include: loaded');

      document.getElementById('ftl-page-load').value = 'loaded';

      document.getElementById('ftl-loading').style.display = "none";
      clearTimeout(self.loading_timeout);
    });

    self.on('updateContent', (obj) => {
      // Mostra uma msg de erro na área de definida
      if (obj.msg !== undefined && obj.msg !== null) {
        if (self.debug) console.log(obj.msg);
        riot.mount('ftl-error-message', {messages: obj.msg});
      }
      // Mostra um alert
      if (obj.alert !== undefined && obj.alert !== null) {
        if (self.debug) console.log(obj.alert);
        alert(obj.alert);
      }
      // Redirect usado em finan.view.assinaturaEditDelete para redirecionar ao MP após POST da compra
      if (obj.redirect !== undefined && obj.redirect !== null) {
        scriptExecute(obj.extrajavascript);
        window.location.href = obj.redirect;
        return
      }

      // Se não houve erro ou houve erro, mas não tem goto, então atualiza com os novos dados
      if (opts.include.safe) self.refs.dados.innerHTML = obj.html;
      else self.responseText = obj.html;

      // Verifica se é pra desabilitar
      if (obj.disableMe !== undefined && obj.disableMe !== null) {
        var disable = $(self.refs.dados).find(".disableMe");
        // autocompletelight
        var disableSelect = $(self.refs.dados).find(".disableMe select[data-autocomplete-light-function='select2']");

        // Insere disable nos template de inline
        disable.removeProp('disabled');
        disable.prop('disabled', 'disabled');
        // disable.filter() => Por que estava SEM ponto e vírgula???? O que faz???
        disable.has('.has-error').removeProp('disabled');
        // Span não tem disable, então tem que usar pointer-events
        disable.filter('SPAN').css("pointer-events", "none");
        // Insere disable nos select dos autocompletelight fields
        disableSelect.removeProp('disabled');
        disableSelect.prop('disabled', 'disabled');
        // disableSelect.filter() => Por que estava SEM ponto e vírgula???? O que faz???
        disableSelect.has('.has-error').removeProp('disabled');
        // Span não tem disable, então tem que usar pointer-events
        // Insere disable nos template de inline
        // $("#detail-template").find('.disableMe').removeProp('disabled');
        // $('div[id^="detail-template"]').find('.disableMe').removeProp('disabled');
        $('div[id*=__prefix__]').find('.disableMe').removeProp('disabled');
      }

      if (obj.form_errors !== undefined || obj.formset_errors !== undefined) {
        $('input[name="save"]').show(); // Mostra campos de save se houve algum erro na validação
      }

      if (self.debug) console.log("OK: ---\>" + obj + "\<---");

      scriptExecute(obj.extrajavascript);

      // Procura por todos os <form> para inserir evento no submit,
      // porém exclui <form> de janelas modais. Ex.: edição de conta no plano contábil
      $(self.refs.dados).find('form:not([ref="modalForm"])').each(function () {
        $(this).attr('action', opts.include.url + (opts.include.url.endsWith('/') ? '' : '/'));

        $('<input>').attr({type: 'hidden', name: 'csrfmiddlewaretoken', value: getCookie('csrftoken')}).appendTo(this);

        $(this).submit(function (e) {
          // e.preventDefault()

          // Se algum javascript está monitorando o post, então avisa que será feito
          riot.store.trigger('ftl-include.pre-submit', this, e);

          // Habilita todos os campos porque o Django não reconhece os campos desabilitados, ignorando-os
          $(":disabled").removeProp('disabled');

          // var submitClickedName = $(this).data("submitClickedName")
          var submitClickedName = $(document.activeElement)[0].name;
          var submitClickedValue = $(document.activeElement)[0].value;

          if ($(document.activeElement)[0].type === 'checkbox') {
            submitClickedValue = $(document.activeElement)[0].checked;
          }

          // Especificamente o campo de Salvar é desabilitado para que o usuário não fique apertando o campo novamente
          document.activeElement.disabled = true;

          $f = $(this);
          var type = $f.attr('method');
          var dados = $f.serialize() + '&' + submitClickedName + '=' + submitClickedValue;
          var form_data = new FormData($f[0]);
          form_data.append(submitClickedName,submitClickedValue);
          var url = $f.attr('action');
          $.ajax({
            type: type,
            url: url,
            // data: dados,
            data: form_data,
            processData: false,
            contentType: false,
            dataType: 'json',
            cache: false,
            // enctype: 'multipart/form-data',
            xhrFields: {
              withCredentials: true
            },
            beforeSend: function (xhr, settings) {
              xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken')); //csrftoken);
              xhr.setRequestHeader("HTTP_X_CSRFTOKEN", getCookie('csrftoken')); //csrftoken);
              self.trigger('loading');
            },
            success: function (data) {
              self.trigger('loaded', data);
              if ((data.form_errors !== undefined && data.form_errors !== null) ||
                (data.formset_errors !== undefined && data.formset_errors !== null)) {
                self.trigger('updateContent', data); // data = req.response
                configuraPagina();
              } else if (data.goto !== undefined) {
                scriptExecute(data.extrajavascript);
                route('/' + data.goto);
              } else {
                self.trigger('updateContent', data); // data = req.response
              }
              if (self.debug) console.log("OK: ---\>" + data + "\<---");
              // self.trigger('updateContent', data); // data = req.response
              return false;
            },
            error: function (xhr, status, error) {
              if (self.debug) console.log("Something went wrong: >" + xhr + "< >" + status + '< >' + error + '<');
              document.open();
              document.write(xhr.responseText);
              document.close();
              return false;
            }
          });
          return false;
        });
      });

      self.update();
    });
  </script>
</ftl-include>

