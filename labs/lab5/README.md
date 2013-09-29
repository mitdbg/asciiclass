# Lab 5: Hadoop/Elastic-Map-Reduce

*Assigned: XXX*

*Due: XXX (just before class)*

The goal of this lab is for you to get experience _running_ hadoop jobs on the cloud, both to understand
the pros and cons of using Hadoop, and as a setup for the next series of labs.  

You will take the full [enron email corpus](http://www.cs.cmu.edu/~enron/), which contains the email contents of all high level employees during the [Enron fiasco](http://en.wikipedia.org/wiki/Enron_scandal).  You will compute simple and _slightly more_ complicated statistics.

A sample of the data is below:

````json
{"bccnames": [], "sender": "phillip.allen@enron.com", "tonames": [""], "cc": [], "text": "Here is our forecast\n\n ", "recipients": ["tim.belden@enron.com"], "mid": "18782981.1075855378110.JavaMail.evans@thyme", "ctype": "text/plain; charset=us-ascii", "bcc": [], "to": ["tim.belden@enron.com"], "replyto": null, "names": [], "ccnames": [], "date": "2001-05-14 16:39:00-07:00", "folder": "_sent_mail", "sendername": "", "subject":     ""}    
{"bccnames": [], "sender": "phillip.allen@enron.com", "tonames": [""], "cc": [], "text": "Traveling to have a business meeting takes the fun out of the trip.  ...", "recipients": ["john.lavorato@enron.com"], "mid": "15464986.1075855378456.JavaMail.evans@thyme", "ctype": "text/plain; charset=us-ascii", "bcc": [], "to": ["john.lavorato@enron.com"], "replyto": null, "names": [], "ccnames": [], "date": "2001-05-04 13:51:00-07:00", "folder": "_sent_mail", "sendername": "", "subject": "Re:"}
````

The dataset is stored as a set of files, where each file is contains all emails sent by one person.  They are sitting on amazon S3 at: `s3://asciiclass/enron/*.json`

## Setup

### Data

Decompress `lay-k.json.gz`:

````bash
gzip -d lay-k.json.gz
````

### Python

You will need to install the following packages:

````bash
pip install mrjob
````    
    
[mrjob](http://pythonhosted.org/mrjob/) makes managing and deploying map reduce jobs from Python easy.

### Amazon

Go to this website to get a class-only AWS account.

Setup your environment:

    export AWS_ACCESS_KEY_ID='your_key_id'
    export AWS_SECRET_ACCESS_KEY='your_access_id'
    

## Running MapReduce locally

`mr_wordcount.py` contains the following code to count the number of times each term (word) appreas
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

The downside is if you run your job at the same time as the other students (e.g., on the last day) you will have less resources.  This is caled _resource sharing_ as is a nice lesson to learn.
</div>



Now let's run the same script on the same file on EC2 (`s3://XXX/lay-k.json`):

````bash
python mr_wordcount.py  --num-ec2-instances=1 \
  --emr-job-flow-id=XXX \
  --python-archive package.tar.gz \
  -r emr \
  -o 's3://dataiap-YOURUSERNAME-testbucket/output' \
  --no-output \
  's3://asciiclass/enron/lay-k.json'
````      

Go to your bucket and download the output to check if the results are sane.  If so, change the inputs to
`s3://asciiclass/enron/*.json` and run again.      

Some details about executing this:

* Please use less than 20 machines
* Always use the class's job id
* `--python-archive` contains the python files and packages that your job includes
* `--no-output` supresses outputs to STDOUT


## Your Task: TF-IDF

You can read about [TF-IDF on Wikipedia](http://en.wikipedia.org/wiki/Tf%E2%80%93idf).  We want you to compute TF-IDF for each sender in the corpus.  Wikipedia describes it as 
    
    a numerical statistic which reflects how important 
    a word is to a document in a collection or corpus.

In wikipedia's lingo, a "document" is all text in a sender's emails, and the "collection or corpus" is the set of all emails in the corpus. 

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
