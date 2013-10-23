# Lab 7: Graph Analytics Using Giraph

*Assigned: Oct 22, 2013*

*Due: Tuesday Oct 31, 2013 12:59PM (just before class)*


The goal of this lab is for you to get experience _running_ graph queries on Giraph, the open-source counterpart 
to Google's Pregel, and to understand the pros and cons of vertex-centric approach to graph analytics. 
Check out the [Pregel](http://dl.acm.org/citation.cfm?id=1807167.1807184&coll=DL&dl=ACM&CFID=371018483&CFTOKEN=18422478)
paper for more details.

## Datasets

In this lab, you will work with the [LiveJournal dataset](http://snap.stanford.edu/data/soc-LiveJournal1.html), 
which is a directed friendship graph from the LiveJournal website. You will run the PageRank and the ShortestPath statistics over this dataset.

Each line in the dataset represents an edge of the form `FromNodeId ToNodeId`in the friendship graph. 


You will also use `tiny_graph.txt` stored as an adjacency list:

````bash
[0,0,[[1,1],[3,3]]]
[1,0,[[0,1],[2,2],[3,1]]]
[2,0,[[1,2],[4,4]]]
[3,0,[[0,3],[1,1],[4,4]]]
[4,0,[[3,4],[2,4]]]
````

where each line is in JSON format as

	[vertexid, vertexvalue, [ [vertexid, edgeweight], ...] ]

Both of these files should be already in the home directory and/or HDFS when you spin up your instances.

## Setup

You should create a micro-instance as you did in previous labs and ssh into your virtual machine (you can also run these commands from your own machine). Install the following packages.


### Start an Instance

You will need Giraph and Hadoop to run this lab.  Installing them is a pain, so we've created AMI images that you
can copy and use with minimal tweaks.  First, create an instance:

	aws ec2 run-instances --image-id <IMAGE_ID> --count 1 --instance-type m1.small --key-name <your key pair from lab6> --region <your region name from lab6>

`--key-name` from lab6 would be `sparklab-yourusername`.  You can go to "Key Pairs" in the aws console to check.

Depending on your region, the IMAGE_ID is 

* `ami-6cedda29` for us-west-1 
* `ami-ea1881da` for us-west-2 
* `ami-6b1d4102` for us-east-1

Make sure that your Amazon credentials are set up as in lab 6 or the `AWS_CONFIG_FILE` environment variable is set as in lab 5. It might take a few minutes to get the instance running. You can check the instance by logging in to [this link](https://6885.signin.aws.amazon.com/console) as in lab 6. Alternatively, you can use the ec2 tools as follows:

	aws ec2 describe-instances --instance-ids <INSTANCE_ID>

Note the public DNS name of the newly launched instance and ssh into it. 

	ssh -i <your keypair .pem file> ubuntu@<public hostname>  
		
You will find the precompiled Giraph binaries in `~/giraph-1.0.0`.  Hadoop is in `~/hadoop/`.  The datasets are in `~/`.

**Remember to terminate your instance once you are done as follows:**

	aws ec2 terminate-instances --instance-ids <INSTANCE_ID>


#### Configuring Hadoop

Setup passphrase-less access from the master to the slave node (The same node in this case).

	# the first two are to remove .ssh stuff from eugene's instance
	rm ~/.ssh/known_hosts 
	rm ~/.ssh/id_rsa*
	# generate a key
	ssh-keygen -t rsa -P ""
	# authorize the key on the machine you want to ssh into
	cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys

Now you can run hadoop!
	
	# PATH should include ~/hadoop/bin
	start-all.sh


On successfully starting Hadoop, running `jps` should show something like this (ignore the pids):

````bash
11576 SecondaryNameNode
11414 DataNode
11835 TaskTracker
11261 NameNode
11878 Jps
11679 JobTracker
````

Note: some commands that you may want to be aware of:	

	# format your HDFS namenode
	hadoop namenode -format

	# start HDFS
	start-dfs.sh

You may also want to tune the number of map tasks by editing `~/hadoop/conf/mapred-site.xml`.


#### Testing HDFS

Let's make sure HDFS works and has our datasets

List files in HDFS

	hadoop dfs -ls
	
You should see a few files (if you don't you'll need to copy them to HFS, which we will do now):

	live.txt
	livesmall.txt
	tiny_graph.txt

These are the full and sampled live journal datasets and the sample graph.  Let's delete and reupload it:

	hadoop dfs -rm tiny_graph.txt
	hadoop dfs -copyFromLocal tiny_graph.txt tiny_graph.txt

Now if you `-ls`, you should see that the file is there again.



## Running Giraph

Let's run something!  We've added a self contained development folder in ~/code 
that contains two sample programs that take two different file formats (tiny_graph and live journal).
This is partly so you don't need to touch the giraph or hadoop codebases and deal with things like Maven.

This code is also in the repository under `lab7/code`.

#### Compile a program

First compile the program

	cd ~/code
    javac -cp lib/giraph.jar:lib/hadoop-core.jar src/test/*.java -d ./ 

The class files should now be in `./test`.  To run the programs, we need to package them up in
a jar that also includes everything Giraph needs:

    cp lib/giraph.jar giraph.jar
    # add the compiled class file to giraph.jar
    jar uf giraph.jar test/*.class

#### Run shortest paths

You should now be able to run shortest paths on `tiny_graph`:

    hadoop jar giraph.jar  org.apache.giraph.GiraphRunner \
     test.SimpleShortestPathsVertex    \
     -vif org.apache.giraph.io.formats.JsonLongDoubleFloatDoubleVertexInputFormat \
     -vip tiny_graph.txt  \
     -of org.apache.giraph.io.formats.IdWithValueTextOutputFormat   \
     -op tinyOutput  \
     -w 1

What are these parameters? (run GiraphRunner with the `-h` option for help)

* `-vif`	defines the vertex input format. See [the source code](https://github.com/apache/giraph/tree/release-1.0/giraph-core/src/main/java/org/apache/giraph/io) for details.
* `-vip`	is the HDFS path for the vertex centric input file
* `-of` the class that defines the output format.  
* `-op` is the HDFS path for the output files
* `-w` tells the number of workers (should be 1 less than the maximum number of map tasks in `mapred-site.xml`)

Setting the `vip` and `vif` parameters is important as we will see when running on the Live Journal dataset:

    hadoop jar giraph.jar  org.apache.giraph.GiraphRunner \
     test.LiveJournalShortestPaths  \
     -eif org.apache.giraph.io.formats.IntNullTextEdgeInputFormat \
     -eip livesmall.txt  \
     -of org.apache.giraph.io.formats.IdWithValueTextOutputFormat \
     -op livesmallOutput  \
     -w 1

We used the `-eif` and `-eip` flags because the dataset is a list of edges rather than vertex centric.
`IntNullTextEdgeInputFormat` knows how to parse files where each line is `[sourceid]  [edgeid]`.

	  
The output files are in

	hadoop dfs -ls tinyOutput/
	hadoop dfs -ls livesmallOutput/	

#### A quick primer on the code


All Giraph programs subclass `org.apache.giraph.graph.Vertex`, which 
is the compute function for a vertex.  The compute structure is basically:

	parse inputs using formattors -> VertexCompute() -> format the output 

`vif`/`eif`/`of` defines the input and output formatting.  The program implements the compute function.

The `Vertex` signature is:

	class Vertex<I extends WritableComparable, V extends Writable, E extends Writable, M extends Writable>

I, V, E, M are respectively serializers for the Vertex id, Vertex data, Edge data (e.g., weight), Message data

Diff the source files to see the differences:

	diff ./src/test/*.java

Looking at the source, the Live Journal data doesn't care about edge weight, so it is a `NullWriter`.  
Take a look at the source for further details.


#### Creating a Cluster

Let's make your existing instance the master and spin up a few more instances (--count flag):

	aws ec2 run-instances --image-id <IMAGE_ID> --count 3 --instance-type m1.small --key-name <your key pair from lab6> --region <your region name from lab6>

Use the same IMAGE\_ID etc as you did when launching the master.

Remember their hostnames (ec2-xx-xx..amazon.com) and instance-IDs. On the master node,
add the hostnames to `~/hadoop/conf/slaves`.  One hostname per line.

Make sure you can passwordless ssh from the master to the slaves by adding the `~/.ssh/id_rsa.pub` value in
each slave's `~/.ssh/authorized_keys` file.

Now run the cluster

1. Start hadoop on your master: `start-all.sh`
2. ssh to a slave and run: `jps`.  TaskTracker and DataNode should be running.

Now update `mapred-site.xml` with the proper number of map tasks.

Note: HDFS may be read-only for ~5 minutes while files are replicated.  Until then, you may get a
"Name node is in safe mode." error when you perform HDFS write operations.

Hurray!


## PageRank Query

Now implement  PageRank using Giraph. You will need to write the `compute` function. 
For reference, you can have a look at the example PageRank implementation in 
Giraph [here](https://github.com/apache/giraph/blob/release-1.0/giraph-examples/src/main/java/org/apache/giraph/examples/SimplePageRankVertex.java). 

Run it on the Live Journal dataset!

**Did we mention that you should terminate your instances when you're done?  (some machines from lab6 were running for 100 hours)**

	aws ec2 terminate-instances --instance-ids <INSTANCE_ID>

### Questions

* List the vertex ids of the top 10 PageRanks.
* How did you handle the LiveJournal input file?
* Compare the PageRank implementation in Giraph with your thought experiments from the previous labs on:
	* Hadoop
	* Spark
* Compare with the previous systems along the usability dimesion.  What would you most likely use in the future?	
* What are the pros and cons of vertex-centric computation model?  Did this even make sense to do?



# Submission Instructions



Answer the questions above in a text file called "lab7-lastname", where lastname is your last name.  Make sure the text file also has your complete name.   Save your writeup and script in a zip file or tarball.   Upload it to the [course Stellar site](http://stellar.mit.edu/S/course/6/fa13/6.885/) as the "lab7" assignment.

Now you're almost done!  Go read the assigned paper(s) for today.

You can always feel free to contact us with questions on [Piazza](https://piazza.com/class/hl6u4m7ft8n373).
