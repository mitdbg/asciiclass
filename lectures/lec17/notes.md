


# Visualization Toolkits

## Component based (using rickshaw)

Define objects that encapsulate an entire graphic.

    bar_chart(data) --> bar chart graphic
    line_chart(data) --> line chart graphic

Examples

* Excel
* Google Charts
* Rickshaw

SHOW DEMO

0. console.log(rows[0])
1. Render the data using y = count, x = time
  * component doesnt support date types.  whoops
2. Group data by location and render as multiple lines

        // extract each location
        var keys = _.uniq(_.map(data, function(d){return d.name}));
        var series = _.map(keys, function(key) {
          return _.filter(data, function(d) { return d.name == key; })
        });
        series = _.map(series, function(s) {
          return { data: s };   // actuall need color!
        })
        var graph = new Rickshaw.Graph( {
          element: document.querySelector("#chart"),
          width: 900,
          height: 300,
          renderer: 'line',
          series: series
        });

3. Add color (map location to color)

    
        var colors = ["#c05020", "steelblue", "#6060c0"];
        series = _.map(series, function(data, i) {
          return {color: colors[i], data: data };
        });

Pros

* Easy to use
* Batteries included (legend, interaction, etc)

Cons

* Difficult to _iterate_
  * change variables to render
  * add aesthetic variables (color)
  * change ordering
  * change layout
  * change scaling e.g., log transform
  * change aesthetics (point, bar)
  * change data goruping
  * change variable types
* Only performs rendering part of visual analysis


## Grammar Based

One of our arguments is that the graphic is defined by the intended
message/insight, and so entire visualization is driven by the
message.  What would a language to represent this message look like?
(this section is based off Wilkinson's Grammar of Graphics)

It turns out that there is a structued approach towards creating 
statistical graphics.  It can be broken down into several orthogonal 
components

* Data
* Facets
* Subplot
* Layers
* Scales
* Groups
* Coordinate System


The value of a grammar based approach:

* reuse existing analysis and only change single part
* visualization must control transformation/analysis steps


At a high level, a graphic is created via the following discrete
steps:

0. Ingest a dataset
1. Variables: Define variables from dataset (a variable is like a column in a table)
2. Algebra: defines how the data maps to hierarchical layout of resulting graphic 
3. Scales: Map variables to domains (numerical, ordinal, temporal, log, etc)
4. Statistics: compute statistics over the data
5. Geom: map statistics to generic geometrical objects (data -> pixel space)
6. Position: modify positioning of geometries (e.g., jitter)
6. Coord: transform geometries based on a coordinate system (maps, polar, etc)
7. Aesthetics: add color, texture, and other aesthetic properties
8. Render the graphic (e.g., onto canvas or svg element)


SHOW DEMO

1. Render per hour in one line

        aes: {
          x: "{new Date(time);}", 
          y: "{+count}"
        },
        layers: [
          {geom: "line"}
        ],
        data: '/data/data.csv'

2. Facet by name, vs group by name

        
        facets: { y: "name" }
        color: "name"


3. Render diffs as well

        {geom: 'line', aes: {y: "{+diff}", opacity: 0.2}  }


3. Render it as lat lon, add a label

        {
          aes: {x: "{+lat}", y: "{+lon}", color: "name"},
          layers: [
            {geom: "point" },
            {geom: "text", aes: { text: "name"}}
          ],
          data: '/data/data.csv',
          scales: {
            y: {lim: [-71.11, -71.04]},
            x: {lim: [42.34, 42.38]}
          }
        }

## Polaris

* Data as table of graphics
* Algebra for dictating the tabular layout
* Defines rules for nominal, ordinal, numeric attribute types

What makes an algebra?  Set & operations over the set that satisfy properties e.g., commutivity, etc.

* p-entry: an atom.  (tag:value) pair where
  * tag may be "field", "constant", <name of field>
  * value is a base value for first two tags, or value in the fields domain for latter
* p-tuple: finite sequence of p-entries.  
  * A p-tuple defines a single pane axis values.
  * Sequence because it needs to be rendered in order
* An operand is a finite sequence of p-tuples.  Each tuple is a row/col/layer in the layout



Define Operators

* Add (+): concat two sequences
* Cross (x): cartesian product
* Nest (/): Tricky definition. (filter X product for pairs that actually exsit in the data)
* Dot (.): Hierarchy aware nesting.  (dont use nest because it needs to read values in table, Dot uses provided hierarchy info)


## D3

D3 eschews the components and grammers and provides the lowest common denominator for building visualizations.  Its core provides a single abstraction

* Table JOIN  DOM elements

Recall Relational Algebra is about operations on Sets

* explain how left joins work: table join table
  * [id, a] join [id, el] 

        key, a      JOIN   key, el
        1,  'hi'
        2,  'bye'
    
        returns
    
        key, a,      el
        1,   'hi',  [DOM element]
        2,   'bye', [DOM element]


* What do we need? (ask)
  * model DOM elements as a table
  * what do we join _on_?  (join key?)
  * aesthetic mappings: how to may a tuple's data to a DOM attribute?
  * what are the semantics of this join?
    * show venn diagram
    * enter, update, exit
  * what is the programatic interface?
  * performance implications?  caching.  nice
* Join is the only multi-set operator, nice observation
  * What about right outer join?



Demo! Add scales with domains

    var tmin = d3.min(data, function(d){return d.time})
    var tmax = d3.max(data, function(d){return d.time})
    var time = d3.scale.linear().domain([tmin, tmax]).range([10, 790]);
    var countmax = d3.max(data, function(d){return d.count})
    var y = d3.scale.linear().domain([0, countmax]).range([10, 490])

    .attr('cx', function(d) { return time(d.time) })
    .attr('cy', function(d) { return y(d.count) })

Colors with the points

    var names = _.uniq(_.map(data, function(d){return d.name}));
    var color = d3.scale.category10().domain(names);

    .attr('fill', function(d) { return color(d.name) })

And animation -- what d3 is awesome for

    d3.selectAll('circle').transition()
    .delay(function(d,i){return 1000 + i/(data.length) * 2000})
    .attr('cx', 10)
    .attr('cy', 10)
    .attr('r', 0.5)

    d3.selectAll('circle').transition()
    .delay(function(d,i){return 4000 + i/(data.length) * 2000})
    .attr('cx', function(d) { return time(d.time) })
    .attr('cy', function(d) { return y(d.count) })
    .attr('r', 5)


Now add a line

    var tmin = d3.min(data, function(d){return d.time})
    var tmax = d3.max(data, function(d){return d.time})
    y = d3.scale.linear().domain([0, d3.max(data, function(d){return d.count})]).range([10, 490])
    var time = d3.scale.linear().domain([tmin, tmax]).range([10, 790]);
    var line = d3.svg.line()
    .x(function(d){return time(d.time)})
    .y(function(d){return y(d.count)})
    .interpolate('basis')

    var els = d3.select("#chart").selectAll("path")

    data = d3.nest().key(function(d){ return d.name}).entries(data)
    var color = d3.scale.category10().domain(_.map(data, function(d){return d.key}))
    els.data(data)
    .enter()
    .append('path')
    .attr('d', function(d) { return line(d.values)})
    .style('fill', 'none')
    .style('stroke', function(d){return color(d.key)})


And if rendering lat/lon data
    
    var x = d3.scale.linear().domain([42.34, 42.38]).range([10, 790]);
    var y = d3.scale.linear().domain([-71.11, -71.04]).range([10, 490]);


