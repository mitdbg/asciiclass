# Lab 5: Hadoop/Elastic-Map-Reduce

*Assigned: Oct 1, 2013*

*Due: Thursday Oct 3, 2013 12:59PM (just before class)*

The goal of this lab is for you to get experience _running_ Hadoop/MapReduce jobs on AWS, both to understand
the pros and cons of using Hadoop, and as a setup for the next series of labs.  

In this lab, you will work with the [enron email corpus](http://www.cs.cmu.edu/~enron/), which contains the email contents of all high level employees during the [Enron fiasco](http://en.wikipedia.org/wiki/Enron_scandal).  You will compute simple and _slightly more_ complicated statistics.

A sample of the data is below:

````json
{"bccnames": [], "sender": "phillip.allen@enron.com", "tonames": [""], "cc": [], "text": "Here is our forecast\n\n ", "recipients": ["tim.belden@enron.com"], "mid": "18782981.1075855378110.JavaMail.evans@thyme", "ctype": "text/plain; charset=us-ascii", "bcc": [], "to": ["tim.belden@enron.com"], "replyto": null, "names": [], "ccnames": [], "date": "2001-05-14 16:39:00-07:00", "folder": "_sent_mail", "sendername": "", "subject":     ""}    
{"bccnames": [], "sender": "phillip.allen@enron.com", "tonames": [""], "cc": [], "text": "Traveling to have a business meeting takes the fun out of the trip.  ...", "recipients": ["john.lavorato@enron.com"], "mid": "15464986.1075855378456.JavaMail.evans@thyme", "ctype": "text/plain; charset=us-ascii", "bcc": [], "to": ["john.lavorato@enron.com"], "replyto": null, "names": [], "ccnames": [], "date": "2001-05-04 13:51:00-07:00", "folder": "_sent_mail", "sendername": "", "subject": "Re:"}
````

The dataset is stored as a set of files, where each file contains all emails sent by one person.  We have put these files on Amazon S3 at: `s3://6885public/enron/*.json`

## Setup

### Data



[Download](https://s3.amazonaws.com/asciiclass/enron/lay-k.json.gz) and decompress `lay-k.json.gz`, which you will use to test your first mapreduce program:

````bash
gzip -d lay-k.json.gz
````

### Python

You will need to install the following packages:

````bash
pip install mrjob
pip install awscli
````    
    
[mrjob](http://pythonhosted.org/mrjob/) makes managing and deploying map reduce jobs from Python easy.

[awscli](https://aws.amazon.com/cli/) provides convenient command line tools for managing AWS services (e.g., copying data to and from S3)

    aws s3 cp <local file> s3://<YOUR BUCKET NAME>/
    

### Amazon

[Go to this website](https://6885.signin.aws.amazon.com/console) and login with the username `6885student` to create your own access key (we will give you the password on Piazza and in class).  Then navigate to the [IAM service](https://console.aws.amazon.com/iam/home?#users) and create a new access key for yourself.  You will need this to interact with AWS.

(We are going to let everyone use the same AWS account and see well that works!)

#### Setup for awscli

First [for awscli](http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html) by creating a config file containing the following (the region=us-west-2 is important)

    [default]
    aws_access_key_id = <your key>
    aws_secret_access_key = <your secret>
    region = us-west-2    


Now point the environment variable to it:

    export AWS_CONFIG_FILE=<location of config file>

Now using `awscli` should just work.  Try to list your buckets:

    aws s3 ls

#### Setup for mrjob

Second, [setup for mrjob](http://pythonhosted.org/mrjob/guides/emr-quickstart.html#amazon-setup) by setting:

    export AWS_ACCESS_KEY_ID=<your access key>
    export AWS_SECRET_ACCESS_KEY=<your secret>


## Running MapReduce locally

Before running a job on multiple servers, it's useful to debug your map reduce job locally (on your own machine, not AWS).

`mr_wordcount.py` contains the following code to count the number of times each term (word) appears
in the email corpus:

````python
import sys
from mrjob.protocol import JSONValueProtocol
from mrjob.job import MRJob
from term_tools import get_terms

class MRWordCount(MRJob):
    INPUT_PROTOCOL = JSONValueProtocol
    OUTPUT_PROTOCOL = JSONValueProtocol

    def mapper(self, key, email):
        for term in get_terms(email['text']):
            yield term, 1

    def reducer(self, term, occurrences):
        yield None, {'term': term, 'count': sum(occurrences)}

if __name__ == '__main__':
    MRWordCount.run()
````


OK now run this locally on `lay-k.json`
            
````bash
python mr_wordcount.py -o 'wordcount_test' --no-output './lay-k.json'
````

The output should be in `wordcount_test/` and should look like:

````json
{"count": 33, "term": "aapl"}
{"count": 2, "term": "aarhus"}
{"count": 8, "term": "aaron"}
{"count": 1, "term": "aarp"}
{"count": 1, "term": "ab-initio"}
{"count": 20, "term": "abandon"}
````

<div style="text-align: center; color: red; font-size: 15pt;">
Be cool, test locally before deploying globally (on AWS)!
</div>


## Running on EMR

<div style="width: 80%; margin-left: auto; margin-right: auto;">
<h3>An important note</h3>
 
We will provide a job pool on AWS (the VMs are spun up and loaded) for you to run on.   <b>Please use the pool and don't allocate machines on your own!</b>  

The reasons are so that

<ol>
<li>We can control the cost of running this lab (very important!) and
<li>You don't need to incur the cost of allocating, starting and shutting down the machines for each job.
</ol>

The downside is if you run your job at the same time as the other students (e.g., on the last day) you will have fewer resources.  This is called _resource sharing_ and is a nice lesson to learn!
</div>

Now let's run the same script on the same file on EC2 (`s3://6885public/enron/lay-k.json`):

````bash
python mr_wordcount.py  \
  --num-ec2-instances=1 \
  --emr-job-flow-id=classpool \
  --python-archive package.tar.gz \
  -r emr \
  -o 's3://asciiclass-YOURUSERNAME-testbucket/output' \
  --no-output \
  's3://6885public/enron/lay-k.json'
````      

Some details about executing this:

* `--num-ec2-instances` specifies the number of machines.  Please use less than 20 machines
* `--emr-job-flow-id` is the name of our job pool.  We named it "classpool".  **Always use this job id**
* `--python-archive` contains the python files and packages that your job includes
* Replace `YOURUSERNAME` with a unique name.  AWS will automatically create the bucket.
* `--no-output` suppresses outputs to STDOUT

Go to your bucket and download the output to check if the results are sane.  If so, it's probably safe to change the inputs to `s3://6885public/enron/*.json` and run again.



## Your Task: TF-IDF

The goal of this section is to perform TF-IDF ("Term Frequency / Inter-Document Frequency") for each sender in the corpus.
You can read about [TF-IDF on Wikipedia](http://en.wikipedia.org/wiki/Tf%E2%80%93idf).    Wikipedia describes it as:
 
    a numerical statistic which reflects how important 
    a word is to a document in a collection or corpus.

In Wikipedia's lingo, a "document" is all text in a sender's emails, and the "collection or corpus" is the set of all emails in the corpus. 

To make things easy, the total number of emails is `516893`.

You will probably want to

1. Compute per-term IDFs
2. Join that with each sender's IDFs


Once again, please test locally before running globally!


### Questions

* List the top TF-IDF terms for Enron's key people: 
    * Kenneth Lay, Founder, Chairman and CEO
    * Jeffrey Skilling, former President, and COO
    * Andrew Fastow, former CFO
    * Rebecca Mark-Jusbasche, former Vice Chairman, Chairman and CEO of Enron International
    * Stephen F. Cooper, Interim CEO and CRO
* How did you compute TF-IDF on the whole corpus?  What was easy, what was hard?


The `from` and `to,cc,bcc` fields in each email define directed edges (from --> to) between 
each person (node).  These edges form a graph.  

* Sketch a description of how you would use EMR to run [page rank](http://en.wikipedia.org/wiki/Page_rank) on this graph.  What would be some pain points?

Bonus question (optional):

* Cluster the senders by their TF-IDF vectors in whatever way you want.  Describe the clusters.  Who's close to whom?



# Submission Instructions


Answer the questions above in a text file called "lab5-lastname", where lastname is your last name.  Make sure the text file also has your complete name.   Save your writeup and scripts in a zip file or tarball.   Upload it to the [course Stellar site](http://stellar.mit.edu/S/course/6/fa13/6.885/) as the "lab5" assignment.

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
