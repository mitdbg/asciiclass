# Lab 8: Visualizing Data

*Assigned: Tuesday, Nov 5, 2013*

*Due:  Tuesday, Nov 12, 2013, 12:59PM (just before class)*


The goal of this lab is for you to create a web-based
visualization in [D3](http://d3js.org) and learn something interesting about a local dataset.

The submissions are hosted as a gallery [here](http://www.mit.edu/~eugenewu/submissions/)!

    http://www.mit.edu/~eugenewu/submissions/

Here are some useful documents

* [D3 documentation](https://github.com/mbostock/d3/wiki/API-Reference)
* [mbostock's gallery](https://github.com/mbostock/d3/wiki/API-Reference)
* [D3 Data Join](http://bost.ocks.org/mike/join/)
* [D3 tutorial](http://alignedleft.com/tutorials/d3)


## Datasets

In this lab, you will use a dataset of all taxi cab pickups in Boston proper over the course of one year.

[Download the dataset here](https://s3.amazonaws.com/mitbigdata/datasets/pickups_train.csv.gz)

Here are the first few lines of this file:

    156527,2012-05-07 14:54:00,50 Francis St Boston Ma 02215,-71.107178,42.335685,126488
    156528,2012-05-07 17:26:00,1080 Boylston St Boston Ma 02215,-71.08807,42.347138,126489
    156529,2012-05-07 17:26:00,50 Seaport Ln Boston Ma 02210,-71.041327,42.349207,126490
    156530,2012-05-07 14:55:00,Viaduct St Boston Ma,-71.041705,42.349905,126491
    156532,2012-05-07 17:27:00,830 Boylston St Boston Ma 02199,-71.082857,42.348595,126492

The format is `trip id,time,address,latitude,longitude,dropoff id`.  Here `dropoff id` is an identifier in
a dropoffs data set (that we have not provided).  Unfortunately, due to the way this dataset was generated, `trip id` is not
guaranteed to be unique.

In the lab directory is also a file `interestpoints.csv` of interesting locations in Boston.
Each line of this file is a named location and a latitude/longitude.  These points were provided by the
City of Boston as a list of locations where they are most interested in taxi activity.  

### Questions

Your goal for this lab is to construct a visualization that provides some insight into pattern of 
taxi rides through the interesting locations in Boston.  You are free to display the data and locations however you want, but here
are some things you may want to consider:

1. Do you want to produce a static visualization or an animation (e.g., over time), or an interactive visualization that lets users vary
some parameter?
1. For the locations, you will probably want to define some radius around each location to count the number of pickups in that location.
1. Think about the _story_ you want to tell from the data.  For example, you might try to visualize outliers in the dataset, or depict daily/weekly/monthly
patterns, or show the differences in traffic between locations.  The best visualization for each of these options is likely to be quite different.

Once you have made your visualization, answer the following questions:

* What is the message in your visualization and what techniques did you use to illustrate it?
* If you used interaction or animation, how does it facilitate the user's understanding?
* What format is the data that is used by the visualization?  Is it the raw data or did you need to compute some summary or derived data product?

# Submission Instructions

Put your visualization and answer to the questions somewhere on the
internet where we can access.  [http://bl.ocks.org/](http://bl.ocks.org/)
is a nice place if you don't want to host yourself.

Add your URL and name to [this spreadsheet](https://docs.google.com/spreadsheet/ccc?key=0Amk2aHsGhWktdE5SeF9JVExScGxYVS1PbkpWTWRxYVE&usp=sharing).
If you don't have a Google Drive account, feel free to email us your URL at `6885-staff@mit.edu`.

**Have you terminated your instances from previous labs?**

	aws ec2 terminate-instances --instance-ids <INSTANCE_ID>


Now you're almost done!  Go read the assigned paper(s) for today.

You can always feel free to contact us with questions on [Piazza](https://piazza.com/class/hl6u4m7ft8n373).
