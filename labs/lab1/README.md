# Lab 1

The goal of this lab is for you to set up Amazon Web Services ("Amazon
Cloud") 

# Step 1: Setup Amazon EC2

Many of the labs in this class will use Amazon's cloud computing infrastructure.
Using a cloud service like Amazon makes it easy to share data sets, and quickly run any number virtual machines that 
are identical for all students in the class.
We have credits from Amazon, which we will use for later labs (in this lab, we will use a free "micro" instance.)

### Sign up and setup the OS

**Signup**: [register for an account](https://aws-portal.amazon.com/gp/aws/developer/registration/index.html)

You will need to provide a credit card, however the class has Amazon credits so
you should not expect to _use_ the credit card.  Once the class registration has 
settled down, we will add you to the class's Amazon groups.

**Launch an instance**

1. Go to [http://aws.amazon.com](http://aws.amazon.com) and click 'AWS Management Console' under 'My Account/Console' 
in the upper right.  
1. Click EC2
1. Click Launch Instance.  
1. Use the "Classic Wizard". As of this writing the "Quick Launch Wizard" would not successfully launch.
1. Select one of the Ubuntu Server images ("AMIs"); it doesn't matter exactly which one for this lab.
1. Specify 1 instance of type "t1.micro". Amazon lets you launch one micro-instance for free, so this won't cost you anything to launch.  
1. You don't care about the subnet, and can simply click "Continue" on the "Advanced Instance Options", "Storage Device Configuration", and "Add Tags" pages.
1. You will need to specify a key value pair, or create a new one.  If you choose to create a new one, make sure you download it and save it (your should have a .pem file).
1. The default security group is fine.
1. Click "Launch".  It will take a few minutes for the instance to launch.
1. After the instances launches, click on it to obtain its DNS name.  It should look something like ec2-xx-xxx-xx-xxx.us-west-2.compute.amazonaws.com

**SSH to Your Instance**: 

Type something like:

    ssh -i <PEM FILE> ubuntu@<public address>

Where <PEM FILE> is key file you downloaded when launching the instance.

**Setup the OS**: ensure the following packages are available using the Ubuntu package management tool apt-get.  

To install a package, type:

    sudo apt-get install <packagename>

Make sure you have the following packages:

* python2.7
  * python-psycopg2
  * python-sqlalchemy
* python-protobuf
* postgresql
* sqlite3
* git
* mongodb

Checkout the class repository

    git clone https://github.com/mitdbg/asciiclass.git

xxx this gives me the error:
Warning: Permanently added 'github.com,192.30.252.130' (RSA) to the list of known hosts.
Permission denied (publickey).
fatal: The remote end hung up unexpectedly