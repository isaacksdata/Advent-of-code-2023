# Notes of interest on Advent of Code puzzles

## Day 1

## Day 2

## Day 3

## Day 4

Has some fun with caching for part B. My first attempt without caching was estimated to take over a day to run!
I first implemented by own caching code using card IDs and results in a dictionary but then optimised the code
further by making use of the functools.cache decorator.

## Day 5

Part A was straightforward.
Part B was straightforward for the test data but it was immediately clear that it would be highly inefficient
to iterate over all numbers between the massive ranges described in the real data. I quickly came up with problem
statement - that I needed to map ranges rather than individual seed IDs but delivering a solution which worked
consistently took multiple attempts and several hours of debugging and walking through mappings. My working
solution does not feel optimal but it completes the problem in ~6ms.

## Day 6

Part A - very easy
Part B - similar to the day 5 puzzle in that it is not feasible to perform the part A solution on the larger scale
problem posed by part B. Similarly the solution here is to use ranges - the large number can be split into buckets
with each bucket representing a sub range within the big number. Once the assumption is realised that all values
within a bucket will be the same if start and end of bucket are equal then we only have to find the buckets where
start != end and then do a detailed iteration over these buckets - massively reducing the computation time.
