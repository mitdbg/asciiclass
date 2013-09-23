# Lab 4: Entity Resolution

*Assigned: XXX, September XXX*

*Due: XXX, September XXX, 12:59 PM (just before class)*

In this lab, you will take two datasets that describe the same
entities, and identify which entity in one dataset is the same as an
entity in the other dataset.  Our datasets were provided by Foursquare
and Locu, and contain descriptive information about various venues
such as venue names and phone numbers.  In fact, we've turned this lab
into a competition: students will submit their best matching
algorihtms and try to beat one-another on a leaderboard to identify
the best algorithm.

This lab uses several files for you to test your entity resolution algorithms on:
 * [locu_train.json]()
 * [foursquare_train.json]()
 * [matches_train.csv]()

The `json` files contain a json-encoded list of venue attribute
dictionaries.  The `csv` file contains two columns, `locu_id` and
`foursquare_id`, which reference the venue `id` fields that match in
each dataset.

Your job is to write a script that will load both datasets and
identify matching venues in each dataset.  Measure the [precision,
recall, and F1-score](https://en.wikipedia.org/wiki/F-score) of your
algorithm against the ground truth in `matches_train.csv`.  Once
you're satisfied with an algorithm that has high values for these
training data points, move on to the two test files:
 * [locu_test.json]()
 * [foursquare_test.json]()

Your job is to generate `matches_test.csv`, a mapping that looks like `matches_train.csv` but with mappings for the new test listings.  Here are a few notes:
 * The schemas for these datasets are aligned, but this was something that Locu and Foursquare engineers had to do ahead of time when we initially matched our datasets.
 * The two datasets don't have the same exact formatting for some fields: check out the `phone` field in each dataset as an example.  You'll have to normalize some of your datasets.
 * There are many different features that can suggest venue similarity. Field equality is a good one: if the names or phone numbers of venues are equal, the venues might be equal.  But this is a relatively high-precision, low-recall feature (`Bob's Pizza` and `Bob's Pizzeria` aren't equal), and so you'll have to add other ones.  For example, [Levenshtein distance](https://en.wikipedia.org/wiki/Levenshtein_distance) between two strings offers finer granularity of how similar two strings are.  At Locu we have many tens of features, ranging from field equality to more esoteric but useful ones (e.g., "Does the first numeric value in the address field match?").
 * Since there are many features, you need some way to combine them.  A simple weighted average of values, where more important values (similar names) are weighed more highly will get you quite far.  In practice, you'd want to build a classifier that takes these features and learns the weights based on the training data.  If you're using Python and want to build a classifier, check out [scikit-learn](http://scikit-learn.org/).  We've seen good results with the decision tree ensemble/random forest techniques.  Note that this step will take time, so only do it if you've hand-rolled your own reasonable matcher already.
 * It's possible to be near 1 for precision/recall/F1 with enough training data and good enough machine learning models, but this took Locu engineers several months to get right.

# Submission Instructions

*Fill this in*