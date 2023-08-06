<ftl-workflow>
    <div if="{ opts.modal.isvisible }" class="modal { fade: opts.modal.fade } bs-workflow-atendimento-modal" ref="ftl_workflow_modal" tabindex="-1" role="dialog" aria-labelledby="ftl-workflow-modal">
        <div class="modal-dialog { cls }" role="document">
            <div class="modal-content">
                <div class="modal-header">
                    <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">×</span><span class="sr-only">Close</span></button>
                    <h3 class="modal-title">Workflow { title }<br></h3>
                </div><!-- End .modal-header -->
                <div class="modal-body text-center">

<!--object type="image/svg+xml" data="/static/img/{ opts.img }.svg" style="width: 870px"> Seu navegador não suporta SVG </object-->
<!--div style="max-width: 870px"-->
<div style="max-width: { maxwidth }">
    <object id="{ svg }" class="svgClass" type="image/svg+xml" style="max-width: { maxwidth }" onload={ changecolor } data="/static/img/{ opts.img }.min.svg"></object>
</div>

                </div><!-- End .modal-body -->
                <form id="form-workflow-modal">
                    <div class="modal-footer">
                        <button each="{ opts.modal.buttons }" type="button" class="btn { 'btn-' + type } btn-sm" onclick="{ action }" style="{ style }">{ text }</button>
                        <button  if="{ opts.modal.dismissable }" type="button" class="btn btn-cancel btn-sm" data-dismiss="modal">Cancelar</button>
                    </div><!-- End .modal-footer -->
                </form>
            </div><!-- End .modal-content -->
        </div><!-- End .modal-dialog -->
    </div>
    <style>
        object {
            max-width: { maxwidth };
        /*    overflow:hidden;
            background:yellow;
            padding:10px;
            display:block;
        */}
    </style>
    <script>
        var self = this
        // self.maxwidth = "870px"
        self.maxwidth = "100%"
        self.svg = "ftl-workflow-svg"
        self.id = null
        self.color = '#87CEFA'
        self.cls = ''

        self.on('mount', () => {
            // console.log(opts.modal)
            if (!opts.modal) {
                opts.modal = {
                    // isvisible: true,
                    // dismissable: true,
                    // fade: true,
                    // heading: 'Modal heading',
                    // cls: 'modal-lg',
                    // buttons: [{
                    //   text: 'Ok',
                    //   type: 'primary',
                    //   action: function () { ... }
                    // }, {
                    //   text: 'Cancel',
                    //   action: function () { ... }
                    // }]
                    // heading: 'Workflow de Atendimento',
                    // buttons: [{
                    //   text: 'Ok',
                    //   type: 'primary',
                    //   action: function () {
                    //     self.trigger('close')
                    //   }
                    // }]
                }
            }
            if (!opts.img) opts.img = 'ftl-workflow-atendimento'
            if (opts.modal.cls) self.cls = opts.modal.cls
            self.changecolor();

            // console.log(opts.modal)
        })

        self.close = () => {
            if (opts.modal.dismissable) {
                opts.modal.isvisible = false
                this.trigger('close')
            }
        }

        self.on('modal', () => {
            $(self.refs.ftl_workflow_modal).modal();
        })

        self.changecolor = () => {
            if (self.id && self.color) {
                document.getElementById(self.svg).contentDocument.getElementById(self.id).style.fill=self.color;
            }
            self.update()
        }

        self.on('mark-id', (id, color) => {
            // document.getElementById(self.svg).getSVGDocument().getElementById(id).style.fill=color;
            self.id = id
            self.color = color
            // console.log('svg:',self.svg,', id:', id, ',color:',color);
            // $(self.refs.ftl_workflow_modal).modal();
            self.trigger('modal');
            // self.changecolor();
            // document.getElementById(self.svg).contentDocument.getElementById(id).style.fill=color;
            // $(ftl_modal[0].refs.ftl_workflow_modal).modal()
        })

    </script>
</ftl-workflow>


