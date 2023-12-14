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

## Day 7

Part A - fairly easy, a couple of interesting sort problems which could be solved using custom
sort functions. I had not come across `functools.cmp_to_key` before which was useful when you need
complex custom sorting functions.
Part B - easy to write the initial logic to handle jokers. Ran into a couple of edge cases such as when jokers
were the only pair etc. Interesting use of `functools.partial` to provide arguments to the custom sorting
function used in part A.

## Day 8

Part A - simple dictionary to map between nodes
Part B - Quickly apparent that more was required than to just follow multiple nodes and break the while loop when all
are at an end node. I spent a while on this puzzle trying to understand where the shortcut might be. I eventually
stumbled on the oscillation behaviour of the paths by tracking the indices of end_nodes along each path. Once I
realised this pattern, then some basic number theory formulas could help to find the right answer.

## Day 9

Part A - use `np.diff` iteratively.
Part B - just add an option to predict previous rather than next
