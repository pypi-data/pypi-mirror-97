// Global settings to ajax, to send CSRFTOKEN with request
$.ajaxSetup({
  beforeSend: function (xhr, settings) {
    // if (!csrfSafeMethod(settings.type) && !this.crossDomain) { // Desabilita verificação se GET para forçar autenticação
    if (!this.crossDomain) {
      csrftoken = getCookie('csrftoken');
      xhr.setRequestHeader("HTTP_X_CSRFTOKEN", csrftoken); //csrftoken);
      xhr.setRequestHeader("X-CSRFToken", csrftoken);
      // xhr.setRequestHeader("Authorization", 'Token ' + token); // var token = '{{ token }}' ==> definido em base.html
    }
  }
});

// Clive.js: hook to jquery: https://github.com/nosir/cleave.js/issues/341
(function ($, window, undefined) {
  'use strict';
  $.fn.cleave = function (opts) {
    var defaults = {autoUnmask: false},
      options = $.extend(defaults, opts || {});

    return this.each(function () {
      var cleave = new Cleave('#' + this.id, options), $this = $(this);
      $this.data('cleave-auto-unmask', options['autoUnmask']);
      $this.data('cleave', cleave);
    });
  };
  var origGetHook, origSetHook;
  if ($.valHooks.input) {
    origGetHook = $.valHooks.input.get;
    origSetHook = $.valHooks.input.set;
  } else {
    $.valHooks.input = {};
  }
  $.valHooks.input.get = function (el) {
    var $el = $(el), cleave = $el.data('cleave');
    if (cleave) {
      return $el.data('cleave-auto-unmask') ? cleave.getRawValue() : el.value;
    } else if (origGetHook) {
      return origGetHook(el);
    } else {
      return undefined;
    }
  };
  $.valHooks.input.set = function (el, val) {
    var $el = $(el), cleave = $el.data('cleave');
    if (cleave) {
      cleave.setRawValue(val);
      return $el;
    } else if (origSetHook) {
      return origSetHook(el);
    } else {
      return undefined;
    }
  };
})(jQuery, window);

function showWorkflow(the_select, el, cls) {
  var e = document.getElementById('id_' + el);
  // var e = document.getElementById("elementId");
  var value, text, url;

  if (e.type === 'select-one') {
    value = e.options[e.selectedIndex].value;
    text = e.options[e.selectedIndex].text;
    url = '/' + value;
  }
  ftl_modal(value, '7', '/workflow/process_graph/' + value + '/', text, cls);
}

function ftl_modal(pk, acao, acaoURL, modaltitle, cls) {
  if (cls === undefined)
    cls = 'modal-lg';
  ftl_modal_mount = riot.mount('div#ftl-modal', 'ftl-modal',
    {
      'modal': {isvisible: false, contextmenu: false, cls: cls},
      'data': {pk: pk, acao: acao, acaoURL: acaoURL, modaltitle: modaltitle}
    });
}

function changeUF2(the_select, valor) {
  if (the_select.selectedIndex < 0) {
    return;
  }
  var uf = the_select.options[the_select.selectedIndex].value;
  //var name = the_select.name.substr(0, the_select.name.length-3);
  //var name = the_select.name.substr(0, the_select.name.length);
//    var name = 'main-municipio';

  var app_label = the_select.getAttribute('data-app_label');
  var object_name = the_select.getAttribute('data-object_name');

  var name = 'id_';
  var lastIndex = the_select.id.lastIndexOf("-");
  if (lastIndex >= 0) {
    name = the_select.id.substring(0, the_select.id.lastIndexOf("-") + 1);
  }
  var id = name + 'municipio';

  if (uf !== "") {
    // Acha o tab ativo, pois pode ter mais de um tab com id_municipio aberto
    var a = the_select.closest("div[class^='tab-pane active']");
    var b = $(a);
    // Acha o campo de select do município dentro do tab ativo
    // var mun_sel = b.find('select[id="id_municipio"]')
    var mun_sel = b.find('select[id="' + id + '"]');
    // var mun_sel = jQuery(id);
    mun_sel.attr('disabled', true).html('<option value="">Aguarde...</option>');
    mun_sel.load(
      //__municipios_base_url__+'ajax/'+uf+'/'+app_label+'/'+object_name+'/',
      '/cliente/municipio/ajax/' + uf + '/' + app_label + '/' + object_name + '/',
      null,
      function () {
        mun_sel[0].disabled = false;
        if (valor !== "") {
          $('#' + id).val(valor);
          //alert("Formato de CEP inválido.");
        }
        //alert("Formato de CEP inválido.");
      }
    );
  } else {
    jQuery(id).html('<option value="">--</option>');
  }
}

function changeUF(the_select) {
  changeUF2(the_select, "");
}

function changeCEP(the_select) {

  //Nova variável "cep" somente com dígitos.
  var cep = $(the_select).val().replace(/\D/g, '');

  //Verifica se campo cep possui valor informado.
  if (cep !== "") {

    //Expressão regular para validar o CEP.
    var validacep = /^[0-9]{8}$/;

    //Valida o formato do CEP.
    if (validacep.test(cep)) {
      var name = 'id_';
      var lastIndex = the_select.id.lastIndexOf("-");
      if (lastIndex >= 0) {
        name = the_select.id.substring(0, the_select.id.lastIndexOf("-") + 1);
      }
      // Acha o tab ativo, pois pode ter mais de um tab com id_municipio aberto
      var a = the_select.closest("div[class^='tab-pane active']");
      var b = $(a);
      // Acha o campo de input do endereço dentro do tab ativo
      var endereco = b.find('input[id="' + name + 'endereco"]');
      var bairro = b.find('input[id="' + name + 'bairro"]');
      var estado = b.find('select[id="' + name + 'estado"]');
      var municipio = b.find('select[id="' + name + 'municipio"]');
      //Preenche os campos com "..." enquanto consulta webservice.
      endereco.val("...");
      bairro.val("...");
      estado[0].value = "";
      municipio[0].value = "";

      //Consulta o webservice viacep.com.br/
      $.getJSON("//viacep.com.br/ws/" + cep + "/json/unicode/?callback=?", function (dados) {

        if (!("erro" in dados)) {
          //Atualiza os campos com os valores da consulta.
          endereco.val(dados.logradouro);
          bairro.val(dados.bairro);
          estado[0].value = dados.uf;
          changeUF2(estado[0], dados.ibge);
          municipio[0].value = dados.ibge;

        } else {
          //CEP pesquisado não foi encontrado.
          limpa_formulario_cep();
          alert("CEP não encontrado.");
        }
      });
    } //end if.
    else {
      //cep é inválido.
      limpa_formulario_cep();
      alert("Formato de CEP inválido.");
    }
  } //end if.
  else {
    //cep sem valor, limpa formulário.
    limpa_formulario_cep();
  }
}

function changeContaDestino(the_select, contaDestino) {
  // the_select é o campo de incidência que seleciona entre Proprietário, Locatário ou Administradora
  // var filtro = "";
  var id = "#id_" + contaDestino;

  var incidencia = the_select.options[the_select.selectedIndex].value;
  if (incidencia !== "") {
    var app_label = the_select.getAttribute('data-app_label');
    var object_name = the_select.getAttribute('data-object_name');

    var planodecontas = $('#planodecontas').val();
    var url = "/" + app_label + "/ajax" + object_name + "Select/" + planodecontas + "/" + incidencia + "/" + app_label + "/" + object_name + "/";

    var field_sel = jQuery(id);
    field_sel.attr('disabled', true).html('<option value="">Aguarde...</option>');
    field_sel.load(
      //__municipios_base_url__+'ajax/'+incidencia+'/'+app_label+'/'+object_name+'/',
      url,
      null,
      function () {
        field_sel[0].disabled = false;
        $(id).prepend('<option value="" selected>---------</option>');
        //$(id).val("");
        //if(valor !== ""){
        //    $(id).val(valor);
        //}
      }
    );
  } else {
    jQuery(id).html('<option value="">--</option>');
  }
  // if(incidencia !== ""){
  // }
}

function changeContaOrigemProvisao(the_select, origem, provisao) {
  changeContaDestino(the_select, origem);
  changeContaDestino(the_select, provisao);
}

function limpa_formulario_cep() {
  // Limpa valores do formulário de cep.
  $("#id_endereco").val("");
  $("#id_bairro").val("");
  //$("#id_municipio").val("");
  //$("#id_estado").val("");
}

function setHeight(jq_in) {
  // Set height of a element to fit content
  // Usado com summernote para autofit o conteúdo
  if (jq_in !== undefined) {
    jq_in.each(function (index, elem) {
      // https://stackoverflow.com/questions/40420782/auto-resizing-textarea-in-a-modal
      // Estava dando um problema na edição de course.Note, porque ficava aumentando o campo conforme digitava
      // O espaço disponível ainda era suficiente, então criei esse if abaixo
      // Observar que elem.style.height é string no formato DDDpx
      if (elem.scrollHeight != elem.style.height.match(/\d+/)[0]) {
        elem.style.overflow = 'hidden';
        elem.style.height = `${elem.scrollHeight + 2}px`;
      }

      // // This line will work with pure Javascript (taken from NicB's answer):
      // elem.style.height = elem.scrollHeight + 'px';
    });
  }
}

function getContentWidth(element) {
  // Retonar com a width somente do conteúdo, sem os paddings de um elemento, somente a largura útil
  // Usado em ftl-graph-sunburst para saber a área possível que pode ser mostrada
  const styles = getComputedStyle(element);

  return element.clientWidth
    - parseFloat(styles.paddingLeft)
    - parseFloat(styles.paddingRight)
}

function getContentHeight(element) {
  // Retonar com a height somente do conteúdo, sem os paddings de um elemento, somente a altura útil
  const styles = getComputedStyle(element);

  return element.clientHeight
    - parseFloat(styles.paddingTop)
    - parseFloat(styles.paddingBottom)
}


// Thanks Django - to get CSRF cookie
function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = jQuery.trim(cookies[i]);
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

var csrftoken = getCookie('csrftoken');

// Verifica se está em método que precisa autorização
// Não sendo usado pois todos os requests para DRF precisam de autorização
function csrfSafeMethod(method) {
  // these HTTP methods do not require CSRF protection
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function configuraCampos(disableMe, readonly) {
  // Busca se há formset com classe disableMe e faz o disable (inclusão de andamento)
  // if ( '{{ disableMe }}' === 'True' ) {
  var disable = $(".disableMe"); // Divs
  var disableSelect = $(".disableMe select[data-autocomplete-light-function='select2']"); // autocompletelight
  if (disableMe) {
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
    if (readonly) {
      $('input[name="save"]').hide();
    }
  } else {
    // $("fieldset.disableMe").removeProp('disabled');
    disable.removeProp('disabled');
  }

  // Se readonly então esconde todos os botões de adição de detalhe e o de post
  if (readonly) {
    $('a[id^="add-item-button"]').hide();
  }
}

// Função que será executada ao final de configuraPagina, como um callback,
// porque não sei como fazê-lo corretamente via callback/Promisse, uma vez que é chamada em vários lugares
callback_configuraPagina = null;

function configuraPagina() {
  // // Setup Django-Polymorphic for inline polymorphic formset
  $('.js-django-inlines').each(function () {
    var $this = $(this);
    var data = $this.data();

    // Local onde será feito o append das novas linhas
    // data.options.newFormTarget = ".js-django-inlines-forms";

    // A cada novo form adicionado, faz a reconfiguração da página
    data.options.onAdd = function (formset_item, options) {
      // group é o this dessa função
      // var management_form = data.djangoInline._getManagementForm();
      configuraPagina();
    };
    $this.djangoInline(data.options || data);
    // Reordena todos os itens de um formset
    data.djangoInline.setFormOrder();
  });

  // $( "#datepicker" ).datepicker( $.datepicker.regional[ "pt-BR" ] );
  $.fn.datepicker.defaults.format = 'dd/mm/yyyy';
  $.fn.datepicker.defaults.todayBtn = 'linked';
  $.fn.datepicker.defaults.language = 'pt-BR';
  $.fn.datepicker.defaults.autoclose = true;
  $.fn.datepicker.defaults.todayHighlight = true;
  $.fn.datepicker.defaults.enableOnReadonly = true;

  $("#datepicker").datepicker({
    // format: "dd/mm/yyyy",
    // todayBtn: "linked",
    // language: "pt-BR",
    // autoclose: true,
    // todayHighlight: true,
    // enableOnReadonly: false
  });
  // $('.dateinput:not([readonly])').datepicker({
  $('.dateinput').datepicker({
    format: "dd/mm/yyyy",
    todayBtn: "linked",
    language: "pt-BR",
    autoclose: true,
    todayHighlight: true,
    enableOnReadonly: false
  });

  // Remove classe has-error dos FormSetFields
  $('div .has-error').filter('.form-group').has($('div[id^="detail-items-"]')).removeClass('has-error');

  // Os campos que terão máscaras, serão configurados usando 'data-ftl' no html do element
  // Mudança de jquery.maskedinput.js para cleave.js
  $("[data-ftl='data']").cleave({date: true, datePattern: ['d', 'm', 'Y']});
  $("[data-ftl='datahora']").cleave({delimiters: ['/', '/', ' ', ':'], blocks: [2, 2, 4, 2, 2]});
  $("[data-ftl='datahorasegundo']").cleave({delimiters: ['/', '/', ' ', ':', ':'], blocks: [2, 2, 4, 2, 2, 2]});
  $("[data-ftl='telefone']").cleave({phone: true, phoneRegionCode: 'BR'});
  $("[data-ftl='celular']").cleave({phone: true, phoneRegionCode: 'BR'}); //prefix:'+55 '});
  $("[data-ftl='cpf']").cleave({blocks: [3, 3, 3, 2], delimiters: ['.', '.', '-']});
  $("[data-ftl='cnpj']").cleave({blocks: [2, 3, 3, 4, 2], delimiters: ['.', '.', '/', '-']});
  $("[data-ftl='cep']").cleave({blocks: [5, 3], delimiters: ['-']});
  $("[data-ftl='percentual']").cleave({
    numeral: true,
    numeralThousandsGroupStyle: 'thousand',
    numeralDecimalMark: ',',
    delimiter: '.',
    // prefix: '%',
    noImmediatePrefix: true,
    // tailPrefix: true,
    autoUnmask: true
  });
  $("[data-ftl='percentual-100-2']").cleave({
    numeral: true,
    numeralThousandsGroupStyle: 'thousand',
    numeralDecimalScale: 2,
    numeralDecimalMark: ',',
    delimiter: '.',
    numeralPositiveOnly: true,
    // prefix: '%',
    noImmediatePrefix: true,
    // tailPrefix: true,
    autoUnmask: true
  });
  $("[data-ftl='money']").cleave({
    // numeralIntegerScale: 15,
    numeral: true,
    // numeralThousandsGroupStyle: 'thousand',  // 'thousand' é o default
    numeralDecimalScale: 2,  // 2 é o default
    numeralDecimalMark: ',',
    delimiter: '.',
    numeralPositiveOnly: true,
    // prefix: 'R$',
    noImmediatePrefix: true,
    // tailPrefix: true,
    autoUnmask: true,
    stripLeadingZeroes: false,
    alwaysShowDecimals: true,
  });


  $('form input:not([type="hidden"]):not([type="submit"])').keydown(function (e) {
    // if (e.keyCode === 13) {
    if (e.key === 'Enter') {
      var inputs = $(this).parents("form").eq(0).find(":input");
      if (inputs[inputs.index(this) + 1] !== null) {
        inputs[inputs.index(this) + 1].focus();
      }
      e.preventDefault();
      return false;
    }
  });

  // $('form div#master-button').insert($('form div:([class="buttons-do-form"])').descendants()[0]);
  $('.tab-content .panel-body').each(function () {
    // $(this).find(".buttons-do-form").appendTo($(this).find("#master-button"));
    // Busca o master-button a partir do pai no tab, que seria o form
    $(this).find(".buttons-do-form").appendTo($(this).parent().find("#master-button"));
  });

  // Procura os campos de select com forward e força a atualização da queryset
  // $('select[data-forward-field]').not("[name*='__prefix__']").attr('data-forward-field')
  // JSON.parse($('.dal-forward-conf').not("[id*='__prefix__']").text())
  $('.dal-forward-conf').not("[id*='__prefix__']").each(function () {
    // id destination (conta bancária)
    var id = this.id.replace('dal-forward-conf-for_', '#');
    var dst = $(id);
    var prefix = dst.getFormPrefix();

    var forwardList;
    // Convert forward information into array
    try {
      forwardList = JSON.parse($(this).text());
    } catch (e) {
      return;
    }

    forwardList.forEach(function (item) {
      // Bind on source field change (beneficiario)
      $('[name=' + prefix + item.src + ']').on('change', function () {
        // Clear the autocomplete destination
        dst.val(null).trigger('change');
      });
    });
  });

  if (callback_configuraPagina != null) {
    callback_configuraPagina();
  }

  // Automount TAG, exemplo ftl-context-menu no Calendário de aluno
  $('.ftl-automount:visible').each(function (index, el) {
    // check if it has not been mounted yet
    if (!el._tag) {
      riot.mount(el);
      el.classList.remove("ftl-automount");
    }
  });

  // Remove todos os tooltip, está mantendo ativo quando clica num botão com link <a href>, como em edição e deleção
  $('[role="tooltip"]').remove();

  // Força esconder a mensagem de Processando...
  // Está havendo conflito com a deleção de caderno de aluno, ela permanece ativa.
  document.getElementById('ftl-loading').style.display = "none";
}

// rotas de acesso às URLs dos menus
var rotas = [];

function configuraFTL() {
  moment.locale('pt-br');

  // RiotJS Mixin para loading/loaded messages
  var LoadMessagesMixin = {
    // the `opts` argument is the option object received by the tag as well
    init: function (opts) {
      // this.debug=true;
      if (this.debug) console.log('LoadMessagesMixin!');

      this.on('loading', () => {
        if (this.debug) console.log('LoadMessagesMixin: loading', this.loading_timeout);
        document.getElementById('ftl-page-load').value = 'loading';
        // Vai mostrar a mensagem de carregando se houver demora na resposta
        // Valida se outro timeout não está ativo
        if (this.loading_timeout === undefined) {
          var self = this;
          this.loading_timeout = setTimeout(function () {
            // Não pode ser block, pois perde centralização horizontal e vertical. Tem que ser grid.
            document.getElementById('ftl-loading').style.display = "grid";
            if (self.debug) console.log('LoadMessagesMixin: timeout', self.loading_timeout);
          }, 500);
        }
        if (this.debug) console.log(this.loading_timeout);
      });

      this.on('loaded', (data) => {
        if (this.debug) console.log('LoadMessagesMixin: loaded', this, this.loading_timeout);
        document.getElementById('ftl-page-load').value = 'loaded';
        document.getElementById('ftl-loading').style.display = "none";
        // Limpa timeout para não ficar perdido
        clearTimeout(this.loading_timeout);
        this.loading_timeout = undefined;
      });
    },
  };
  riot.mixin('LoadMessagesMixin', LoadMessagesMixin);

  // RiotJS Mixin para tratar o Opts
  var OptsMixin = {
    // init method is a special one which can initialize
    // the mixin when it's loaded to the tag and is not
    // accessible from the tag its mixed in
    // `opts` here is the option object received by the tag as well
    init: function(opts) {
      // this.on('updated', function() {
      //   console.log('Updated!')
      // })
    },

    getOpts: function() {
      return this.opts;
    },

    setOpts: function(opts, update) {
      this.opts = opts;
      if (update) this.update();
      return this
    }
  };
  riot.mixin('OptsMixin', OptsMixin);

  configuraPagina();

  // Achando o menu corrente e ativando
  var url = window.location;
  var menu = $('li a[href="' + url.pathname + '"]');
  if (menu.length > 0) {
    menu.parent().addClass('active'); // Ativa a linha que tem o link para a URL atual
    // Ativa o menu que tem a URL contida nele
    $('ul.treeview-menu').filter(function (index) {
      return $("a[href^='" + url.pathname + "']", this).length === 1;
    }).addClass('active').css("display", "block");
  } else {
    if (document.referrer) {
      var a = document.referrer.match(/:\/\/[^\/]+([^\?]*)[\/]*(?:\?.*)?$/)[1];
      if ($('li a[href^="' + a + '"]').length > 0) {
        // Ativa a linha que tem o link para a URL atual
        $('li a[href="' + a + '"]').parent().addClass('active');
        // Ativa o menu que tem a URL contida nele
        $('ul.treeview-menu').filter(function (index) {
          return $("a[href^='" + a + "']", this).length === 1;
        }).addClass('active').css("display", "block");
      }
    }
  }

  // Monta o local das tabs das rotas onde serão mostradas as páginas carregadas
  ftltabs = riot.mount('ftl-tabs')[0];

  // Monta as rotas dos menus
  route('/..', function (name) {
    var url = window.location;
    var current_url = url.hash.slice(1);

    rotas.forEach(function (r, key) {
      if (r.rota === current_url.slice(0, r.rota.length)) {
        var small = '';

        if (url.hash.endsWith('/add/')) small = 'Inclusão';
        else if (url.hash.split("/")[4] === '2') small = 'Alteração';
        else if (url.hash.split("/")[4] === '3') small = 'Exclusão';

//          document.getElementById('h1title').innerHTML = r.nome + '<small>'+small+'</small>';

        ftltabs.trigger('updateRoute', key, r.nome, current_url, small, r.reload);
      }
    });
  });

  route.start(true);
}

// Controle elementos fixos para scroll, exemplo: toolbar do summernote na edição de conteúdo quando rola a tela
$(window).scroll(function (e) {
  var $el = $('.fixedElement:visible');
  var isPositionFixed = ($el.css('position') === 'fixed');
  if ($(this).scrollTop() > 260 && !isPositionFixed) {
    $el.css({position: 'fixed', top: '0px'});
  }
  if ($(this).scrollTop() <= 260 && isPositionFixed) {
    $el.css({position: 'static', top: '0px'});
  }
  // console.log('parent width', $el.parent().width());
  $el.css({width: $el.parent().find('.note-editing-area').width() + 'px'});
});

function formset_up(e) {
  var $e = $(e);
  var $djinline = $e.closest('.js-django-inlines').data().djangoInline;
  var index = $djinline.getFormIndex(e);
  $djinline.moveFieldUp(index);
}

function formset_down(e) {
  var $e = $(e);
  var $djinline = $e.closest('.js-django-inlines').data().djangoInline;
  var index = $djinline.getFormIndex(e);
  $djinline.moveFieldDown(index);
}

function goBack() {
  window.history.back();
}

// closeActiveTab: usado em executeUseCase para fechar o tab ativo no post de execução de use cases
function closeActiveTab() {
  try {
    $('[ref="#' + $f.closest("div[class^='tab-pane active']").attr('id') + '-close"]').click();
  } catch (e) {
    $('[ref="#' + $("div[class^='tab-pane active']").attr('id') + '-close"]').click();
  }
  // Deleta cookie next que é usado em redirect de venda de OAB no estudar
  document.cookie = 'next=; Path=/; Expires=Thu, 01 Jan 1970 00:00:01 GMT;';
}

var UUID = function () {
  var dec2hex = [];
  for (var i = 0; i <= 15; i++) {
    dec2hex[i] = i.toString(16);
  }
  var uuid = '';
  for (i = 1; i <= 36; i++) {
    if (i === 9 || i === 14 || i === 19 || i === 24) {
      uuid += '-';
    } else if (i === 15) {
      uuid += 4;
    } else if (i === 20) {
      uuid += dec2hex[(Math.random() * 4 | 0 + 8)];
    } else {
      uuid += dec2hex[(Math.random() * 16 | 0)];
    }
  }
  return uuid;
};

var Store = function () {
  riot.observable(this)
};


// // Monitora DOM e monta automaticamente riotjs tag ainda não montada (_tag não existe) e class ftl-automount
// var appFTL = document.querySelector('body');
// // all the nodes appended into the body will pass from here
// appFTL.addEventListener('DOMNodeInserted', function (e) {
//   var node = e.target;
//   // check if it's a tag node
//   if (node.nodeType === 1) { // 1 = element, 2 = attribute, 3 = text, 4 = comment
//     node.querySelectorAll('.ftl-automount').forEach(function (el) {
//       if (
//         // check if it has not been mounted yet
//         !el._tag
//         // // Para montar tags html padrão com data-is, porém não é o caso.
//         // && (
//         //   // check if it's an unknown html element
//         //   el instanceof HTMLUnknownElement ||
//         //   // or if it has the data-is attribute
//         //   el.getAttribute('data-is')
//         // )
//       ) {
//         // riot.mount(el);
//         // el.classList.remove("ftl-automount");
//       }
//
//     });
//   }
// }, false);
