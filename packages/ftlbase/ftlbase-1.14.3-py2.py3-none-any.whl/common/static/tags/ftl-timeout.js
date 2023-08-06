riot.tag2('ftl-timeout', '<span></span>', '', '', function(opts) {
    var self = this;
    self.delay = undefined;
    self.inc = undefined;
    self.url = undefined;
    self.responseText = undefined;

    self.on('mount', () => {
      self.url = opts.url;
      self.delay = opts.delay !== undefined ? opts.delay : 5 * 60 * 1000;
      self.cors = opts.cors === undefined ? true : opts.cors;
      self.trigger('updateContent');
    });

    self.on('updateContent', () => {

      const req = new XMLHttpRequest();
      req.responseType = 'json';
      req.onload = resp => {
        if (req.status !== 200) {

        } else {
          this.root.innerHTML = req.response.html;
          self.update();
        }
        if (self.delay > 0) {
          setTimeout(function () {
            self.trigger('updateContent')
          }, self.delay);
        }
      };

      req.open('get', self.url, true);
      req.setRequestHeader("X-Requested-With", "XMLHttpRequest");
      if (self.cors) {
        try {
          req.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
          req.setRequestHeader("HTTP_X_CSRFTOKEN", getCookie('csrftoken'));
        } catch (e) {
        }
      }
      req.send();
    });

});
