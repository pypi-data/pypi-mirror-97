// var $tree = $("#{{ idTree }}");
// var acaoURL="{{ acaoURL|safe }}";
// var detalheText="{{ detail }}";
// var updateParentText="{{ updateParent }}";

var $contextMenu = $("#contextMenu");
var $contextMenuDelete = $("#contextDelete");
var $contextMenuID = $('#contextMenuID');
var $contextMenuParent = $('#contextMenuParent');
var $modal = $('#editModal');
var $form=$modal.find('.modal-body');
var $body = $("body");

// function popitup(url, acao) {
//     newwindow=window.open(url+$contextMenuID.val()+'/'+acao+'/','Add Advance','height=400,width=900');
//     if (window.focus) {newwindow.focus()}
//     return false;
// }

function popitupModal(acaoURL, pk, acao) {
  $btnSave = $("#modal-button-save");
  $btnDELETE = $("#modal-button-delete");
  if (acao == 1 || acao == 2){
    $btnSave.show();
    $btnDELETE.hide();
  }
  else {
    $btnSave.hide();
    $btnDELETE.show();
  }
  //$modal.find('.modal-title').text('Alteração do ID ' + pk);
  $modal.find('.modal-title').text(detalheText); // tinha que ser o modaltitle
  var pk = $('#pk').val();
  var url = acaoURL+pk+'/'+acao+'/'+pk+'/';
  $("#modalForm").attr('action', url);
  $form.load(
    url,
    null,
    function(response, status, xhr){
        if (xhr.status != 200) {
            alert("Status: >" + status+ "< \nxhr.status = >"+xhr.status+"<");
        }
    }
  );
  $modal.modal("toggle");
  return false;
}

function configTree() {
  $body.click(function () {
      $(contextMenu).hide();
  });

  $("#modalForm").submit(function () {
      var pk = $('#pk').val();
      //var element = document.getElementById('leaveCode');
      //element.value = valueToSelect;
      $f = $("#modalForm");
      var dados = $f.serialize();
      $.ajax({
          type: $f.attr('method'),
          url: $f.attr('action'),
          //url: acaoURL+pk+'/4/',
          data: dados,
          success: function (data) {
              //$("#qualquer").val("OK: ---\>"+data+"\<---");
              $tree.tree('reload', function() {
                  //console.log('data is loaded');
                  var pk = $contextMenuID.val();
                  if (pk === null) {
                      pk = $contextMenuParent.val();
                  }
                  var node = $tree.tree('getNodeById', pk);
                  $tree.tree('selectNode', node);
                  $tree.tree('openNode', node, false);
                  //$tree.tree('scrollToNode', node);
                  //console.log('Scroll to node');
              });
          },
          error: function(data) {
              //$("#qualquer").val("Something went wrong: >"+data+"<");
          }
      });
      $modal.modal("toggle");
      return false;
  });


  //$('#editModal').on('show.bs.modal', function (event) {
  $modal.on('show.bs.modal', function (event) {
    var e=event;
    //var button = $(event.relatedTarget) // Button that triggered the modal
    //var recipient = button.data('whatever') // Extract info from data-* attributes
    // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
    // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
  });

  $('#contextCreate').click(function(e) {
    e.preventDefault();
    popitupModal(acaoURL, $contextMenuID.val(), '1');
  });

  $('#contextAlter').click(function(e) {
    e.preventDefault();
    popitupModal(acaoURL, $contextMenuID.val(), '2');
  });

  $('#contextDelete').click(function(e) {
    e.preventDefault();
    popitupModal(acaoURL, $contextMenuID.val(), '3');
  });

    $tree.tree({
      dragAndDrop: true,
      autoOpen: false,
      slide: false,
      onLoading: function(is_loading, node, $el) {
          //
          if (is_loading) {
              //$("#qualquer").val("Carregando dados da tree...");
              $body.addClass("loading");
          } else {
              //$("#qualquer").val("Dados carregados...");
              $body.removeClass("loading");
          }
      },
      onLoadFailed: function(response) {
          //
      }
  });

  $tree.bind(
      'tree.move',
      function(event) {
          //console.log('moved_node', event.move_info.moved_node);
          //console.log('target_node', event.move_info.target_node);
          //console.log('position', event.move_info.position);
          //console.log('previous_parent', event.move_info.previous_parent);
          var new_parent;
          if (event.move_info.position == 'inside') {
              // Movendo para um item, novo parent = target
              new_parent = event.move_info.target_node.id;
              //alert('Movendo para inside de um item, novo parent = target');
          }
          if (event.move_info.position == 'after') {
              // Movendo para um item, novo parent = target.parent, se target.parent é null então está na raiz
              new_parent = event.move_info.target_node.parent.id;
              //alert('Movendo para after de um item, novo parent = target.parent');
          }
          //var txt = event.move_info.moved_node.id + " - " + new_parent;
          //$("#teste").val(txt);
          if (new_parent != event.move_info.moved_node.parent.id) {
              // Novo parent diferente do parent original, então faz a atualização de parent
              $.post(updateParentText,
              {
                  no: event.move_info.moved_node.id,
                  pai: new_parent
              },
              function(data, status, xhr){
                  if (xhr.status != 200) {
                      alert("Status: >" + status+ "< \nxhr.status = >"+xhr.status+"<");
                  }
              });
              $tree.tree('reload', function() {
                  //console.log('data is loaded');
                  var pk = event.move_info.moved_node.id;
                  if (pk === null) {
                      pk = new_parent;
                  }
                  var node = $tree.tree('getNodeById', pk);
                  $tree.tree('selectNode', node);
                  $tree.tree('openNode', node, false);
                  //$tree.tree('scrollToNode', node);
                  //console.log('Scroll to node');
              });
          }
          //alert(event.move_info.moved_node.id);
          //alert(new_parent);
      }
  );
  $tree.bind(
    'tree.dblclick',
    function(event) {
      // event.node is the clicked node
      var node = event.node;
      $contextMenuID.val(node.id);
      popitupModal(acaoURL, node.id, '2'); // Dupli click é esição da conta
      //alert(node.name);
      //console.log(event.node);
    }
  );
  function getMenuPosition(mouse, direction, scrollDir) {
      var win = $(window)[direction](),
          scroll = $(window)[scrollDir](),
          menu = $(contextMenu)[direction](),
          position = mouse + scroll;

      // opening menu would pass the side of the page
      if (mouse + menu > win && menu < mouse) {
          position -= menu;
      }

      return position;
  }

  $tree.bind(
    'tree.contextmenu',
    function(event) {
      // The clicked node is 'event.node'
      var node = event.node;
      $tree.tree('selectNode', node);
      $contextMenuID.val(node.id);
      var nodeP = node.getPreviousNode();
      if (nodeP) {
        $contextMenuParent.val(nodeP.id);
      }
      //$contextMenuParent.val(node.parent.id);
      //pk = node.id;
      if (node.children.length > 0) {
          $contextMenuDelete.hide();
      } else {
          $contextMenuDelete.show();
      }
      $contextMenu.show()
                  .css({
                      position: "absolute",
                      left: getMenuPosition(event.click_event.clientX, 'width', 'scrollLeft'),
                      top: getMenuPosition(event.click_event.clientY, 'height', 'scrollTop')
                  })
                  .off('click')
                  .on('click', 'a', function (e) {
                      $contextMenu.hide();
                  });
    }
  );

}