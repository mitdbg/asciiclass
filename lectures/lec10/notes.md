# Lab 5 response

Yahoo and non-enron accounts are where the interesting content is

Many of the things are spam

# Approximate Query Processing


Goal: low latency queries on lang edatasets
      
Use summary or subset of data to answer _some_ queries over original data

Tricks

* Histograms
* Samples
* Sketches

History lesson:  DBs used to run query plans on sample of the data for cost estimation.  Later, trick surfaced as approximate query processing to handle large datasets.

## Histograms

Frequency count of values:

    Salary    Count
    0-10        5
    10-20      10
    20-30       5
    30-40      12
    >40        15

Answer

    select count(*) where salary between [25 - 35]
    Estimate as 1/2 * 5 + 1/2 * 12

Nice for these aggregation queries.  

Not so good for

* Outliers: Catch all bins (>40) throws away outlier information.  Could use exception lists, etc
* Non-numeric values (e.g., LIKE)
* May fix minimum granularity (usually use equiheight histogram rather than equiwidth)
* Guarantees?  
* Joins
* Using multiple histograms (if dimensions are correlated)
* Multi-dimensional histograms are expensive

## Sampling

* Compute sample, use to answer query

given:

    f: function
    S: sample
    g: answer
    g': estimated answer

    if Q(s) = g, g' = g/f
    Can figure this out for some Qs (mean, count, sum, etc)

Pros:

* Sample contains non-numeric fields
* Correlations may be preserved

Cons:

* Computing extrema is hard e.g., max, min
* Sample size increases ^2 wrt desired confidence
* Rare items not in sample.  


### How to actually use sampling?

At query time, read data in single pass and use Bernoulli sampling.  Doesn't guarantee sample size!

[Reservoir sampling](http://en.wikipedia.org/wiki/Reservoir_sampling): math trick to guarantee a sample size.  To convince yourself, consider how it works with sample size 1

Probably don't want to compute sample at query time (will need to read all the data, which we are trying to avoid!) Instead, we can:

* precompute and store samples, then choose sample to use at query time
* (somehow) randomly pick blocks to read at query time
    * Problem: we want to avoid random IO!
    * trick is played when blocks are distributed
    * randomized indices

Theoretical guarantees break down if you keep using single sample if unlucky

* Could use escape hatch and run over all the data
* Could store multiple samples at multiple sizes

How to handle rare-subgroups?

* Stratified sampling
        
        sample from group if size > k
        entire group if size < k

* Pick attributes to stratify over using past workload queries on 
* note: using past workloads is a classic database trick

[BlinkDB@Berkeley/MIT](http://blinkdb.org/) uses stratified sampling

    select avg(sal) from T 
    where dept = 'eng' within X seconds
    
    or 
    
    select avg(sal) from T
    where dept = 'eng' w/ conf 95%
    
Works as follows

    workload -> pick lots of stratified samples 
    query -> pick samples to use -> run query on sample on hive --> error estimation --> result

        
