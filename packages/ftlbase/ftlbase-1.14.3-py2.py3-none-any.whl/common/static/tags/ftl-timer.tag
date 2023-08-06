<ftl-timer>
  <a href="#">
    <i class="fa fa-user-clock" aria-hidden="true" data-toggle="tooltip" title="Cronômetro para auxiliar no controle de tempo de estudo" data-placement="bottom" data-delay='{"show":"500", "hide":"100"}'></i>
    { time }
    <i hide={timer.started} class="fa fa-play-circle " aria-hidden="true" data-toggle="tooltip" title="Iniciar cronômetro" data-placement="bottom" data-delay='{"show":"500", "hide":"100"}' onclick="{ click_start }"></i>
    <i show={timer.started} class="fa fa-pause-circle" aria-hidden="true" data-toggle="tooltip" title="Parar cronômetro" data-placement="bottom" data-delay='{"show":"500", "hide":"100"}' onclick="{ click_stop }"></i>
    <i class="fa fa-undo" aria-hidden="true" data-toggle="tooltip" title="Resetar cronômetro" data-placement="bottom" data-delay='{"show":"500", "hide":"100"}' onclick="{ click_reset }"></i>
  </a>

  <script>
    var self = this;
    self.delay = 1000; // a cada segundo
    self.timer = {started: false, duration: 0};
    self.time = '00:00:00';
    self.url_load = undefined; // URL de leitura do status atual do timer do usuário
    self.url_stop = undefined;
    self.responseText = undefined;

    self.show_date = function(){
      var date = new Date(0);
      date.setSeconds(self.timer.duration); // specify value for SECONDS here
      self.time = date.toISOString().substr(11, 8);
      self.update();
    };

    self.on('mount', () => {
      self.url_load = opts.url_load;
      self.url_stop = self.url_load + 'stop/';
      self.trigger('updateContent')
    });

    self.tick = (function () {
      if (self.timer.started) {
        ++self.timer.duration;
      }
      self.show_date();

    }).bind(self);

    var timer_tick = setInterval(self.tick, 1000);

    self.on('unmount', function () {
      console.info('timer_tick cleared');
      clearInterval(timer_tick);
    });

    // Busca pela url_laod o valor atual do timer associado ao usuário
    self.on('updateContent', () => {
      const req = new XMLHttpRequest();
      req.responseType = 'json';
      req.onload = resp => {
        if (req.status !== 200) {
          // Erro, não faz nada
          // if (req.status === 403) {
          //   // Forbiden - Não tem permissão
          //   alert('Desculpe, mas você não tem permissão!')
          // }
          // else
          //   alert('Request failed.  Returned status of ' + req.status);
        } else {
          self.timer = req.response;
          self.show_date();
        }
      };

      req.open('get', self.url_load, true);
      req.setRequestHeader("X-Requested-With", "XMLHttpRequest");
      req.setRequestHeader("X-CSRFToken", getCookie('csrftoken')); //csrftoken);
      req.setRequestHeader("HTTP_X_CSRFTOKEN", getCookie('csrftoken')); //csrftoken);
      req.send()
    });

    self.click_start = function(element){
      $('.tooltip').tooltip("hide");
      self.timer.started = true;
      self.show_date();
    };

    self.click_stop = function(element){
      $('.tooltip').tooltip("hide");
      self.timer.started = false;
      self.show_date();

      const req = new XMLHttpRequest();
      req.responseType = 'json';
      req.onload = resp => {
        if (req.status !== 200) {
          // Erro, não faz nada
          // if (req.status === 403) {
          //   // Forbiden - Não tem permissão
          //   alert('Desculpe, mas você não tem permissão!')
          // }
          // else
          //   alert('Request failed.  Returned status of ' + req.status);
        } else {
          self.timer = req.response;
          self.show_date();
        }
      };

      var duration = `${self.url_stop}${self.timer.duration}/`;
      req.open('post', duration, true);
      req.setRequestHeader("X-Requested-With", "XMLHttpRequest");
      req.setRequestHeader("X-CSRFToken", getCookie('csrftoken')); //csrftoken);
      req.setRequestHeader("HTTP_X_CSRFTOKEN", getCookie('csrftoken')); //csrftoken);
      req.send()
    };

    self.click_reset = function(element){
      self.timer.duration = 0;
      self.click_stop();
    };
  </script>

</ftl-timer>
