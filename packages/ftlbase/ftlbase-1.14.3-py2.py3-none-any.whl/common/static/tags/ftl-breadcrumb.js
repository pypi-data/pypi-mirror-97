riot.tag2('ftl-breadcrumb', '<div class="ftl-breadcrumb {ftl-breadcrumb-numbered : opts.numbered}"> <a each="{link, index in opts.links}" href="{link.url}" class="{active : link.active}" onclick="{linkclicked}"> {link.text} <span if="{link.badge}" class="badge">{link.badge}</span> </a> </div>', '', '', function(opts) {
    var self = this;

    linkclicked = function (e) {
      sellink = e.item.link;
      link = {text: sellink.text, url: sellink.url};

      self.trigger("link-clicked", link);

    };

    self.on("before-mount", function () {

      if (!self.opts.links) self.opts.links = {links: []};
    });

    self.on("update", function (opts) {
      if (opts.links) self.opts.links = opts.links;
    });
});