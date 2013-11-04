The following directions will compile the example in src/test/

    javac -cp lib/giraph.jar:lib/hadoop-core.jar src/test/*.java -d ./ 
    cp lib/giraph.jar giraph.jar
    # add the compiled class file to giraph.jar
    jar uf giraph.jar test/*.class


You should now be able to run this using (assuming tiny_graph.txt is on HDFS)

    hadoop jar giraph.jar  org.apache.giraph.GiraphRunner \
     test.SimpleShortestPathsVertex    \
     -vif org.apache.giraph.io.formats.JsonLongDoubleFloatDoubleVertexInputFormat \
     -vip tiny_graph.txt  \
     -of org.apache.giraph.io.formats.IdWithValueTextOutputFormat   \
     -op shortestpathsOutput  \
     -w 1

To run it on the livejournal dataset (assuming the sampled dataset
 livesmall.txt is on HDFS)

    hadoop jar giraph.jar  org.apache.giraph.GiraphRunner \
     test.LiveJournalShortestPaths  \
     -eif org.apache.giraph.io.formats.IntNullTextEdgeInputFormat \
     -eip livesmall.txt  \
     -of org.apache.giraph.io.formats.IdWithValueTextOutputFormat \
     -op shortestpathsOutput  \
     -w 
