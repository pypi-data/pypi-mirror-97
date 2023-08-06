<ftl-badge-days>
  <span class="badge">{ days }</span>

  <script>
  var self = this
  self.date = opts.date
  self.days = moment(self.date).fromNow(true)

  // console.log("iconStyle=",self.iconStyle)

  // this.iconType = loading ? 'loading' : icon;
  // self.on('mount', function () {
  //   // self.setAttribute('style', self.style)
  //   if (self.root) {
  //     self.root.setAttribute('style', self.style)
  //   }
  // })

  </script>
</ftl-badge-days>

