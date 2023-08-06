var PIEMixin = {
  init: function() {
  },
  _setData: function(values){
      data = []
      if(values){
          for (i = 0; i < values.length; i++) {
              data.push({label: values[i].label, value: values[i].value , caption: values[i].value.toString()})
          }
      }
      return data
  },
}


riot.tag2('dashboard-pie', '', '', '', function(opts) {
        var self = this

        self.title = opts.title
        self.description = opts.description
        self.values = opts.values

        self.on('mount',function(){
            if(self.values && (self.values.length > 0)){
                self.data = []
                for (i = 0; i < self.values.length; i++) {
                    self.data.push({label: self.values[i].label, value: self.values[i].value , caption: self.values[i].value.toString()})
                }

                var dashboardStatus2 = new pie(self.root, self.title, self.description, self.data)
            }
        })
});

riot.tag2('dashboard', '<div id="dashboard" class="row"> <div class="row"> <div id="dashboard-status" class="col-md-4 text-center"></div> <div id="dashboard-pendentes" class="col-md-4 text-center"></div> <div id="dashboard-tarefas" class="col-md-4 text-center"></div> </div> <div class="row"> <div id="chart" class="col-md-1"></div><div id="chart"><svg style="width:1000px;height:500px;"></div> </div> <div class="row"> <div class="col-md-1"></div><div id="multibarchart_container"><svg style="width:600px;height:400px;"></svg></div> </div> </div>', '', '', function(opts) {
        var self = this
        self.status = opts.status
        self.atendimentos = opts.atendimentos
        self.pendentes = opts.pendentes
        self.atendimentosPendentes = opts.atendimentosPendentes
        self.tarefas = opts.tarefas
        self.tarefasPendentes = opts.tarefasPendentes
        self.chart = opts.chart
        self.chart_data = opts.chart_data
        self.multibarchart = opts.multibarchart
        self.multibarchart_data = opts.multibarchart_data

        self.on('mount',function(){
            if (self.status && (self.atendimentos.length > 0)) {

                riot.mount('#dashboard-status', 'dashboard-pie', {

                    title: "Atendimentos por Status",
                    description: "Quantidade de atendimentos realizados no mês",
                    values: self.atendimentos
                })
            }
            if (self.pendentes && (self.atendimentosPendentes.length > 0)) {

                riot.mount('#dashboard-pendentes', 'dashboard-pie', {

                    title: "Atendimentos Pendentes",
                    description: "Quantidade de atendimentos pendentes",
                    values: self.atendimentosPendentes
                })
            }
            if (self.tarefas && (self.tarefasPendentes.length > 0)) {

                riot.mount('#dashboard-tarefas', 'dashboard-pie', {
                    element: 'dashboard-tarefas',
                    title: "Tarefas Pendentes",
                    description: "Quantidade de tarefas pendentes",
                    values: self.tarefasPendentes
                })
            }
            if (self.tarefas) {
                riot.mount('dashboard-tarefas-pendentes', {values: self.tarefasPendentes})
            }
            if (self.chart) {
                myChart2 = complexBarChart('#chart svg', self.chart_data, 'Saldo de Caixa', '', 'Saldo(R$)', 960, 500);

            }
            if (self.multibarchart) {
                myChart = simpleBarChart('#multibarchart', self.multibarchart_data, 'Saldo de Caixa', '', 'Saldo(R$)', 960, 500);

            }
        })
});


