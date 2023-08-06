riot.tag2('ftl-workflow', '<div if="{opts.modal.isvisible}" class="modal {fade: opts.modal.fade} bs-workflow-atendimento-modal" ref="ftl_workflow_modal" tabindex="-1" role="dialog" aria-labelledby="ftl-workflow-modal"> <div class="modal-dialog {cls}" role="document"> <div class="modal-content"> <div class="modal-header"> <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">×</span><span class="sr-only">Close</span></button> <h3 class="modal-title">Workflow {title}<br></h3> </div> <div class="modal-body text-center"> <div riot-style="max-width: {maxwidth}"> <object id="{svg}" class="svgClass" type="image/svg+xml" riot-style="max-width: {maxwidth}" onload="{changecolor}" data="/static/img/{opts.img}.min.svg"></object> </div> </div> <form id="form-workflow-modal"> <div class="modal-footer"> <button each="{opts.modal.buttons}" type="button" class="btn {\'btn-\' + type} btn-sm" onclick="{action}" riot-style="{style}">{text}</button> <button if="{opts.modal.dismissable}" type="button" class="btn btn-cancel btn-sm" data-dismiss="modal">Cancelar</button> </div> </form> </div> </div> </div>', 'ftl-workflow object,[data-is="ftl-workflow"] object{ max-width: { maxwidth }; }', '', function(opts) {
        var self = this

        self.maxwidth = "100%"
        self.svg = "ftl-workflow-svg"
        self.id = null
        self.color = '#87CEFA'
        self.cls = ''

        self.on('mount', () => {

            if (!opts.modal) {
                opts.modal = {

                }
            }
            if (!opts.img) opts.img = 'ftl-workflow-atendimento'
            if (opts.modal.cls) self.cls = opts.modal.cls
            self.changecolor();

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

            self.id = id
            self.color = color

            self.trigger('modal');

        })

});


