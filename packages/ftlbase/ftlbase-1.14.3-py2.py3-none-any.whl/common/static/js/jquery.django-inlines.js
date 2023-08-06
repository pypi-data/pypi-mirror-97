/**
 * jQuery plugin for Django inlines
 *
 * - When a `.js-django-inlines` is present, it will automatically enable this script for it.
 * - When `.js-django-inlines-add-form` is missing, an add button will be inserted manually.
 * - Make sure a `.js-django-inlines-remove-form` element is present in the HTML.
 *
 * To customize the behavior, use different class names and manually call $formset.djangoInline().
 * This can also be used to manually connect the 'add' and 'delete' buttons.
 *
 * Source: https://gist.github.com/vdboor/5020164
 *
 * (c) 2011-2016 Diederik van der Boor, Apache 2 Licensed.
 *
 * (c) 2017 Washington Lucena
 * Alterações para que o se possa trabalhar com as novas versões do Django e suporte a ftlbase
 *
 */

(function ($) {

  /**
   * The internal object that manages the inline.
   * This object is constructed in the jQuery plugin binding, and stored as 'data' attribute.
   *
   * @param group The container DOM element.
   * @param options The `data-..` fields given by the jQuery plugin.
   * @constructor
   */
  function DjangoInline(group, options) {
    options = $.extend({}, $.fn.djangoInline.defaults, options);

    this.group = group;
    this.$group = $(group);
    this.options = options;

    options.prefix = options.prefix || this.$group.attr('id').replace(/-group$/, '');

    if (options.formTemplate) {
      this.$form_template = $(options.formTemplate);
    } else {
      // this.$form_template = this.$group.find(this.options.emptyFormSelector);  // the extra item to construct new instances.
      // Empty forms devem estar numa div de classe js-django-inlines-forms child do group
      this.$form_template = this.$group.children('.js-django-inlines-forms').children(this.options.emptyFormSelector);

      // Preserva todos os campos hidden required, pois há erro quando um campo hidden é required no browser
      var hiddenFields = $('input,textarea,select').filter('[required]:hidden');
      // Retira o required dos hidden
      hiddenFields.prop('required', false);
      // Insere class required para marcar os campos requeridos.
      // Será usado no addForm para remarcar required nos novos campos.
      hiddenFields.addClass('required');
    }


    // Create the add button if requested (null/undefined means auto select)
    if (options.showAddButton !== false) {
      // $addButton devem estar numa div de classe js-django-inlines-add child do group
      this.$addButton = this.$group.find('.js-django-inlines-add-form-' + options.prefix);
      if (!this.$addButton.length) {
        this.$addButton = this.createAddButton();
      } else {
        this.$addButton.filter('a, button').click($.proxy(this._onAddButtonClick, this));
        this.$addButton.find('a, button').click($.proxy(this._onAddButtonClick, this));
      }

      // Hide the add button when there are too many forms (NOTE: partially implemented)
      this._toggleAddButtonDisplay();
    }

    // Auto-bind the delete button.
    var myself = this;
    this.$group.on('click', '.js-django-inlines-remove-form', function (event) {
      event.preventDefault();
      myself.removeForm(this);
    });
  }

  DjangoInline.prototype = {

    /**
     * Create the add button (if needed)
     */
    createAddButton: function () {
      var $addButton;
      var myself = this;
      if (this.options.childTypes) {
        // Polymorphic inlines - the add button opens a menu.
        $addButton = $(this._renderPolymorphicAddButton());
        this.$group.after($addButton);

        $addButton.children('a').click($.proxy(this._onMenuToggle, this));
        $addButton.find('li a').click($.proxy(this._onAddButtonClick, this));
      } else {
        // Normal inlines
        $addButton = $(this._renderAddButton());
        this.$group.after($addButton);

        $addButton.find('a').click($.proxy(this._onAddButtonClick, this));
      }

      return $addButton;
    },

    _renderAddButton: function () {
      return ''
      // Marretada para evitar mostrar o botão de add
      // return '<div class="' + this.options.addCssClass + '"><a href="#">' + this.options.addText + "</a></div>";
    },

    _renderPolymorphicAddButton: function () {
      var menu = '<div class="add-form-choice-menu" style="display: none;"><ul>';
      for (var i = 0; i < this.options.childTypes.length; i++) {
        var obj = this.options.childTypes[i];
        menu += '<li><a href="#" data-type="' + obj.type + '">' + obj.name + '</a></li>';
      }

      menu += '</ul></div>';
      return '<div class="' + this.options.addCssClass + ' add-form-choice"><a href="#">' + this.options.addText + "</a>" + menu + "</div>";
    },

    _onMenuToggle: function (event) {
      event.preventDefault();
      event.stopPropagation();
      var $menu = $(event.target).next('.add-form-choice-menu');

      if (!$menu.is(':visible')) {
        function hideMenu() {
          $menu.slideUp();
          $(document).unbind('click', hideMenu);
        }

        $(document).click(hideMenu);
      }

      $menu.slideToggle();
    },

    _onAddButtonClick: function (event) {
      event.preventDefault();
      var type = $(event.target).attr('data-type');
      var empty_form_selector = !type ? null : this.options.emptyFormSelector + "[data-inline-type=" + type + "]";
      this.addForm(empty_form_selector);
    },

    _toggleAddButtonDisplay: function () {
      // Hide the add button when there are no more forms available.
      var management_form = this._getManagementForm();
      var hideAddButton = (management_form.max_forms
        && management_form.max_forms.value
        && parseInt(management_form.total_forms.value) >= parseInt(management_form.max_forms.value));
      this.$addButton.toggle(!hideAddButton);
    },

    _setFieldOrder: function (id_prefix, item, val) {
      // Ordenação de formset, default field name = order
      item.find("[id^='" + id_prefix + "'][id$='" + this.options.orderFieldName + "']:not([id^='detail-items-'])")
        .val(val * 10);
      // item.find("[id^='" + id_prefix + "'][id$='" + this.options.orderFieldName + "']:not([id^='detail-items-'])").each(function () {
      //   this.value = val * 10;
      // });
    },

    setFieldOrder: function (id) {
      // Ordenação de formset, default field name = order
      var id_prefix = this.getFieldIdPrefix(id);
      var item = this.getFormAt(id);
      this._setFieldOrder(id_prefix, item, item.index() + 1);
      // item.find("[id^='" + id_prefix + "'][id$='" + this.options.orderFieldName + "']:not([id^='detail-items-'])").each(function () {
      //   this.value = (id + 1) * 10;
      // });
    },

    // Reordena todos os formsets
    setFormOrder: function () {
      var management_form = this._getManagementForm();
      var total_count = parseInt(management_form.total_forms.value);
      for (var i = 0; i < total_count; i++) {
        this.setFieldOrder(i);
      }
    },

    // Move Up one element without any jquery
    moveUp: function (element) {
      var prev = element.previousElementSibling;
      if (!prev) return prev;
      // Se é um elemento emptyForm, então pula, pega o anterior (despreza o ponto no início do seletor)
      if (prev.classList.contains(this.options.emptyFormSelector.substring(1))) {
        prev = prev.previousElementSibling;
      }
      if (prev)
        element.parentNode.insertBefore(element, prev);
      return prev;
    },

    // Move Down one element without any jquery
    moveDown: function (element) {
      var next = element.nextElementSibling;
      if (!next) return next;
      // Se é um elemento emptyForm, então pula, pega o próximo (despreza o ponto no início do seletor)
      if (next.classList.contains(this.options.emptyFormSelector.substring(1))) {
        next = next.nextElementSibling;
      }
      if (next)
        element.parentNode.insertBefore(next, element);
      return next;
    },

    moveFieldUp: function (from) {
      // Move um formset de uma posição pra cima

      var $current = this.getFormAt(from);
      // Se length é zero, então não existe from, não faz nada e retorna
      if ($current.length === 0) return;

      var $other = $(this.moveUp($current[0]));
      // Se length é zero, então é a última linha, não tem pra onde descer mais e não faz nada
      if ($other.length === 0) return;

      // var to = from - 1;
      var to = this.getFormIndex($other);

      // this._renumberItem($current, to);
      // this._renumberItem($other, from);

      // Ajusta a ordem dos campos
      this.setFieldOrder(from);
      this.setFieldOrder(to);

      // Se $current.index() === 0, então os títulos da linha from tem q ser mostrado,
      // enquanto o da linha zero tem q ser escondidos
      if ($current.index() === 0) {
        $current.find('div.row > div > label.sr-only').removeClass('sr-only').addClass('control-label');
        $other.find('div.row > div > label').addClass('sr-only').removeClass('control-label');
      }
    },

    moveFieldDown: function (from) {
      // Move um formset de uma posição pra baixo
      var $current = this.getFormAt(from);
      // Se length é zero, então não existe from, não faz nada e retorna
      if ($current.length === 0) return;

      var $other = $(this.moveDown($current[0]));
      // Se length é zero, então é a última linha, não tem pra onde descer mais e não faz nada
      if ($other.length === 0) return;

      // var to = from + 1;
      var to = this.getFormIndex($other);

      // this._renumberItem($current, to);
      // this._renumberItem($other, from);

      // Ajusta a ordem dos campos
      this.setFieldOrder(from);
      this.setFieldOrder(to);

      // Se $current.index() === 0, então os títulos da linha from tem q ser mostrado, enquanto o da linha zero tem q ser escondidos
      if ($other.index() === 0) {
        // Nova linha zero === $other -> Mostra título das linhas
        $other.find('div.row > div > label.sr-only').removeClass('sr-only').addClass('control-label');
        $current.find('div.row > div > label').addClass('sr-only').removeClass('control-label');
      }
    },

    /**
     * The main action, add a new row.
     * Allow to select a different form template (for polymorphic inlines)
     */
    addForm: function (emptyFormSelector) {
      var $form_template;

      if (emptyFormSelector) {
        // Se o template já foi preenchido na construção de DjangoInline
        if (this.$form_template && this.$form_template.length > 0) {
          $form_template = this.$form_template.filter(emptyFormSelector)
        } else {
          $form_template = this.$group.find(emptyFormSelector);
        }
        if ($form_template.length === 0) {
          throw new Error("Form template '" + emptyFormSelector + "' not found");
        }
      } else {
        if (!this.$form_template || this.$form_template.length === 0) {
          throw new Error("No empty form available. Define the 'form_template' setting or add an '.empty-form' element in the '" + this.options.prefix + "' formset group!");
        }

        $form_template = this.$form_template;
      }
      // Remove from template all span elements from autocomplete-light (class select2)
      $form_template.find('.select2').remove();
      // $form_template.parent().remove('.select2');

      // The Django admin/media/js/inlines.js API is not public, or easy to use.
      // Recoded the inline model dynamics.
      var management_form = this._getManagementForm();
      if (!management_form.total_forms) {
        throw new Error("Missing '#" + this._getGroupFieldIdPrefix() + "-TOTAL_FORMS' field. Make sure the management form included!");
      }

      // When a inline is presented in a complex table,
      // the newFormTarget can be very useful to direct the output.
      var container;
      if (this.options.newFormTarget == null) {
        container = $form_template.parent();
      } else if ($.isFunction(this.options.newFormTarget)) {
        container = this.options.newFormTarget.apply(this.group);
      } else {
        container = this.$group.find(this.options.newFormTarget);
      }

      if (container === null || container.length === 0) {
        throw new Error("No container found via custom 'newFormTarget' function!");
      }

      // Clone the item.
      var new_index = parseInt(management_form.total_forms.value);
      var item_id = this._getFormId(new_index);
      // var newhtml = _getOuterHtml($form_template).replace(/__prefix__/g, new_index);
      // var newitem = $(newhtml).removeClass("empty-form").attr("id", item_id);
      var newitem = $form_template.clone();
      newitem.find('[id*="__prefix__"],[name*="__prefix__"],[for*="__prefix__"],[class*="__prefix__"]').each(function () {
        function updatePrefix(elm, atr) {
          var val = elm.attr(atr);
          // Só o primeiro prefix, pois em caso de nested, o segundo não muda (dropdown autocomplete inside form)
          if ((val !== undefined) && val.includes('__prefix__')) {
            val = val.replace(/__prefix__/, new_index);
            // $this.attr(atr, val);
            elm.attr(atr, val);
          }
        }

        var $this = $(this);
        updatePrefix($this, 'id');
        updatePrefix($this, 'name');
        updatePrefix($this, 'for');

        // console.log('Tipo:', $this[0].tagName);

        if (($this[0].tagName === 'DIV') && this.classList.contains('js-django-inlines')) {
          // data-option de div contém configuração do DjangoInline e possui __prefix__ em dropdown interno
          // Então tem q alterar
          updatePrefix($this, 'data-options');
        }
        if (($this[0].tagName === 'A') && this.className.match(/__prefix__/)) {
          // O botão de adição de dropdown interno é <a> e tem classe js-django-inlines-add-form- com __prefix__
          // Então tem q alterar
          updatePrefix($this, 'class');
        }
      });
      newitem = newitem.removeClass("empty-form").attr("id", item_id);
      newitem.find('.empty-form:not([id*="__prefix__"])').removeClass('empty-form'); // Remove class empty-form do formset no caso de formset dentro de formset

      // Troca classe ftl-inlines-first-only para sr-only de forma a que o campo não apareça na tela
      if (new_index > 0) {
        // compiledTmpl = compiledTmpl.replace(/ftl-inlines-first-only/g, 'sr-only');

        // $('div:not([id^="detail-items-"])', newitem).filter('div:not([id^="detail-template-"])').find('.ftl-inlines-first-only').each(function(index, el){
        $('div:not([id^="detail-items-"])', newitem).filter('div:not([id^="detail-template-"])').find('.ftl-inlines-first-only').each(function (index, el) {
          $(el).removeClass("ftl-inlines-first-only").addClass('sr-only');
          // console.log(index, el.id, el.name);
        });
      }

      if (new_index > 0) {
        newitem.find('div.row > div > label').addClass('sr-only').removeClass('control-label');
      }

      // Se existe field de com classe ftl-seq, então preenche com o valor do último seq + 1
      // Serve para controlar item de detail de model master/detail
      var maximum = null;
      $('.ftl-seq:not([id*="__prefix__"])').each(function() {
        console.log($(this));
        // var value = parseInt($(this).value);
        var value = parseInt(this.value);
        maximum = (value > maximum) ? value : maximum;
      });
      newitem.find('.ftl-seq:not([id*="__prefix__"])').each(function (index, el) {
          el.value = ++maximum;
          // console.log(index, el.id, el.name);
        });

      // Add it
      container.append(newitem);
      var formset_item = $("#" + item_id);
      if (formset_item.length === 0) {
        throw new Error("New FormSet item not found: #" + item_id);
      }

      formset_item.data('djangoInlineIndex', new_index);

      // Remarca como requerido os campos com class required
      newitem.find('.required').prop('required', true).removeClass('required');

      if (this.options.onAdd) {
        this.options.onAdd.call(this.group, formset_item, new_index, this.options);
      }

      // Ordenação de formset, default field name = order
      this.setFieldOrder(new_index);

      // Update administration
      management_form.total_forms.value = new_index + 1;
      return formset_item;
    },

    getFormAt: function (index) {
      return $('#' + this._getFormId(index));
    },

    _getFormId: function (index) {
      // The form container is expected by the numbered as #prefix-NR
      return this.options.itemIdTemplate.replace('{prefix}', this.options.prefix).replace('{index}', index);
    },

    _getGroupFieldIdPrefix: function () {
      // typically:  #id_modelname
      return this.options.autoId.replace('{prefix}', this.options.prefix);
    },

    /**
     * Get the management form data.
     */
    _getManagementForm: function () {
      var group_id_prefix = this._getGroupFieldIdPrefix();
      return {
        // management form item
        total_forms: $("#" + group_id_prefix + "-TOTAL_FORMS")[0],
        initial_forms: $("#" + group_id_prefix + "-INITIAL_NUM_FORMS")[0],
        min_forms: $("#" + group_id_prefix + "-MIN_NUM_FORMS")[0],
        max_forms: $("#" + group_id_prefix + "-MAX_NUM_FORMS")[0],
        group_id_prefix: group_id_prefix
      }
    },

    _getItemData: function (child_node) {
      var formset_item = $(child_node).closest(this.options.itemsSelector);
      if (formset_item.length === 0) {
        return null;
      }

      // Split the ID, using the id_template pattern.
      // note that ^...$ is important, as a '-' char can occur multiple times with generic inlines (inlinetype-id / app-model-ctfield-ctfkfield-id)
      var id = formset_item.attr("id");
      var cap = (new RegExp('^' + this.options.itemIdTemplate.replace('{prefix}', '(.+?)').replace('{index}', '(\\d+)') + '$')).exec(id);

      return {
        formset_item: formset_item,
        prefix: cap[1],
        index: parseInt(cap[2], 0)   // or parseInt(formset_item.data('djangoInlineIndex'))
      };
    },

    /**
     * Get the meta-data of a single form.
     */
    _getItemForm: function (child_node) {
      var dominfo = this._getItemData(child_node);
      if (dominfo === null) {
        return null;
      }

      var field_id_prefix = this._getGroupFieldIdPrefix() + "-" + dominfo.index;
      return $.extend({}, dominfo, {
        // Export settings data
        field_id_prefix: field_id_prefix,
        field_name_prefix: dominfo.prefix + '-' + dominfo.index,

        // Item fields
        pk_field: $('#' + field_id_prefix + '-' + this.options.pkFieldName),
        delete_checkbox: $("#" + field_id_prefix + "-DELETE")
      });
    },

    /**
     * Remove a row
     */
    removeForm: function (child_node) {
      // Get dom info
      var management_form = this._getManagementForm();
      var itemform = this._getItemForm(child_node);
      if (itemform === null) {
        throw new Error("No form found for the selector '" + child_node.selector + "'!");
      }

      var total_count = parseInt(management_form.total_forms.value);
      var has_pk_field = itemform.pk_field.length !== 0;

      if (this.options.onBeforeRemove) {
        this.options.onBeforeRemove.call(this.group, itemform.formset_item, this.options);
      }

      // In case there is a delete checkbox, save it.
      if (has_pk_field && itemform.pk_field[0].value) {
        // Item was an existing form, need to update the delete checkbox.
        if (itemform.delete_checkbox.length) {
          // itemform.pk_field.insertAfter(management_form.total_forms);
          // itemform.delete_checkbox.attr('checked', true).insertAfter(management_form.total_forms).hide();
          // Alterado para que apenas o checkbox seja marcado e não haja deleção do mesmo
          itemform.delete_checkbox.attr('checked', true);
        } else {
          // Construct a delete checkbox on the fly.
          // itemform.pk_field.insertAfter(management_form.total_forms);
          // var dummyDelete = '<input type="hidden" id="' + itemform.field_id_prefix + '-DELETE" name="' + itemform.field_name_prefix + '-DELETE" value="on">';
          // $(dummyDelete).insertAfter(management_form.total_forms);
          // Alterado para que apenas o checkbox seja marcado e não haja deleção do mesmo
          var dummyDelete = '<label class="" for="\' + itemform.field_id_prefix + \'-DELETE"><input type="checkbox" id="' + itemform.field_id_prefix + '-DELETE" name="' + itemform.field_name_prefix + '-DELETE" value="on" class="checkboxinput">Apagar</label>';
          $(dummyDelete).appendTo(itemform.formset_item);
        }

        // Incluído aqui porque não remove mais após if, faz só hide
        itemform.formset_item.hide();
      } else {
        // Newly added item, renumber in reverse order
        for (var i = itemform.index + 1; i < total_count; i++) {
          this._renumberItem(this.getFormAt(i), i - 1);
        }

        management_form.total_forms.value--;

        // Remove form se empty (newly), inserido aqui porque não remove mais após if, faz só hide
        itemform.formset_item.remove();
      }


      // And remove item
      // itemform.formset_item.remove();

      if (this.options.onRemove) {
        this.options.onRemove.call(this.group, itemform.formset_item, this.options);
      }

      return itemform.formset_item;
    },

    // Based on django/contrib/admin/media/js/inlines.js
    _renumberItem: function ($formset_item, new_index) {
      var id_regex = new RegExp("(" + this._getFormId('([-]?\\d+|__prefix__)') + ")");
      var id_regex_order = new RegExp("^(" + this.options.autoId.replace('{prefix}', this._getFormId('([-]?\\d+|__prefix__)-order')) + ")");
      var replacement = this._getFormId(new_index);
      $formset_item.data('djangoInlineIndex', new_index);

      // Loop through the nodes.
      // Getting them all at once turns out to be more efficient, then looping per level.
      var nodes = $formset_item.add($formset_item.find("*"));
      for (var i = 0; i < nodes.length; i++) {
        var node = nodes[i];
        var $node = $(node);

        var for_attr = $node.attr('for');
        if (for_attr && for_attr.match(id_regex)) {
          $node.attr("for", for_attr.replace(id_regex, replacement));
        }

        if (node.id && node.id.match(id_regex)) {
          node.id = node.id.replace(id_regex, replacement);
        }

        if (node.name && node.name.match(id_regex)) {
          node.name = node.name.replace(id_regex, replacement);
        }
      }
    },

    // Extra query methods for external callers:

    getFormIndex: function (child_node) {
      var dominfo = this._getItemData(child_node);
      return dominfo ? dominfo.index : null;
    },

    getForms: function () {
      // typically:  .inline-related:not(.empty-form)
      return this.$group
        .children('.js-django-inlines-forms')
        .children(this.options.itemsSelector + ":not(" + this.options.emptyFormSelector + ")");
    },

    getEmptyForm: function () {
      // typically:  #modelname-group > .empty-form
      return this.$form_template;
    },

    getFieldIdPrefix: function (item_index) {
      if (!$.isNumeric(item_index)) {
        var dominfo = this._getItemData(item_index);
        if (dominfo === null) {
          throw new Error("Unexpected element in getFieldIdPrefix, needs to be item_index, or DOM child node.");
        }
        item_index = dominfo.index;
      }

      // typically:  #id_modelname-NN
      return this._getGroupFieldIdPrefix() + "-" + item_index;
    },

    getFieldsAt: function (index) {
      var $form = this.getFormAt(index);
      return this.getFields($form);
    },

    getFields: function (child_node) {
      // Return all fields in a simple lookup object, with the prefix stripped.
      var dominfo = this._getItemData(child_node);
      if (dominfo === null) {
        return null;
      }

      var fields = {};
      var $inputs = dominfo.formset_item.find(':input');
      var name_prefix = this.options.prefix + "-" + dominfo.index;

      for (var i = 0; i < $inputs.length; i++) {
        var name = $inputs[i].name;
        if (name.substring(0, name_prefix.length) === name_prefix) {
          var suffix = name.substring(name_prefix.length + 1);  // prefix-<name>
          fields[suffix] = $inputs[i];
        }
      }

      return fields;
    },

    removeFormAt: function (index) {
      return this.removeForm(this.getFormAt(index));
    }
  };


  function _getOuterHtml($node) {
    if ($node.length) {
      if ($node[0].outerHTML) {
        return $node[0].outerHTML;
      } else {
        return $("<div>").append($node.clone()).html();
      }
    }
    return null;
  }


  // jQuery plugin definition
  // Separated from the main code, as demonstrated by Twitter bootstrap.
  $.fn.djangoInline = function (option) {
    var args = Array.prototype.splice.call(arguments, 1);
    var call_method = (typeof option === 'string');
    var plugin_result = (call_method ? undefined : this);

    this.filter('.inline-group').each(function () {
      var $this = $(this);
      var data = $this.data('djangoInline');

      if (!data) {
        var options = typeof option === 'object' ? option : {};
        $this.data('djangoInline', (data = new DjangoInline(this, options)));
      }

      if (typeof option === 'string') {
        plugin_result = data[option].apply(data, args);
      }
    });

    return plugin_result;
  };

  $.fn.djangoInline.defaults = {
    pkFieldName: 'id',       // can be `tablename_ptr` for inherited models.
    autoId: 'id_{prefix}',   // the auto id format used in Django.
    prefix: null,            // typically the model name in lower case.
    newFormTarget: null,     // Define where the row should be added; a CSS selector or function.

    itemIdTemplate: '{prefix}-{index}',  // Format of the ID attribute.
    itemsSelector: '.inline-related',   // CSS class that each item has
    emptyFormSelector: '.empty-form',    // CSS class that for jquery selector

    formTemplate: null,  // Complete HTML of the new form
    childTypes: null,    // Extra for django-polymorphic, allow a choice between empty-forms.

    showAddButton: true,
    addText: "add another",      // Text for the add link
    addCssClass: "add-row",      // CSS class applied to the add link

    orderFieldName: 'order',     // Field name for order formset in drag and drop/move
  };

  // Also expose inner object
  $.fn.djangoInline.Constructor = DjangoInline;


  // Auto enable inlines
  $.fn.ready(function () {
    $('.js-django-inlines').each(function () {
      var $this = $(this);
      var data = $this.data();
      $this.djangoInline(data.options || data);
    });
  })
})(window.django ? window.django.jQuery : jQuery);
