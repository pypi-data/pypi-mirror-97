<ftl-graph-pie>
  <script>
    var self = this;
    // self.element = opts.element ? opts.element : 'pie'
    self.title = undefined;
    self.description = undefined;
    self.values = undefined;

    function pie(element, title, subtitle, content) {
      var pie = d3.pie().sort(null).value(d => d.value);
      var width = 600;
      var height = Math.min(width, 500);
      var arc = d3.arc().innerRadius(0).outerRadius(Math.min(width, height) / 2 - 1);
      var color = d3.scaleOrdinal()
        .domain(content.map(d => d.label))
        .range(d3.quantize(t => d3.interpolateSpectral(t * 0.8 + 0.1), content.length).reverse());
      const radius = Math.min(width, height) / 2 * 0.8;
      var arcLabel = d3.arc().innerRadius(radius).outerRadius(radius);

      const arcs = pie(content);

      const svg = d3.create("svg").attr("viewBox", [-width / 2, -height / 2, width, height]);

      svg.append("g")
        .attr("stroke", "white")
        .selectAll("path")
        .data(arcs)
        .join("path")
        .attr("fill", d => d.data.color ? d3.color(d.data.color) : color(d.data.label))
        .attr("d", arc)
        .append("title")
        // .text(d => `${d.data.label}: ${d.data.value.toLocaleString()}`);
        .text(d => `${d.data.label}: ${d.data}`);

      svg.append("g")
        .attr("font-family", "sans-serif")
        .attr("font-size", 12)
        .attr("text-anchor", "middle")
        .selectAll("text")
        .data(arcs)
        .join("text")
        .attr("transform", d => `translate(${arcLabel.centroid(d)})`)
        .call(text => text.append("tspan")
          .attr("y", "-0.4em")
          .attr("font-weight", "bold")
          .text(d => d.data.label))
        .call(text => text.filter(d => (d.endAngle - d.startAngle) > 0.25).append("tspan")
          .attr("x", 0)
          .attr("y", "0.7em")
          .attr("fill-opacity", 0.7)
          .text(d => d.data.value.toLocaleString()));

      return svg.node();
    }

    // console.log('dashboard-pie (',self.element,') =', self.data)
    self.on('mount', function () {
      self.title = opts.title;
      self.description = opts.description;
      self.values = opts.values;
      if (self.values && (self.values.length > 0)) {
        self.data = [];
        for (i = 0; i < self.values.length; i++) {
          self.data.push({
            label: self.values[i].label,
            value: self.values[i].value,
            color: self.values[i].color,
            // caption: self.values[i].value.toString()
          });
        }
        self.data.push({columns: ['label', 'value']});
        // console.log('dashboard-pie (',self.element,') =', self.data)
        var dashboardStatus2 = pie(self.root, self.title, self.description, self.data);
        self.root.innerHTML = dashboardStatus2.outerHTML;
      }
    })
  </script>
</ftl-graph-pie>


