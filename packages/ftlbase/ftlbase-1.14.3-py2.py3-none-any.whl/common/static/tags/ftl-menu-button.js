riot.tag2('ftl-menu-button', '<a onclick="{click}" class="{classList}" tabindex="0" aria-controls="{aria}" riot-style="{style}"><span><i if="{icon}" class="{icon}" riot-style="{iconStyle}"></i></span> {text}</a>', '', '', function(opts) {
  var self = this
  self.text = opts.text
  self.classList = opts.classList === undefined ? 'clearfix btn btn-sm btn-space btn-primary' : opts.classList
  self.href = opts.href
  self.aria = opts.aria

  self.icon = opts.icon === undefined ? '' : opts.icon
  self.iconStyle = opts.iconStyle === undefined ? 'color:#ffffff;' : opts.iconStyle
  self.style = "padding-bottom: 5px; padding-top: 5px;color:#ffffff;"

  self.on('mount', function () {

    if (self.root) {
      self.root.setAttribute('style', self.style)
    }
  })

  this.click = function(e) {

    window.location.href = self.href;
  }.bind(this)

});
