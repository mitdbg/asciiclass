# Lab 3

*Assigned: sometime*

*Due: Sometime (just before class)*

In this lab, you will use various types of tools -- from low-level tools like sed and awk to high-level tools like Data Wrangler -- to perform data parsing and extraction from data encoded into a text file.  The goal of this lab is simply to gain experience with these tools and compare and contrast their usage.


# Setup

To start, go to the AWS console and start your EC2 instance.  SSH into it.
First, you need to check out/update the files for lab3:

    cd asciiclass/labs/
    git pull

Then :

    cd lab3

The _lab3_ directory contains two datasets (in addition to the datasets used in class):

1. A dataset of synonyms and their meanings (_synsets_). Each line contains one synset with the following format:

    ID, &lt;synonyms separated by spaces&gt;, &lt;different meanings separated by semicolons&gt;

1. The second dataset is a snippet of the following Wikipedia webpage on [FIFA (Soccer) World Cup](http://en.wikipedia.org/wiki/FIFA_World_Cup).
Specifically it is the source for the table toward the end, that lists the teams reaching the top four. 

# Wrangler

Go to the [data wrangler website](http://vis.stanford.edu/wrangler/app/).  Load each of the datasets (we recommend a small subset -- 100~ lines) into data wrangler and try playing with the tool.

## Tasks:

1. For the synsets data set, use the data wrangler tool to generate a list of word-meaning pairs. The output should look like:

	'hood,(slang) a neighborhood
	1530s,the decade from 1530 to 1539
	...
	angstrom,a metric unit of length equal to one ten billionth of a meter (or 0.0001 micron)
	angstrom, used to specify wavelengths of electromagnetic radiation
	angstrom\_unit,a metric unit of length equal to one ten billionth of a meter (or 0.0001 micron)
	angstrom\_unit, used to specify wavelengths of electromagnetic radiation
	...

2. For the FIFA dataset, use the tool to generate output as follows.

	Brazil, 1962, 1
	Brazil, 1970, 1
	Brazil, 1994, 1
	Brazil, 2002, 1
	Brazil, 1958, 1
	Brazil, 1998, 2
	Brazil, 1950, 2
	...

i.e., each line in the output contains a country, a year, and the position of the county in that year (if within top 4).


NOT EDITED BEYOND THIS

5. now use wrangler to extract the structured content.  What was easy to do?  What was difficult?
6. dump the structured content into sqlite3 or postgresql
1. run some queries on the extracted text to prove you've done it.


Some tips:

1. Undo tool
1. Export tool

# Grep, Sed & Awk

The set of three UNIX tools, _sed_, _awk_, and _grep_, can be very useful for quickly cleaning up and transforming data for further analysis
(and have been around since the inception of UNIX). 
In conjunction with other unix utilities like _sort_, _uniq_, _tail_, _head_, etc., you can accomplish many simple data parsing and cleaning 
tasks with these tools. 
You are encouraged to play with these tools and familiarize yourselves with the basic usage of these tools. However, there is no explicit 
deliverable in this lab.

As an example, the following sequence of commands can be used to answer the third question from the previous lab ("Find the five uids that have tweeted the most").

	grep "created\_at" twitter.json | sed 's/"user":{"id":\([0-9]\*\).\*/XXXXX\1/' | sed 's/.\*XXXXX\([0-9]\*\)$/\1/' | sort | uniq -c | sort -n | tail -5

To get into some details:

## grep

The basic syntax for _grep_ is: 

	 grep 'regexp' filename

or equivalently (using UNIX pipelining):

	cat filename | grep 'regexp'

The output contains only those lines from the file that match the regular expression. Two options to grep are useful: _grep -v_ will output those lines that
_do not_ match the regular expression, and _grep -i_ will ignore case while matching. See the manual (or online resources) for more details.

## sed
Sed stands for _stream editor_. Basic syntax for _sed_ is:

	sed 's/regexp/replacement/g' filename

For each line in the intput, the portion of the line that matches _regexp_ (if any) is replaced with _replacement_. Sed is quite powerful within the limits of
operating on single line at a time. You can use \( \) to refer to parts of the pattern match. In the first sed command above, the sub-expression within \( \)
extracts the user id, which is available to be used in the _replacement_ as \1. If the _regexp_ contains multiple \( \), the subexpression matches are available
as \1, \2, and so on.

In the above example, the first command (_grep_) discards the deleted tweets, the _sed_ commands extract the first "user-id" from each line, _sort_ sorts the user ids, and _uniq -c_ counts the unique entries (i.e., user ids). The final _sort -n | tail -5_ return the top 5 uids.

Note that, combining the two _sed_ commands as follows does not work -- we will let you figure out why.

	grep "created\_at" twitter.json | sed 's/.\*"user":{"id":\([0-9]\*\).\*/\1/' | sort | uniq -c | sort -n | tail -5"

## awk 

Finally, _awk_ is a powerful scripting language (not unlike perl). The basic syntax of _awk_ is: 

	awk -F',' 'BEGIN{commands} /regexp1/ {command1} /regexp2/ {command2} END{commands}' 

For each line, the regular expressions are matched in order, and if there is a match, the corresponding command is executed (multiple commands may be executed
for the same line). BEGIN and END are both optional. The _-F','_ specifies that the lines should be _split_ into fields using the separator _,_, and those fields are available to the regular
expressions and the commands as $1, $2, etc. See the manual or online resources for further details. 

## Comparing to Data Wrangler

The above tools can do many of the things that Data Wrangler enables you to do. E.g., most of the _map_ operations in Data Wrangler directly map to the tools above.

## Examples 

A few examples to give you a flavor of the tools and what one can do with them.

1. _wrap_ on labor.csv (i.e., merge consecutive groups of lines referring to the same record)
	cat labor.csv | awk '/^Series Id:/ {print combined; combined = $0} !/^Series Id:/ {combined = combined", "$0;} '

1. On the crime data, the following command does _fill_ (first row of output: "Alabama, 2004, 4029.3".
	cat crime.txt | grep -v '^,$' | awk '/^[A-Z]/ {state = $4} !/^[A-Z]/ {print state, $0}'

1. Wrangle the crimes data as done in the Wrangler demo. The following works assuming perfectly homogenous data (as the provided dataset is).
	cat crime.txt | grep -v '^,$' | sed 's/Reported crime in //; s/[0-9]\*,//' | awk 'BEGIN {printf "State, 2004, 2005, 2006, 2007, 2008"} /^[A-Z]/ {print c; c=$0} !/^[A-Z]/ {c=c", "$0;} END {print c}'

1. Same as above but allows the data to contain incomplete information (e.g., some years may be missing).
	cat crime.txt | grep -v '^,$' | sed 's/Reported crime in //; s/[0-9]\*,//' | awk -F',' '/^[A-Z]/ {if(state) {printf(state); for(i = 2004; i &lt= 2008; i++) {if(array[i]) {printf("%s,", array[i])} else {printf("0,")}}; printf("\n");} state=$0; delete array} !/^[A-Z]/ {array[$1] = $2}'
    
## Tasks:

Perform the above cleaning tasks using these tools. QUESTION: Should we provide a portion of the command for the second one?


NOT EDITED BEYOND THIS

2. use sed/awk to extract out the descriptions of the events, the tags, and the hours
3. what's the most popular 1/2-grams?
4. what are the most popular hours?  for partying?



### Questions

1. What does fold/un-fold do?


**Handing in your work**:

Your task is to write a query that XXXX.

You should create a text file with your name, XXX.  Upload it to the [course Stellar site](http://stellar.mit.edu/S/course/6/fa13/6.885/) as the "lab3" assignment.

Now you're almost done!  Go read the assigned paper(s) for today.

You can always feel free to email us with questions at [6885staff@mit.edu](mailto:6885staff@mit.edu).
