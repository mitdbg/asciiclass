# Graph Frameworks

How do you program in the Pregel model?

* Executes in supersteps
    * vertices run in lock-step (superstep to superstep)
* vertex-centric
    * per-vertex "compute" functions    
    * update vertex state
    * can read or send messages to neighbors
    * read messages from previous super step
    * write messages to next super step
* mutate the graph e.g.,
    * some algorithms want to make supernodes that represent multiple vertices
    * often want to merge vertices (entity resolution) or add/remove edges
    * if searching for a subgraph, may want to replace it with a higher level vertices
* stop criteria (how does Pregel know when to stop?)
    * vertices can vote to stop

### PageRank example

    vertex_compute(messages) 
      sum = sum(messages)
      v = .15 / totalNumVertices + .85 * sum
      this.setValue(v)  // set vertex's state to new pagerank value
      if getSuperStep() < MAX_STEPS
        nedges = this.numOutEdges()
        sendMessageToEdges(v / nedges)
      else
        voteToStop()

Why does the `< MAX_STEPS` line exist?  What happens if a subset of your neighbors decide to stop?  

* This kind of sucks. See GraphLab below for advances


### Running on >1 machines

Pregel needs to store the vertices (and their edges) across multiple machines.  

* Pregel by default places vertices randomly (hash partitioning).  
* GraphLab/subsequent systems talk about smartly placing vertices e.g., by cluster

Most systems assume the whole graph sits in memory

#### How to detect failures?

Naive implementation

* Let's say we have one master and every node sends heartbeats.  
* We can detect failure but how to recover? 
* Could write everything to HDFS on every step and restore on recovery
    * rollback whole cluster to last checkpoint

Some alternatives/optimizations

* Nodes store their messages and replay messages to failed nodes
* Replication


### Stepping Back

So far, we've implied that the Pregel _programming model_ is tied to the mapreduce/hadoop framework.  But they're orthogonal!

What if we implemented in an RDBMS?  What are the tables, what are the queries?

Some Tables

    msgs (src, dst, value)
    edges(src, dst, weight)

How to query?

    for each superstep
      for each node n
        oldmsgs = select * from msgs where dst = n
        newmsgs = select UDF(oldmsgs, n)
        delete from msgs where dst = n
        insert newmsgs into msgs table
        
Does this even make sense?  Some cons (but how many of them are _fundamental_?)

* RDBMSes incur high cost of consistency.  Pregel is more relaxed
* How do we partition?  on src or dst?
* Not optimized for graph queries
* What if we wanted to support losing messages?

What's good about this?

* fault tolerance!
* RDBMses are mature

Graphs on other frameworks

* On RDBMS: Alekh in Sam's group is working on this.  Initial results show it's pretty competitive except against large graphs on Giraph
* On Spark: [GraphX](https://amplab.cs.berkeley.edu/wp-content/uploads/2013/05/grades-graphx_with_fonts.pdf)
* Titan seems to be crossframework


### GraphLab

GraphLab's model gives handles to neighbor's states for a vertex to read

But!! Things run on multiple machines, so what if a neighbor changes its state and I'm reading it?  What are the _consistency guarantees_?

* Graphlab supports multiple consistency levels defined by whether vertices with overlapping neighborhoods can execute in parallel
    * Full: can't share edges or vertices
    * Edge: can overlap neighboring vertices, not edges
    * Vertex: can overlap neighborhoods
* This matters because algorithms like pagerank are robust to these inconsistencies (these types of hill climbing algorithms)

It's still in the air what's the best!!

    

    