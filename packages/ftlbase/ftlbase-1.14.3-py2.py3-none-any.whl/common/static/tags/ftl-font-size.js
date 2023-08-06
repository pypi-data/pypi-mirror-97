riot.tag2('ftl-font-size', '<a href="#"> <i class="fa fa-text-size" aria-hidden="true" data-toggle="tooltip" title="Ajusta o tamanho da letra do site" data-placement="bottom" data-delay="{⁗show⁗:⁗500⁗, ⁗hide⁗:⁗100⁗}" onclick="{change_font}"> {size} </i> </a>', '', '', function(opts) {
    var self = this;
    self.size = 14;
    self.size_min = 10;
    self.size_max = 18;

    self.change_font = function (element) {
      if (self.size >= self.size_max) self.size = self.size_min;
      else self.size += 2;
      $("body").css("fontSize", `${self.size}px`);
    };

});
