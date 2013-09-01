# Instructions for Lab 1

The goal of this lab is for you to set up  amazon/cloud  experience the pain of working
with data in various degrees of structure.  

You will the same tweet dataset encoded in multiple ways to compute
some summary information and reflect on the pros and cons of each
encoding.  


# Step 0: Setup Amazon EC2

Many of the labs in this class will involve running on cloud computing infrastructure.
so we ask that you to run the labs an such an infrastructure from the very beginning.  
The class has recieved Amazon credits so the instructions will be written towards their
services.

If you would like to use another cloud infrastructure, feel free
to do so but you're on your own!

## Sign up and setup the OS

**Signup**: sign up at https://aws-portal.amazon.com/gp/aws/developer/registration/index.html

You will need to provide a credit card, however the class has amazon credits so
you should not expect to _use_ the credit card.  Once the class registration has 
settled down, we will add you to the class amazon groups.

**Launch an instance**

1. Go to http://aws.amazon.com and click 'AWS Management Console' under 'My Account/Console' 
in the upper right.  
1. Click EC2
1. Click Launch Instance.  Amazon lets you launch one micro-instance for free, so we strongly recommend 
   that you do this.
1. Use one of the Ubuntu Server images (doesn't matter exactly which one for this lab)
1. Check its public address.  It should look something like ec2-xx-xxx-xx-xxx.us-west-2.compute.amazonaws.com

**Download your keys**: you need to download a pem file in order to ssh to your instance.
Download it and ssh:

    ssh -i <PEM FILE> ubuntu@<public address>

**Setup the OS**: ensure the following packages are available using apt-get.  

* python 2.7
  * psycopg2
* protocol buffers
* postgresql
* sqlite3
* git

Checkout the class repository

    git clone git@github.com:sirrice/asciiclass.git

Go to lab 1:

    cd asciiclass/labs/lab1


# Step 1: Joins on JSON

Use twitter.data for this step.  twitter.data contains a json-encoded tweet
on each line.


# Step 2: Joins on Protocol Buffers

Protocol Buffers are

# Step 3: Joins on databaes records

Download the following sqlite3 database that is already loaded with data.

Start sqlite using

    sqlite3 <filename>

This should land you in the prompt.  Now compute 

URL to SQLITE documentation and Postgresql documentation.

# Questions

