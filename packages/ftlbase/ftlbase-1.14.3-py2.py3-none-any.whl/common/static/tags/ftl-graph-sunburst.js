riot.tag2('ftl-graph-sunburst', '', '', '', function(opts) {
    var self = this;

    self.title = undefined;
    self.description = undefined;
    self.values = undefined;

    function plot_sunburst(id, raw_data) {

      const pt_BR = {
        "decimal": ",",
        "thousands": ".",
        "grouping": [3],
        "currency": ["R$ ", ""],
        "dateTime": "%d/%m/%Y H:%M:%S",
        "date": "%d/%m/%Y",
        "time": "%H:%M",
        "periods": ["", ""],
        "days": ["Domingo", "Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado"],
        "shortDays": ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sab"],
        "months": ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"],
        "shortMonths": ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
      };
      const locale = d3.formatDefaultLocale(pt_BR);

      const base_id = id.split('#').pop();
      const title = document.getElementById(`${base_id}-title`);
      const description = document.getElementById(`${base_id}-description`);
      if (title && raw_data.title) title.innerText = raw_data.title;
      if (description && raw_data.description) description.innerText = raw_data.description;

      function buildHierarchy(csv) {

        const root = {name: "root", children: []};
        for (let i = 0; i < csv.length; i++) {
          const sequence = csv[i][0];
          const size = +csv[i][1];
          if (isNaN(size)) {

            continue;
          }
          const parts = sequence.split("->");
          let currentNode = root;
          for (let j = 0; j < parts.length; j++) {
            const children = currentNode["children"];
            const nodeName = parts[j];
            let childNode = null;
            if (j + 1 < parts.length) {

              let foundChild = false;
              for (let k = 0; k < children.length; k++) {
                if (children[k]["name"] === nodeName) {
                  childNode = children[k];
                  foundChild = true;
                  break;
                }
              }

              if (!foundChild) {
                childNode = {name: nodeName, children: [], color: csv[i][2], id: csv[i][3]};
                children.push(childNode);
              }
              currentNode = childNode;
            } else {

              childNode = {name: nodeName, value: size, color: csv[i][2], id: csv[i][3]};
              children.push(childNode);
            }
          }
        }
        return root;
      }
      hieararchy_data = buildHierarchy(raw_data.values);

      function build_names_plot(csv) {

        const names_for_color = [];

        for (let i = 0; i < csv.length; i++) {
          const sequence = csv[i][0];
          const parts = sequence.split("->");
          for (let j = 0; j < parts.length; j++) {
            names_for_color.push(parts[j]);
          }
        }
        return [...new Set(names_for_color)]
      }
      const names_plot = build_names_plot(raw_data.values);

      function breadcrumb(sunburst) {
        const routes = [];
        sunburst.sequence.forEach(d => {
          const percentage = locale.format(",.1f")(((100 * d.value) / root.value).toPrecision(3)) + "%";
          const badge = `${d.value} / ${percentage}`;
          routes.push({text: d.data.name, badge: badge});
        });
        if (document.getElementById('summariesSunburst-breadcrumb')._tag) {
          document.getElementById('summariesSunburst-breadcrumb')._tag.update({links: routes, numbered: false});
        } else {
          riot.mount(`${id}-breadcrumb`, 'ftl-breadcrumb', {links: routes, numbered: false});
        }
      }

      const width = Math.min(getContentWidth(document.getElementById(`${base_id}`)), window.innerHeight)*0.7;
      const radius = width / 2;
      const mousearc = d3
        .arc().startAngle(d => d.x0).endAngle(d => d.x1)
        .innerRadius(d => Math.sqrt(d.y0)).outerRadius(radius);
      const arc = d3
        .arc().startAngle(d => d.x0).endAngle(d => d.x1).padAngle(1 / radius).padRadius(radius)
        .innerRadius(d => Math.sqrt(d.y0)).outerRadius(d => Math.sqrt(d.y1) - 1);

      const partition = data =>
        d3.partition().size([2 * Math.PI, radius * radius])(
          d3
            .hierarchy(data)
            .sum(d => d.value)

            .sort((a, b) => a.data.id - b.data.id || b.value - a.value)
        );

      const root = partition(hieararchy_data);
      const svg = d3.select(id).append('svg');

      const element = svg.node();
      element.value = {sequence: [], percentage: 0.0};

      const label = svg
        .append("text")
        .attr("text-anchor", "middle")
        .attr("fill", "#888")
        .style("visibility", "hidden");

      label
        .append("tspan")
        .attr("class", "percentage")
        .attr("x", 0)
        .attr("y", 0)
        .attr("dy", "0.35em")
        .attr("font-size", "3em")
        .text("");

      svg
        .attr("viewBox", `${-radius} ${-radius} ${width} ${width}`)
        .style("max-width", `${width}px`)
        .style("font-size", "12px")
        .style("font-family", "'Source Sans Pro','Helvetica Neue',Helvetica,Arial,sans-serif");

      var color = d3
        .scaleOrdinal()
        .domain(names_plot)
        .range(d3.quantize(t => d3.interpolateSpectral(t * 0.8 + 0.1), names_plot.length).reverse());

      function my_color(d) {

        const cor = d3.color(d.data.color);
        const percent = 0.15;
        cor.opacity = 1 - percent * (d.depth - 1);
        const sequence = d
          .ancestors()
          .reverse()
          .slice(1);
        if (d.depth > 1) {
          const le = d.parent.children.length;
          const position = d.parent.children.indexOf(d);
          cor.opacity = cor.opacity * (1 - percent * position / 3);
        }
        return cor
      }

      const path = svg
        .append("g")
        .selectAll("path")
        .data(root.descendants().filter(d => {

          return d.depth && d.x1 - d.x0 > 0.001;
        }))
        .join("path")
        .attr("fill", d => my_color(d))

        .attr("d", arc);

      svg
        .append("g")
        .attr("fill", "none")
        .attr("pointer-events", "all")
        .on("mouseleave", () => {
          path.attr("fill-opacity", 1);
          label.style("visibility", "hidden");

          element.value = {sequence: [], percentage: 0.0};

          breadcrumb(element.value);
        })
        .selectAll("path")
        .data(root.descendants().filter(d => {

          return d.depth && d.x1 - d.x0 > 0.001;
        }))
        .join("path")
        .attr("d", mousearc)
        .on("mouseenter", (event, d) => {

          const sequence = d
            .ancestors()
            .reverse()
            .slice(1);

          path.attr("fill-opacity", node =>
            sequence.indexOf(node) >= 0 ? 1.0 : 0.3
          );
          const percentage = locale.format(",.1f")(((100 * d.value) / root.value).toPrecision(3)) + "%";
          const badge = `${d.value} / ${percentage}`;
          label
            .style("visibility", null)
            .select(".percentage")
            .text(badge);

          element.value = {sequence, percentage};

          breadcrumb(element.value);
        });

      return element;
    }

    self.on('mount', function () {

      self.div_id = opts.div_id;
      self.title = opts.title;
      self.description = opts.description;
      self.values = opts.values;
      if (self.values && (self.values.length > 0)) {
        const param = {title: self.title, description: self.description, values: self.values};
        var el = plot_sunburst(self.div_id, param);
      }
    })
});
