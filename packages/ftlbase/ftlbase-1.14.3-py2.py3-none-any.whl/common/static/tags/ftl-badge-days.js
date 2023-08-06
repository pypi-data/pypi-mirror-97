riot.tag2('ftl-badge-days', '<span class="badge">{days}</span>', '', '', function(opts) {
  var self = this
  self.date = opts.date
  self.days = moment(self.date).fromNow(true)

});

