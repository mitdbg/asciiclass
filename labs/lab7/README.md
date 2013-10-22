# Lab 7: Graph Analytics Using Giraph

*Assigned: Oct 24, 2013*

*Due: Tuesday Oct 31, 2013 12:59PM (just before class)*


The goal of this lab is for you to get experience _running_ graph queries on Giraph, the open-source counterpart 
to Google's Pregel, and to understand the pros and cons of vertex-centric approach to graph analytics. 
Check out the [Pregel](http://dl.acm.org/citation.cfm?id=1807167.1807184&coll=DL&dl=ACM&CFID=371018483&CFTOKEN=18422478)
paper for more details.

In this lab, you will work with the [LiveJournal dataset](http://snap.stanford.edu/data/soc-LiveJournal1.html), 
which is a directed friendship graph from the LiveJournal website. You will run the PageRank and the ShortestPath statistics over this dataset.

Each line in the dataset represents an edge of the form `FromNodeId ToNodeId`in the friendship graph. 
We have put these files on Amazon S3 at: `s3://6885public/livejournal/dataset.txt`


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

where each line is in JSON format as

	[vertexid, vertexvalue, [ [vertexid, edgeweight], ...] ]


### Start an Instance

You will need Giraph and Hadoop to run this lab.  Installing them is a pain, so we've created AMI images that you
can copy and use with minimal tweaks.  First, create an instance:

	aws ec2 run-instances --image-id <IMAGE_ID> --count 1 --instance-type m1.small --key-name <your key pair from lab6> --region <your region name from lab6>

`--key-name` from lab6 would be `sparklab-yourusername`.  You can go to "Key Pairs" in the aws console to check.

Depending on your region, the IMAGE_ID is 

* `ami-aee4d3eb` for us-west-1 
* `ami-a463fa94` for us-west-2 
* `ami-995d01f0` for us-east-1

Make sure that your Amazon credentials are set up as in lab 6 or the `AWS_CONFIG_FILE` environment variable is set as in lab 5. It might take a few minutes to get the instance running. You can check the instance by logging in to [this link](https://6885.signin.aws.amazon.com/console) as in lab 6. Alternatively, you can use the ec2 tools as follows:

	aws ec2 describe-instances --instance-ids <INSTANCE_ID>

Note the public DNS name of the newly launched instance and ssh into it. 

	ssh -i <your keypair .pem file> ubuntu@<public hostname>  
		
You will find the precompiled Giraph binaries in `~/giraph-1.0.0`.  Hadoop is in `~/hadoop/`.  The datasets are in `~/`.
Remember to terminate your instance once you are done as follows:

	aws ec2 terminate-instances --instance-ids <INSTANCE_ID>

<!--
### Set up Hadoop

Giraph runs on top of Hadoop/MapReduce. To run it we first need to setup Hadoop. We will first set up Hadoop in pseudo-distributed mode on a single instance.

	wget http://archive.apache.org/dist/hadoop/core/hadoop-0.20.2/hadoop-0.20.2.tar.gz
	tar xzf hadoop-0.20.2.tar.gz
	mv hadoop-0.20.2 hadoop
	export HADOOP_HOME=~/hadoop
-->

#### Configuring Hadoop

<!--
Now we need to configure a bunch of properties.


First install Java 7:

	sudo apt-get update
	sudo apt-get install openjdk-7-jdk
	export JAVA_HOME=/usr/lib/jvm/java-7-openjdk-amd64


Set the java home in $HADOOP_HOME/conf/hadoop-env.sh:

	export JAVA_HOME=/usr/lib/jvm/java-7-openjdk-amd64

-->

You need to tell this Hadoop instance where it is, and setup password-less SSH so Hadoop can log into the nodes without
typing in a password.

Update `$HADOOP_HOME/conf/core-site.xml`. Replace `HOSTNAME` with the name (ec2-X-X-X-X.compute-..com) 
of your instance.

	<property>
	<name>fs.default.name</name>
	<value>hdfs://HOSTNAME:9000</value>
	</property>

Update `$HADOOP_HOME/conf/mapred-site.xml` similarly -- replace `HOSTNAME` with the name of your instance.

	<property>
	<name>mapred.job.tracker</name>
	<value>HOSTNAME:9001</value>
	</property>

<!--	
Now specify a temporary directory location and replication factor in $HADOOP_HOME/conf/hdfs-site.xml. 
Since we are running in "pseudo-distributed mode", we just set the replication factor to 1.

	<property>
	<name>hadoop.tmp.dir</name>
	<value>/home/ubuntu/hadoopTmpDirectory</value>
	</property>

	<property>
	<name>dfs.replication</name>
	<value>1</value>
	</property>
-->

Finally, we need to setup passphrase-less access from the master to the slave node (The same node in this case).

	rm ~/.ssh/known_hosts
	rm ~/.ssh/id_rsa*
	ssh-keygen -t rsa -P ""
	cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys

_Finally_, you can run Hadoop:
	
	$HADOOP_HOME/bin/start-all.sh
	
<!--	
	$HADOOP_HOME/bin/hadoop namenode -format
	$HADOOP_HOME/bin/start-dfs.sh 
	$HADOOP_HOME/bin/start-mapred.sh
-->

On successfully starting Hadoop, `jps` should show something like this (ignore the pids):

````bash
11576 SecondaryNameNode
11414 DataNode
11835 TaskTracker
11261 NameNode
11878 Jps
11679 JobTracker
````


#### Testing HDFS

Let's make sure HDFS works and has our `tiny_graph.txt` dataset

List files in HDFS

	$HADOOP_HOME/bin/hadoop dfs -ls
	
You should see a few files: `live.txt, tiny_graph.txt, ...`.  The first one is the livejournal dataset that
we pre-loaded into HDFS.  The second `tiny_graph.txt` has size zero, so let's re-upload it again.

Delete the file

	$HADOOP_HOME/bin/hadoop dfs -rm tiny_graph.txt

Copy it back in
	
	$HADOOP_HOME/bin/hadoop dfs -rm tiny_graph.txt

Now if you `-ls`, you should see that the file is not empty.

#### Creating a Cluster

Now you can spin up (between 1 - 7) instances and configure them.  Record their hostnames.

In order to add them to a cluster, pick one of your instances as the master and add the hostnames
to `~/hadoop/conf/slaves`.  One hostname per line.

Test this by

1. Stop Hadoop on all of the instances: `$HADOOP_HOME/bin/stop-all.sh`
2. Start hadoop on your master: `$HADOOP_HOME/bin/start-all.sh`
3. ssh to a slave and run: `jps`.  TaskTracker and DataNode should be running.

HDFS may be read-only for ~5 minutes while files are replicated.  Until then, you may get a
"Name node is in safe mode." error.



Hurray!


<!--
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
	mvn package -DskipTests -Phadoop_non_secure 0.20.2	
	export GIRAPH_HOME=~/giraph
-->

## Running Giraph

#### Compile a program



#### Shortest Path Query

Run the query:

	$HADOOP_HOME/bin/hadoop jar \
	  ~/giraph-1.0.0/giraph-examples/target/giraph-examples-1.0.0-for-hadoop-0.20.2-jar-with-dependencies.jar \
	  org.apache.giraph.GiraphRunner\
	  org.apache.giraph.examples.SimpleShortestPathsVertex \
	  -vif org.apache.giraph.io.formats.JsonLongDoubleFloatDoubleVertexInputFormat\
	  -vip tiny_graph.txt \
	  -of org.apache.giraph.io.formats.IdWithValueTextOutputFormat \
	  -op shortestpathsOutput \
	  -w 1
	  
The output files are in

	$HADOOP_HOME/bin/hadoop dfs -ls shortestpathsOutput/

We briefly describe the parameters above below;  for more details run GiraphRunner with the `-h` option:

* -vif	defines the vertex input format.  `JsonLongDoubleFloatDoubleVertexInputFormat` parses the input file format.
* -vip	provides the path of the vertex input file
* -of defines the output format
* -op provides the output path
* -w tells the number of workers (should be at most 1 less than the maximum number of map tasks)

For example code, look in the `~/giraph-1.0.0/giraph-examples/src/main/java/org/apache/giraph/examples` directory.

#### PageRank Query

Now implement  PageRank using Giraph. You will need to write the `compute` function. 
For reference, you can have a look at the example PageRank implementation in 
Giraph [here](https://github.com/apache/giraph/blob/release-1.0/giraph-examples/src/main/java/org/apache/giraph/examples/SimplePageRankVertex.java). 

You will run PageRank on the LiveJournal dataset, which is not in the `tiny_graph.txt` format. 
Instead, each line is simply a `startvertexid  endvertexid` pair.  You can handle this in either of two ways:

1. Pre-process the data file and convert it into the JSON format, or
2. Modify the vertex/edge input formats to parse the input data accordingly.


#### Fully Distributed Mode (Optional)

Launch 10 instances on ec2 and install/configure Hadoop on all of them (one way is to create an AMI image of
an instance with hadoop installed and call `aws ec2 run-instances` with that image).  Then you will need to

* Start Hadoop on all of the instances
* Add the slave machines' hostnames (ec2-x-x...amazon.com) to the master node's `~/hadoop/conf/slaves` file. 
  One hostname per line
* On the master node.  Terminate everything (`~/hadoop/bin/stop-all.sh`) and start everything up (`~/hadoop/bin/start-all.sh`).

Sanity check by rerunning on `tiny_graph.txt`

Finally, re-run  PageRank on 10 instances.

### Questions

* List the vertex ids of the top 10 PageRanks.
* How did you handle the LiveJournal input file?
* Qualitatively compare the PageRank implementation in Giraph with the PageRank implementation in:
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
