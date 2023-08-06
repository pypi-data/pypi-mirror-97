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

  var data = [1, 2, 3, 4];
  var ret = d3.pie()(data);
  return ret;

  return new d3.pie()(element, {
    "header": {
      "title": {
        "text": title,
        "fontSize": 23,
        "font": "verdana"
      },
      "subtitle": {
        "text": subtitle,
        "color": "#999999",
        "fontSize": 12,
        "font": "verdana"
      },
      "titleSubtitlePadding": 12
    },
    "footer": {
      "color": "#999999",
      "fontSize": 11,
      "font": "open sans",
      "location": "bottom-center"
    },
    "size": {
      "canvasHeight": 350,
      "canvasWidth": 400,
      "pieOuterRadius": "88%"
    },
    "data": {
      "sortOrder": "value-desc",
      "smallSegmentGrouping": {
        "enabled": true,
        "value": 4,
        "label": "Outros"
      },
      "content": content
    },
    "labels": {
      "outer": {
        "format": "label-percentage2",
        "pieDistance": 32
      },
      "inner": {
        "format": "value"
      },
      "mainLabel": {
        "font": "verdana",
        "fontSize": 14
      },
      "percentage": {
        "color": "#bc6666",
        "font": "verdana",
        "fontSize": 12,
        "decimalPlaces": 0
      },
      "value": {
        "color": "#fcfcfc",
        "font": "verdana",
        "fontSize": 12,
      },
      "lines": {
        "enabled": true,
        "color": "#cccccc"
      },
      "truncation": {
        "enabled": true
      }
    },
    "effects": {
      "load": {
        "speed": 500
      },
      "pullOutSegmentOnClick": {
        "effect": "linear",
        "speed": 400,
        "size": 8
      }
    }
  });
}

function simpleBarChart(element, data, title, titleX, titleY, width2, height2) {
// nv.addGraph(function() {
//   var chart = nv.models.discreteBarChart()
//       .x(function(d) { return d.label })    //Specify the data accessors.
//       .y(function(d) { return d.value })
//       .staggerLabels(true)    //Too many bars and not enough room? Try staggering labels.
//       .tooltips(false)        //Don't show tooltips
//       .showValues(true)       //...instead, show the bar value right on top of each bar.
//       .transitionDuration(350)
//       ;

//   d3.select('#chart svg')
//       .datum(data) //.datum(exampleData())
//       .call(chart);

//   nv.utils.windowResize(chart.update);

//   return chart;
// });

  var margin = {top: 20, right: 20, bottom: 100, left: 100}; //margin = {top: 20, right: 20, bottom: 30, left: 40};
  // if (title.length>0) {
  //   margin.top = margin.top+30
  // }
  var width = width2 - margin.left - margin.right,
    height = height2 - margin.top - margin.bottom;

  var x = d3.scale.ordinal()
    .rangeRoundBands([0, width], 0.1);

  var y = d3.scale.linear()
    .range([height, 0]);

  var xAxis = d3.svg.axis()
    .scale(x)
    .orient("bottom")
  ;

  var yAxis = d3.svg.axis()
      .scale(y)
      .orient("left")
    //.ticks(10, "%")
  ;

  var svg = d3.select(element).append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
  // if (title.length>0) {
  //   svg
  //     .append("text")
  //       .attr("y", width/2)
  //       .attr("dy", ".71em")
  //       .style("text-anchor", "middle")
  //       .text(title);
  // }
  // svg
  //     .append("g")
  //       .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  data.forEach(function (d) {
    d.value = +d.value;
  });

  x.domain(data.map(function (d) {
    return d.x;
  }));
  var ymin = d3.min(data, function (d) {
    return d.value;
  });
  var ymax = d3.max(data, function (d) {
    return d.value;
  });
  if ((ymin >= 0) && (ymax >= 0)) {
    ymin = 0;
  }
  y.domain([ymin, ymax]);//y.domain([0, d3.max(data, function(d) { return d.value; })]);

  svg
    .append("g")
    .attr("class", "x axis")
    .attr("transform", "translate(0," + height + ")")
    .call(xAxis)
    .selectAll("text")
    .style("text-anchor", "end")
    .attr("dx", "-.8em")
    .attr("dy", "-.55em")
    .attr("transform", "rotate(-90)")
  //.text(titleX)
  ;

  svg
    .append("g")
    .attr("class", "y axis")
    .call(yAxis)
    .append("text")
    .attr("transform", "rotate(-90)")
    .attr("y", 4)
    .attr("dy", ".71em")
    .style("text-anchor", "end")
    .text(titleY)
  ;

  svg
    .selectAll(".bar")
    .data(data)
    .enter().append("rect")
    //.style("fill", "steelblue")
    .attr("class", "bar")
    .attr("x", function (d) {
      return x(d.x);
    })
    .attr("width", x.rangeBand())
    .attr("y", function (d) {
      return y(d.value);
    })
    .attr("height", function (d) {
      return height - y(d.value);
    });

  return svg;
}

/* Inspired by Lee Byron's test data generator. */
function stream_layers(n, m, o) {
  if (arguments.length < 3) o = 0;

  function bump(a) {
    var x = 1 / (0.1 + Math.random()),
      y = 2 * Math.random() - 0.5,
      z = 10 / (0.1 + Math.random());
    for (var i = 0; i < m; i++) {
      var w = (i / m - y) * z;
      a[i] += x * Math.exp(-w * w);
    }
  }

  return d3.range(n).map(function () {
    var a = [], i;
    for (i = 0; i < m; i++) a[i] = o + o * Math.random();
    for (i = 0; i < 5; i++) bump(a);
    return a.map(stream_index);
  });
}

/* Another layer generator using gamma distributions. */
function stream_waves(n, m) {
  return d3.range(n).map(function (i) {
    return d3.range(m).map(function (j) {
      var x = 20 * j / m - i / 3;
      return 2 * x * Math.exp(-0.5 * x);
    }).map(stream_index);
  });
}

function stream_index(d, i) {
  return {x: i, y: Math.max(0, d)};
}

// Set locale
var pt_BR = {
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
var locale = d3.formatDefaultLocale(pt_BR);

function complexBarChart(element, data, title, titleX, titleY, width2, height2) {
  if (1 == 1) {
    nv.addGraph(function () {

      var margin = {top: 20, right: 20, bottom: 100, left: 100}; //margin = {top: 20, right: 20, bottom: 30, left: 40};

      var chart = nv.models.multiBarChart()
        //.transitionDuration(350)  // deprecated => .duration()
        .duration(350)
        .reduceXTicks(true)   //If 'false', every single x-axis tick label will be rendered.
        .rotateLabels(-90)      //Angle to rotate x-axis labels.
        .showControls(true)   //Allow user to switch between 'Grouped' and 'Stacked' mode.
        .groupSpacing(0.1)    //Distance between each group of bars.
      ;

      //chart.legend.margin({top: 5, right: 100, bottom: 50, left: 100});
      //chart.legend.margin().bottom = 50;
      //chart.margin( {top: 30, right: 20, bottom: 50, left: 60} );
      chart.margin().left = 110;


      chart.xAxis
      //.tickFormat(d3.format(',f'))
      //.tickPadding(25)
      ;

      chart.yAxis
        //.tickPadding(25)
        .tickFormat(locale.numberFormat('$,.2f')); //.tickFormat(d3.format(',.2f')); locale.numberFormat(

      //console.log(console, data);

      d3.select(element)
        .datum(data)
        //.datum(exampleData())
        .call(chart);

      nv.utils.windowResize(chart.update);

      return chart;
    });
  }

  //Generate some nice data.
  //   function exampleData() {
  //     return stream_layers(3,10+Math.random()*100,0.1).map(function(data, i) {
  //       return {
  //         key: 'Stream #' + i,
  //         values: data
  //       };
  //     });
  //   }
  // }

  if (1 === 0) {
    nv.addGraph(function () {
      var chart = nv.models.discreteBarChart()
        .x(function (d) {
          return d.label
        })    //Specify the data accessors.
        .y(function (d) {
          return d.value
        })
        .staggerLabels(true)    //Too many bars and not enough room? Try staggering labels.
        //.tooltips(false)        //Don't show tooltips
        .showValues(true)       //...instead, show the bar value right on top of each bar.
        //.transitionDuration(350)
        .duration(350)
      ;

      d3.select(element)
        .datum(data) //.datum(exampleData())
        .call(chart);

      nv.utils.windowResize(chart.update);

      return chart;
    });
  }
}

//
// Função transferida para ftl-graph-sunburst.tag
//
// function plot_sunburst(id, raw_data) {
//   const base_id = id.split('#').pop();
//   const title = document.getElementById(`${base_id}-title`);
//   const description = document.getElementById(`${base_id}-description`);
//   if (title && raw_data.title) title.innerText = raw_data.title;
//   if (description && raw_data.description) description.innerText = raw_data.description;
//
//   function buildHierarchy(csv) {
//     // Helper function that transforms the given CSV into a hierarchical format.
//     // CSV possui: Nome, qtde, cor, id
//     const root = {name: "root", children: []};
//     for (let i = 0; i < csv.length; i++) {
//       const sequence = csv[i][0];
//       const size = +csv[i][1];
//       if (isNaN(size)) {
//         // e.g. if this is a header row
//         continue;
//       }
//       const parts = sequence.split("->");
//       let currentNode = root;
//       for (let j = 0; j < parts.length; j++) {
//         const children = currentNode["children"];
//         const nodeName = parts[j];
//         let childNode = null;
//         if (j + 1 < parts.length) {
//           // Not yet at the end of the sequence; move down the tree.
//           let foundChild = false;
//           for (let k = 0; k < children.length; k++) {
//             if (children[k]["name"] === nodeName) {
//               childNode = children[k];
//               foundChild = true;
//               break;
//             }
//           }
//           // If we don't already have a child node for this branch, create it.
//           if (!foundChild) {
//             childNode = {name: nodeName, children: [], color: csv[i][2], id: csv[i][3]};
//             children.push(childNode);
//           }
//           currentNode = childNode;
//         } else {
//           // Reached the end of the sequence; create a leaf node.
//           childNode = {name: nodeName, value: size, color: csv[i][2], id: csv[i][3]};
//           children.push(childNode);
//         }
//       }
//     }
//     return root;
//   }
//
//   hieararchy_data = buildHierarchy(raw_data.values);
//
//   function build_names_plot(csv) {
//     // Helper function that transforms the given CSV into a hierarchical format.
//     const names_for_color = [];
//
//     for (let i = 0; i < csv.length; i++) {
//       const sequence = csv[i][0];
//       const parts = sequence.split("->");
//       for (let j = 0; j < parts.length; j++) {
//         names_for_color.push(parts[j]);
//       }
//     }
//     return [...new Set(names_for_color)]
//   }
//
//   const names_plot = build_names_plot(raw_data.values);
//
//   function breadcrumb(sunburst) {
//     const routes = [];
//     sunburst.sequence.forEach(d => {
//       const percentage = locale.format(",.1f")(((100 * d.value) / root.value).toPrecision(3)) + "%";
//       routes.push({text: d.data.name, badge: percentage});
//     });
//     riot.mount(`${id}-breadcrumb`, 'ftl-breadcrumb', {links: routes, numbered: false});
//   }
//
//   var width = 400;
//   var radius = width / 2;
//   var mousearc = d3
//     .arc().startAngle(d => d.x0).endAngle(d => d.x1)
//     .innerRadius(d => Math.sqrt(d.y0)).outerRadius(radius);
//   var arc = d3
//     .arc().startAngle(d => d.x0).endAngle(d => d.x1).padAngle(1 / radius).padRadius(radius)
//     .innerRadius(d => Math.sqrt(d.y0)).outerRadius(d => Math.sqrt(d.y1) - 1);
//
//   var partition = data =>
//     d3.partition().size([2 * Math.PI, radius * radius])(
//       d3
//         .hierarchy(data)
//         .sum(d => d.value)
//         // Ou usa o id se foi passado pelo json ou usa o valor
//         .sort((a, b) => a.data.id - b.data.id || b.value - a.value)
//     );
//
//   const root = partition(hieararchy_data);
//   const svg = d3.select(id).append('svg');
//
//   // Make this into a view, so that the currently hovered sequence is available to the breadcrumb
//   const element = svg.node();
//   element.value = {sequence: [], percentage: 0.0};
//
//   const label = svg
//     .append("text")
//     .attr("text-anchor", "middle")
//     .attr("fill", "#888")
//     .style("visibility", "hidden");
//
//   label
//     .append("tspan")
//     .attr("class", "percentage")
//     .attr("x", 0)
//     .attr("y", 0)
//     .attr("dy", "0.35em")
//     .attr("font-size", "3em")
//     .text("");
//
//   svg
//     .attr("viewBox", `${-radius} ${-radius} ${width} ${width}`)
//     .style("max-width", `${width}px`)
//     .style("font-size", "12px")
//     .style("font-family", "'Source Sans Pro','Helvetica Neue',Helvetica,Arial,sans-serif");
//
//   var color = d3
//     .scaleOrdinal()
//     .domain(names_plot)
//     .range(d3.quantize(t => d3.interpolateSpectral(t * 0.8 + 0.1), names_plot.length).reverse());
//
//   function my_color(d) {
//     // return color(d.data.name);
//     const cor = d3.color(d.data.color);
//     const percent = 0.15;
//     cor.opacity = 1 - percent * (d.depth - 1);
//     const sequence = d
//       .ancestors()
//       .reverse()
//       .slice(1);
//     if (d.depth > 1) {
//       const le = d.parent.children.length;
//       const position = d.parent.children.indexOf(d);
//       cor.opacity = cor.opacity * (1 - percent * position / 3);
//     }
//     return cor
//   }
//
//   const path = svg
//     .append("g")
//     .selectAll("path")
//     .data(
//       root.descendants().filter(d => {
//         // Don't draw the root node, and for efficiency, filter out nodes that would be too small to see
//         return d.depth && d.x1 - d.x0 > 0.001;
//       })
//     )
//     .join("path")
//     .attr("fill", d => my_color(d))
//     // .attr("fill", d => color(d.data.name))
//     .attr("d", arc);
//
//   svg
//     .append("g")
//     .attr("fill", "none")
//     .attr("pointer-events", "all")
//     .on("mouseleave", () => {
//       path.attr("fill-opacity", 1);
//       label.style("visibility", "hidden");
//       // Update the value of this view
//       element.value = {sequence: [], percentage: 0.0};
//       // element.dispatchEvent(new CustomEvent("input"));
//       breadcrumb(element.value);
//     })
//     .selectAll("path")
//     .data(
//       root.descendants().filter(d => {
//         // Don't draw the root node, and for efficiency, filter out nodes that would be too small to see
//         return d.depth && d.x1 - d.x0 > 0.001;
//       })
//     )
//     .join("path")
//     .attr("d", mousearc)
//     .on("mouseenter", (event, d) => {
//       // Get the ancestors of the current segment, minus the root
//       const sequence = d
//         .ancestors()
//         .reverse()
//         .slice(1);
//       // Highlight the ancestors
//       path.attr("fill-opacity", node =>
//         sequence.indexOf(node) >= 0 ? 1.0 : 0.3
//       );
//       const percentage = ((100 * d.value) / root.value).toPrecision(3);
//       label
//         .style("visibility", null)
//         .select(".percentage")
//         .text(locale.format(",.1f")(percentage) + "%");
//       // Update the value of this view with the currently hovered sequence and percentage
//       element.value = {sequence, percentage};
//       // element.dispatchEvent(new CustomEvent("input"));
//       breadcrumb(element.value);
//     });
//
//   return element;
// }
