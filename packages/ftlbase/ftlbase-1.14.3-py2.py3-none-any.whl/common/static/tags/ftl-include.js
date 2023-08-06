riot.tag2('ftl-include', '<div> {responseText} <div ref="dados"></div> <div ref="prog"></div> </div>', '', '', function(opts) {


    var self = this;
    self.debug = false;
    self.loading_timeout = null;

    function scriptExecute(extrajavascript) {
      if (extrajavascript !== undefined) {

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
          xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
          xhr.setRequestHeader("HTTP_X_CSRFTOKEN", getCookie('csrftoken'));
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

            alert('Desculpe, mas você não tem permissão!');
            window.history.back()

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

      self.loading_timeout = setTimeout(function () {

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

      if (obj.msg !== undefined && obj.msg !== null) {
        if (self.debug) console.log(obj.msg);
        riot.mount('ftl-error-message', {messages: obj.msg});
      }

      if (obj.alert !== undefined && obj.alert !== null) {
        if (self.debug) console.log(obj.alert);
        alert(obj.alert);
      }

      if (obj.redirect !== undefined && obj.redirect !== null) {
        scriptExecute(obj.extrajavascript);
        window.location.href = obj.redirect;
        return
      }

      if (opts.include.safe) self.refs.dados.innerHTML = obj.html;
      else self.responseText = obj.html;

      if (obj.disableMe !== undefined && obj.disableMe !== null) {
        var disable = $(self.refs.dados).find(".disableMe");

        var disableSelect = $(self.refs.dados).find(".disableMe select[data-autocomplete-light-function='select2']");

        disable.removeProp('disabled');
        disable.prop('disabled', 'disabled');

        disable.has('.has-error').removeProp('disabled');

        disable.filter('SPAN').css("pointer-events", "none");

        disableSelect.removeProp('disabled');
        disableSelect.prop('disabled', 'disabled');

        disableSelect.has('.has-error').removeProp('disabled');

        $('div[id*=__prefix__]').find('.disableMe').removeProp('disabled');
      }

      if (obj.form_errors !== undefined || obj.formset_errors !== undefined) {
        $('input[name="save"]').show();
      }

      if (self.debug) console.log("OK: ---\>" + obj + "\<---");

      scriptExecute(obj.extrajavascript);

      $(self.refs.dados).find('form:not([ref="modalForm"])').each(function () {
        $(this).attr('action', opts.include.url + (opts.include.url.endsWith('/') ? '' : '/'));

        $('<input>').attr({type: 'hidden', name: 'csrfmiddlewaretoken', value: getCookie('csrftoken')}).appendTo(this);

        $(this).submit(function (e) {

          riot.store.trigger('ftl-include.pre-submit', this, e);

          $(":disabled").removeProp('disabled');

          var submitClickedName = $(document.activeElement)[0].name;
          var submitClickedValue = $(document.activeElement)[0].value;

          if ($(document.activeElement)[0].type === 'checkbox') {
            submitClickedValue = $(document.activeElement)[0].checked;
          }

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

            data: form_data,
            processData: false,
            contentType: false,
            dataType: 'json',
            cache: false,

            xhrFields: {
              withCredentials: true
            },
            beforeSend: function (xhr, settings) {
              xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
              xhr.setRequestHeader("HTTP_X_CSRFTOKEN", getCookie('csrftoken'));
              self.trigger('loading');
            },
            success: function (data) {
              self.trigger('loaded', data);
              if ((data.form_errors !== undefined && data.form_errors !== null) ||
                (data.formset_errors !== undefined && data.formset_errors !== null)) {
                self.trigger('updateContent', data);
                configuraPagina();
              } else if (data.goto !== undefined) {
                scriptExecute(data.extrajavascript);
                route('/' + data.goto);
              } else {
                self.trigger('updateContent', data);
              }
              if (self.debug) console.log("OK: ---\>" + data + "\<---");

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
});

