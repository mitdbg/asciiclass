# Lab 1

*Assigned: September 5, 2013*

*Due: September 10, 2013, 12:59 PM (just before class)*

*Updated September 6 to specify that you need to modify the default security group

The goal of this lab is for you to set up Amazon Web Services ("Amazon
Cloud").

Many of the labs in this class will use Amazon's cloud computing
infrastructure.  Using a cloud service like Amazon makes it easy to
share data sets, and quickly run any number of virtual machines that are
identical for all students in the class.  We have credits from Amazon,
which we will use for later labs (in this lab, we will use a free
"micro" instance.)

### Sign up and setup the OS

**Signup**: [register for an account](https://aws-portal.amazon.com/gp/aws/developer/registration/index.html)

You will need to provide a credit card, however the class has Amazon credits so
you should not expect to _use_ the credit card even if you exhaust the free usage tier.  
Once the class registration has settled down, we can provide you with an account to utilize the class' Amazon credits instead. 
[[ old: Once the class registration has settled down, we will add you to the class's Amazon groups. ]]

If you're worried about being billed unexpectedly because you left a server or service running for too long, sign up for [billing alerts](https://portal.aws.amazon.com/gp/aws/developer/account?ie=UTF8&action=billing-alerts&sc_icampaign=welcome_email_2&sc_icontent=billing_alerts_link&sc_iplace=welcome_email_2&sc_idetail=aws_resources).

**Launch an instance**

1. Go to [http://aws.amazon.com](http://aws.amazon.com) and click 'AWS Management Console' under 'My Account/Console' 
in the upper right.  
1. Click EC2
1. Click Launch Instance.  (You can optionally change the region you're in from 'Oregon' to 'Virginia' in the top right, which might get you lower latency to your server.)
1. Use the "Classic Wizard". As of this writing the "Quick Launch Wizard" would not successfully launch.
1. Select the 64-bit version of "Ubuntu Server 13.04."
1. Specify 1 instance of type "t1.micro". During the first year, Amazon does not charge for the first 750 hours of micro-instance usage (per month), so this won't cost you anything to launch.
1. You don't care about the subnet, and can simply click "Continue" on the "Advanced Instance Options", "Storage Device Configuration", and "Add Tags" pages.
1. You will need to specify a key pair, or create a new one.  If you choose to create a new one, make sure you download it and save it (your file extension should be `.pem`).
1. The default security group is fine (you will need to enable ssh access to it below)
1. Click "Launch".  It will take a few minutes for the instance to launch.  Close the dialog, and wait on the instance listing table.
1. After the instances launches, click on it to obtain its "Public DNS" name.  It should look something like ec2-xx-xxx-xx-xxx.us-REGION-2.compute.amazonaws.com

**Enable SSH Access**: 

Before you can ssh to your instance, you need to enable ssh access for it.  To do this:

1. Go the [EC2 Console](https://console.aws.amazon.com/ec2/v2/home?region=us-west-2)
1. Click on "Security Groups" under "Network & Security" in the leftmost panel.   
1. Click the checkbox next to the "default" security group
1. Click on the "inbound" tab
1. Choose "SSH" from the "Create a new rule:" menu
1. Enter 0.0.0.0/0 to enable access from all IPs, or enter the IP address of your machine followed by "/32". (e.g., 192.168.1.10/32) to enable access from just your IP.

(This will enable ssh access to allow VMs in the default security group, so you shouldn't need to do this in the future.)

**SSH to Your Instance**: 

Using a terminal program (e.g, MacOS Terminal, or an xterm on Athena, or a Cygwin terminal under windows), type:

    ssh -i <PEM FILE> ubuntu@<public address>

Where <PEM FILE> is key file you downloaded when launching the instance.

You may get an error about the permissions of your PEM file.  If so, type:

    chmod 400 <PEM FILE>

and then try to ssh again.

**Setup the OS**: ensure the following packages are available using the Ubuntu package management tool _apt-get_.  

To install a package, type:

    sudo apt-get install <packagename>

Make sure you have the following packages:

* python2.7
  * python-psycopg2
  * python-sqlalchemy
* python-protobuf
* postgresql-9.1
* postgresql-client-9.1
* sqlite3
* git
* mongodb



**Checkout the class repository**

The class repository is publicly accessibly, and contains a `labs`
directory that contains all of your labs.  Clone it using git into a
directory called `asciiclass`.

    git clone https://github.com/mitdbg/asciiclass.git

**Test that things worked**

Let's make sure you have access to Python, sqlite3, MongoDB, and the git repository.

**Python**: Type `python` and ensure that you see the following:

    Python 2.7.4 (default, Apr 19 2013, 18:28:01) 
    [GCC 4.7.3] on linux2
    Type "help", "copyright", "credits" or "license" for more information.
    >>> 

If you do, push `ctrl+d` to exit the prompt.

**sqlite3**: 

SQLite is an "embedded" SQL database (it doesn't depend on a dedicated server process;  instead the client just manipulated a stored
datbase file directly.)

To ensure it is installed, type `sqlite3` and verify that you see the following:

    SQLite version 3.7.15.2 2013-01-09 11:53:05
    Enter ".help" for instructions
    Enter SQL statements terminated with a ";"
    sqlite>

If you do, push `ctrl+d` to exit the prompt.

**MongoDB**:

MongoDB is a "document database" that stores and queries collections
of JSON-like documents.  Spend a bit of time familiarizing yourself
with its features by browsing [the MongoDB
website](http://www.mongodb.org).

To ensure that you have it installed correctly, `mongo` and verify that you see the following:

    MongoDB shell version: 2.2.4
    connecting to: test
    > 

If you do, push `ctrl+d` to exit the prompt.

When running mongo, you may see an error like this:

    Thu Sep  5 01:22:46 Error: couldn't connect to server 127.0.0.1 shell/mongo.js:84
    exception: connect failed

Try running:

    sudo rm /var/lib/mongodb/mongod.lock
    sudo -u mongodb mongod -f /etc/mongodb.conf --repair

And then try `mongo` again

**git repository**: Type `cat asciiclass/labs/lab1/README.md`

You should see the instructions for this lab fly by.

**Stop your virtual machine**: 

While the AWS free tier should get you through the class, you only get
750 hours per month of compute time.  That's enough time for one micro
instance machine to run for a month, but later in the semester, we
will be running multiple machines at the same time.  To conserve your
hours (and avoid wasting energy), make sure to turn off your machine
when not using it.  (Don't worry---we've got credits for those of you
with course projects that require burning up compute resources!)

1. Go to the [EC2 Console](https://console.aws.amazon.com/ec2/v2/home?region=us-west-2).
1. In the dashboard on the left, click on "Instances"
1. Click on the checkbox on the left of your running micro instance.
1. In the "Actions" menu at the top, choose "Stop".  This will shut down the instance.  Before doing future labs, you'll have to follow these instructions and choose "Start" to restart your instance.  Note that restarting the instance will potentially change the "Public DNS" value for that instance.

**Handing in your work**:

To complete this lab, download the "zoo.json" file from Amazon into your "micro" instance, by typing:

    curl https://s3.amazonaws.com/6885public/zoo.json > zoo.json

Load it into mongo by typing:

    mongoimport -d test -c animals zoo.json

You should now have a collection called `animals` with several animals of note.  Then start the mongo shell by running `mongo`.

Your task is to write a query that finds the names of the snakes in the zoo.  You will find the [Mongo Find Command Documentation](http://docs.mongodb.org/manual/reference/method/db.collection.find/#db.collection.find) useful.

You should create a text file with your name, the MongoDB expression your wrote to do this, and its output.  Upload it to the [course Stellar site](http://stellar.mit.edu/S/course/6/fa13/6.885/) as the "lab1" assignment.

Now you're almost done!  Go read the assigned paper(s) for today.

You can always feel free to email us with questions at [6885staff@mit.edu](mailto:6885staff@mit.edu).
