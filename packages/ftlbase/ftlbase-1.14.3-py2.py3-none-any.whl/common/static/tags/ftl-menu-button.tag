<ftl-menu-button>
  <a onclick={ click } class={ classList } tabindex="0" aria-controls={ aria } style={ style }><span><i if={ icon } class={ icon } style={ iconStyle }></i></span> { text }</a>

  <script>
  var self = this
  self.text = opts.text
  self.classList = opts.classList === undefined ? 'clearfix btn btn-sm btn-space btn-primary' : opts.classList
  self.href = opts.href
  self.aria = opts.aria
  // self.icon = '<i class="fa fa-plus-square fa-fw" style="color:#ffffff;"></i>'
  self.icon = opts.icon === undefined ? '' : opts.icon
  self.iconStyle = opts.iconStyle === undefined ? 'color:#ffffff;' : opts.iconStyle
  self.style = "padding-bottom: 5px; padding-top: 5px;color:#ffffff;"


  // console.log("text=",self.text)
  // console.log("classList=",self.classList)
  // console.log("href=",self.href)
  // console.log("aria=",self.aria)
  // console.log("icon=",self.icon)
  // console.log("iconStyle=",self.iconStyle)

  // const {type, shape, size, className, htmlType, icon, loading = false, prefixCls = 'ant-btn', onMouseUp, onClick} = opts;
  // const clickClassName = prefixCls + '-clicked';

  // root.setAttribute('type', htmlType || 'button');

  // this.iconType = loading ? 'loading' : icon;
  self.on('mount', function () {
    // self.setAttribute('style', self.style)
    if (self.root) {
      self.root.setAttribute('style', self.style)
    }
  })


  click(e) {
    // console.log('clicked')
    window.location.href = self.href;
  }

  </script>

</ftl-menu-button>
