# Lab 8: Graph Analytics Using Giraph

*Assigned: Oct 24, 2013*

*Due: Tuesday Oct 31, 2013 12:59PM (just before class)*


The goal of this lab is for you to get experience _running_ graph queries on Giraph, the open-source counterpart to Google's Pregel, and to understand the pros and cons of vertex-centric approach to graph analytics. Check out the [Pregel](http://dl.acm.org/citation.cfm?id=1807167.1807184&coll=DL&dl=ACM&CFID=371018483&CFTOKEN=18422478) paper for more details.

In this lab, you will work with the [LiveJournal dataset](http://snap.stanford.edu/data/soc-LiveJournal1.html), which is a directed friendship graph from the LiveJournal website. You will run the PageRank and the ShortestPath statistics over this dataset.

Each line in the dataset represents an edge of the form `FromNodeId ToNodeId`in the friendship graph. We have put these files on Amazon S3 at: `s3://6885public/livejournal/dataset.txt`


## Setup

You should create a micro-instance as you did in previous labs and ssh into your virtual machine (you can also run these commands from your own machine). Install the following packages.

### Data

You will use `tiny_graph.txt` to test your first Giraph program. It contains the following data:

````bash
[0,0,[[1,1],[3,3]]]
[1,0,[[0,1],[2,2],[3,1]]]
[2,0,[[1,2],[4,4]]]
[3,0,[[0,3],[1,1],[4,4]]]
[4,0,[[3,4],[2,4]]]
````

### Java

Install Java 7:

	sudo apt-get install openjdk-7-jdk
	export JAVA_HOME=/usr/lib/jvm/java-7-openjdk-amd64


### Hadoop

Giraph runs on top of Hadoop/MapReduce. So we need to first setup Hadoop. We will first set up Hadoop in pseudo-distributed mode on a single instance.

	wget http://archive.apache.org/dist/hadoop/core/hadoop-0.20.203.0/	hadoop-0.20.203.0rc1.tar.gz
	tar xzf hadoop-0.20.203.0rc1.tar.gz
	mv hadoop-0.20.203.0 hadoop
	export HADOOP_HOME=~/hadoop

#### Configuring Hadoop

Now we need to configure a bunch of properties.

Set the java home in $HADOOP_HOME/conf/hadoop-env.sh:

	export JAVA_HOME=/usr/lib/jvm/java-7-openjdk-amd64

Add the following in $HADOOP_HOME/conf/core-site.xml. Replace `HOSTNAME` with the name of your instance.

	<property>
	<name>fs.default.name</name>
	<value>hdfs://HOSTNAME:9000</value>
	</property>

Add the following properties in $HADOOP_HOME/conf/mapred-site.xml. Again replace `HOSTNAME` with the name of your instance.

	<property>
	<name>mapred.job.tracker</name>
	<value>HOSTNAME:9001</value>
	</property>
	
	<property>
	<name>mapred.tasktracker.map.tasks.maximum</name>
	<value>4</value>
	</property>
	
	<property>
	<name>mapred.map.tasks</name>
	<value>4</value>
	</property>


Specify a temporary directory location and replication factor in $HADOOP_HOME/conf/hdfs-site.xml. Replication factor is set to 1 in the pseudo-distributed mode.

	<property>
	<name>hadoop.tmp.dir</name>
	<value>/home/ubuntu/hadoopTmpDirectory</value>
	</property>

	<property>
	<name>dfs.replication</name>
	<value>1</value>
	</property>

Finally, you need to setup passphraseless access from the master to the slave node (The same node in this case).

	ssh-keygen -t rsa -P ""
	cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys

Now run Hadoop as follows:
	
	$HADOOP_HOME/bin/hadoop namenode -format
	$HADOOP_HOME/bin/start-dfs.sh 
	$HADOOP_HOME/bin/start-mapred.sh

On successfully starting Hadoop, `jps` should show something like this (ignore the pids):

````bash
11576 SecondaryNameNode
11414 DataNode
11835 TaskTracker
11261 NameNode
11878 Jps
11679 JobTracker
````


### Maven

We need Maven to build Giraph. Run the following.

	sudo apt-get install maven

If you see the installer complaining about `libwagon2-java` then run the folloowing and then try installing maven again.
	
	sudo dpkg -i --force-all /var/cache/apt/archives/libwagon2-java_2.2-3+nmu1_all.deb


### Giraph

Deploy Giraph as follows:
	
	wget http://apache.mirrors.pair.com/giraph/giraph-1.0.0/giraph-1.0.0.tar.gz
	tar xzf giraph-1.0.0.tar.gz
	mv giraph-1.0.0 giraph
	cd giraph
	mvn package -DskipTests
	export GIRAPH_HOME=~/giraph


## Running Giraph

#### Shortest Path Query

Upload the sample dataset:

	$HADOOP_HOME/bin/hadoop dfs -copyFromLocal tiny_graph.txt tiny_graph.txt

Run the query:

	$HADOOP_HOME/bin/hadoop jar giraph-examples-1.0.0-for-hadoop-0.20.2-jar-with-dependencies.jar org.apache.giraph.GiraphRunner org.apache.giraph.examples.SimpleShortestPathsVertex -vif org.apache.giraph.io.formats.JsonLongDoubleFloatDoubleVertexInputFormat -vip tiny_graph.txt -of org.apache.giraph.io.formats.IdWithValueTextOutputFormat -op shortestpaths -w 1

Few details about the parameters abive are as follows (for more details run GiraphRunner with `-h` option).  

* -vif	defines the vertex input format
* -vip	provides the path of the vertex input file
* -of defines the output format
* -op provides the output path
* -w tells the number of workers (should be at most 1 less than the maximum number of map tasks)


#### PageRank Query

Now implement the PageRank query using Giraph. You will need to write the `compute` function. For reference, you can have a look at the example PageRank implementation in Giraph [here](https://github.com/apache/giraph/blob/release-1.0/giraph-examples/src/main/java/org/apache/giraph/examples/SimplePageRankVertex.java). 

You will run PageRank on the LiveJournal dataset, which is not in the JSON format (as the tiny_graph.txt). You can handle this in either of two ways:

1. Pre-process the data file and convert it into the JSON format, or
2. Modify the vertex/edge input format to parse the input data accordingly.


#### Fully Distributed Mode

Launch 10 instances on ec2 and install/configure Hadoop on all of them. Re-run the PageRank query on 10 instances.

### Questions

* List the vertex ids of the top 10 PageRanks.
* How did you handle the LiveJournal input file?
* Compare the PageRank implementation in Giraph with the PageRank implementation in:
	* Hadoop
	* Spark
* What are the pros and cons of vertex-centric computation model?


# Submission Instructions


Answer the questions above in a text file called "lab8-lastname", where lastname is your last name.  Make sure the text file also has your complete name.   Save your writeup and scripts in a zip file or tarball.   Upload it to the [course Stellar site](http://stellar.mit.edu/S/course/6/fa13/6.885/) as the "lab8" assignment.

Now you're almost done!  Go read the assigned paper(s) for today.

You can always feel free to contact us with questions on [Piazza](https://piazza.com/class/hl6u4m7ft8n373).

### Feedback (optional, but valuable)

If you have any comments about this lab, or any thoughts about the
class so far, we would greatly appreciate them.  Your comments will
be strictly used to improve the rest of the labs and classes and have
no impact on your grade. 

Some questions that would be helpful:

* Is the lab too difficult or too easy or too boring?  
* Did you look forward to any exercise that the lab did not cover?
* Which parts of the lab were interesting or valuable towards understanding the material?
* How is the pace of the course so far?
