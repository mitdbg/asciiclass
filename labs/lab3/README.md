# Lab 3

*Assigned: sometime*

*Due: Sometime (just before class)*

In this lab, you will use various types of tools -- from low-level tools like sed and awk to high-level tools like Data Wrangler -- to perform data parsing and extraction from data encoded into a text file, where each record is a line.  The goal of this lab is simply to gain experience with these tools and compare and contrast their usage.


# Setup

Download the events dataset.  This is a dataset of all events in Boston from May-August 2012.

    wget XXX


# Sed & Awk

Sam goes here

2. use sed/awk to extract out the descriptions of the events, the tags, and the hours
3. what's the most popular 1/2-grams?
4. what are the most popular hours?  for partying?


# Wrangler

Go to the [data wrangler website]().  Load the dataset (web recommend a small subset -- 100~ lines) into data wrangler and try playing with the tool.

Goal:

5. now use wrangler to extract the structured content.  What was easy to do?  What was difficult?
6. dump the structured content into sqlite3 or postgresql
1. run some queries on the extracted text to prove you've done it.


Some tips:

1. Undo tool
1. Export tool

### Questions

1. What does fold/un-fold do?


**Handing in your work**:

Your task is to write a query that XXXX.

You should create a text file with your name, XXX.  Upload it to the [course Stellar site](http://stellar.mit.edu/S/course/6/fa13/6.885/) as the "lab3" assignment.

Now you're almost done!  Go read the assigned paper(s) for today.

You can always feel free to email us with questions at [6885staff@mit.edu](mailto:6885staff@mit.edu).
