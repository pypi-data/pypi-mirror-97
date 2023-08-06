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


<dashboard-pie>
    <script>
        var self = this
        // self.element = opts.element ? opts.element : 'pie'
        self.title = opts.title
        self.description = opts.description
        self.values = opts.values

        // console.log('dashboard-pie (',self.element,') =', self.data)
        self.on('mount',function(){
            if(self.values && (self.values.length > 0)){
                self.data = []
                for (i = 0; i < self.values.length; i++) {
                    self.data.push({label: self.values[i].label, value: self.values[i].value , caption: self.values[i].value.toString()})
                }
                // console.log('dashboard-pie (',self.element,') =', self.data)
                var dashboardStatus2 = new pie(self.root, self.title, self.description, self.data)
            }
        })
    </script>
</dashboard-pie>

<dashboard>
    <div id="dashboard" class="row">
    <div class="row">
        <div id="dashboard-status" class="col-md-4 text-center" ></div>
        <div id="dashboard-pendentes" class="col-md-4 text-center" ></div>
        <div id="dashboard-tarefas" class="col-md-4 text-center" ></div>
    </div>
    <div class="row">
        <div id="chart" class="col-md-1"></div><div id="chart" ><svg style="width:1000px;height:500px;"></div>
    </div>
    <div class="row">
        <div class="col-md-1"></div><div id="multibarchart_container"><svg style="width:600px;height:400px;"></svg></div>
    </div>
    </div>

    <script>
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

        // self.on('before-mount',function(){
        //     self.tags.dashboard_status.unmount(true)
        //     self.tags.prioridade.unmount(true)
        //     self.tags.tarefas.unmount(true)
        //     self.tags.chart.unmount(true)
        //     self.tags.multibarchart.unmount(true)
        // })

        self.on('mount',function(){
            if (self.status && (self.atendimentos.length > 0)) {
                // console.log('Mount dashboard-status', self.atendimentos, 'status=', self.status)
                riot.mount('#dashboard-status', 'dashboard-pie', {
                    //element: 'dashboard-status',
                    title: "Atendimentos por Status",
                    description: "Quantidade de atendimentos realizados no mês",
                    values: self.atendimentos
                })
            }
            if (self.pendentes && (self.atendimentosPendentes.length > 0)) {
                // console.log('Mount dashboard-pendentes', self.atendimentosPendentes, 'status=', self.status)
                riot.mount('#dashboard-pendentes', 'dashboard-pie', {
                    //element: 'dashboard-pendentes',
                    title: "Atendimentos Pendentes",
                    description: "Quantidade de atendimentos pendentes",
                    values: self.atendimentosPendentes
                })
            }
            if (self.tarefas && (self.tarefasPendentes.length > 0)) {
                // console.log('Mount dashboard-tarefas', self.tarefasPendentes, 'status=', self.status)
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
                myChart2 = complexBarChart('#chart svg', self.chart_data, 'Saldo de Caixa', '', 'Saldo(R$)', 960, 500); //.width(450).height(400);
                //riot.mount('dashboard-chart')
            }
            if (self.multibarchart) {
                myChart = simpleBarChart('#multibarchart', self.multibarchart_data, 'Saldo de Caixa', '', 'Saldo(R$)', 960, 500); //.width(450).height(400);
                //riot.mount('dashboard-multibarchart')
            }
        })
    </script>

</dashboard>

<!--
{% comment "Transferencia para tags" %}
  {% if perms.atendimento.add_atendimento and atendimentos %}
  var _dashboardStatus = new pie("dashboardStatus", "Atendimentos por Status", "Quantidade de atendimentos realizados no mês",
   [{% for st in atendimentos %}
         { label: "{{ st.status }}", value: {{ st.value }}, caption: "{{ st.value }}" },{% endfor %}
      ]
  );
  {% endif %}
  {% if perms.atendimento.add_atendimento and atendimentosPendentes %}
  var _dashboardPrioridade = new pie("dashboardPrioridade", "Atendimentos Pendentes", "Quantidade de atendimentos pendentes",
   [{% for st in atendimentosPendentes %}
         { label: "{{ st.prioridade }}", value: {{ st.value }}, caption: "{{ st.value }}" },{% endfor %}
      ]
  );
  //console.log('dashboard-pend');
  {% endif %}
  {% if perms.imobiliar.add_tarefas and tarefasPendentes %}
  var _dashboardTarefasPendentes = new pie("dashboardTarefasPendentes", "Tarefas Pendentes", "Quantidade de tarefas pendentes",
   [{% for st in tarefasPendentes %}
         { label: "{{ st.usuario }}", value: {{ st.qtde }}, caption: "{{ st.qtde }}" },{% endfor %}
      ]
  );
  {% endif %}
  var data2 = [
                {
                  key: "Saldo da Conta {{ conta }}",
                    values: [{% for st in saldosCaixa %}
                                 { x: "{# st.data|date:"m/Y" #}{{ st.competencia}}", y: {{ st.saldoini|unlocalize }} },{% endfor %}
                    ]
                },
                {
                  key: "Saldo da Conta {{ conta02 }}",
                    values: [{% for st in saldosCaixa02 %}
                                 { x: "{# st.data|date:"m/Y" #}{{ st.competencia}}", y: {{ st.saldoini|unlocalize }} },{% endfor %}
                    ]
                },
                {
                  key: "Saldo da Conta {{ conta03 }}",
                    values: [{% for st in saldosCaixa03 %}
                                 { x: "{# st.data|date:"m/Y" #}{{ st.competencia}}", y: {{ st.saldoini|unlocalize }} },{% endfor %}
                    ]
                },
                {
                  key: "Saldo da Conta {{ conta2 }}",
                    values: [{% for st in saldosCaixa2 %}
                                 { x: "{# st.data|date:"m/Y" #}{{ st.competencia}}", y: {{ st.saldoini|unlocalize }} },{% endfor %}
                    ]
                },
                {
                  key: "Saldo da Conta {{ conta1 }}",
                    values: [{% for st in saldosCaixa1 %}
                                 { x: "{# st.data|date:"m/Y" #}{{ st.competencia}}", y: {{ st.saldoini|unlocalize }} },{% endfor %}
                    ]
                },
                {
                  key: "Saldo da Conta {{ conta102 }}",
                    values: [{% for st in saldosCaixa102 %}
                                 { x: "{# st.data|date:"m/Y" #}{{ st.competencia}}", y: {{ st.saldoini|unlocalize }} },{% endfor %}
                    ]
                },
                {
                  key: "Saldo da Conta {{ conta103 }}",
                    values: [{% for st in saldosCaixa103 %}
                                 //{ x: "{# st.data|date:"d/m/Y" #}{{ st.data}}", y: {{ st.saldoini|unlocalize }} },{ endfor }
                                 { x: "{# st.data|date:"m/Y" #}{{ st.competencia}}", y: {{ st.saldoini|unlocalize }} },{% endfor %}
                    ]
                },
              ]
  var myChart2 = complexBarChart('#chart svg', data2, 'Saldo de Caixa', '', 'Saldo(R$)', 960, 500); //.width(450).height(400);

  var eixoY = [{% for st in saldosCaixa %} {{ st.saldoini|unlocalize }}, {% endfor %}];
  var eixoX = [{% for st in saldosCaixa %} "{# st.data pipe date doispontos "m/Y" #}{{ st.competencia}}", {% endfor %}];
  var data = eixoX.map(function(d,i){return {"value":-eixoY[i]+100000,"x":eixoX[i]};});
  var myChart = simpleBarChart('#multibarchart', data, 'Saldo de Caixa', '', 'Saldo(R$)', 960, 500); //.width(450).height(400);
  {% load l10n %}

{% endcomment %}
-->
