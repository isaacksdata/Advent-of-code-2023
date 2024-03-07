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

## Day 10

Part A - took me quite a while to implement the solution correctly even though I knew what the correct approach should
be. A few corner cases caused trouble in correctly determining the end point of the loop such as multiple possible next
steps along one arm of the loop being able to access the same co-ordinate.
Part B - this one took me a while - for a while I did not really have an idea of how to handle the gaps between pipes.
After a few hours of playing around, I decided to try expanding the array 3x so that the gaps between pipes could
be represented by a an entry in the array. Then I would be able to use a flood-fill from the edges to discount these
spaces. Even once I had this idea, it took me a while to get a working implementation. My first working attempt was to
re-walk the maze and map onto the 3x array - but this took nearly 30s to successfully solve the real puzzle. I then
spent a bit of time looking for a more efficient solution and realised that I should simply track a list of coordinates
from part A of the problem so that I could then iterate along the list of coordinates without having to do any logic to
check that the next coordinate is the right one. This got the time down to \<50ms!
Might be fun to try the Shoelace algorithm with Picks Theorem.
Theorem approach comes out marginally quicker.

## Day 11

Part A -> easy, just format the array, pair of up the labels and find Euclidean distance
Part B -> not feasible to insert millions of rows/cols into an array - so needed a way of knowing how many
empty rows/cols would be found between g1 and g2 and then just multiplying by the scaling factor to find
the real coordinates - then just get Euclidean distance again.

## Day 12

Part A - can brute force through all possible solutions and find matches
Part B - now cannot brute force as too many possibilities. Spent a long time on this part,
I knew i needed to use recursion and caching (dynamic programming) but took a while to find
where the recursion needed to be implemented.

## Day 13

Part A - Simple enough, find possible mirror lines where neighbouring rows/cols are equal and then
iterate towards the edges until it fails or reach an edge.

Part B - nothing special needed here - just find potential smudge points by nearly equal rows/cols and then check
the answer of each possible smudge location to see if it gives a different mirror line.

## Day 14

Part A - straightforward - just write a function to move round rocks towards top

Part B - more difficult - first implemented the brute force solution which estimated to run in 200hrs.
Next tried caching which brought it down to 3hrs. Suggested to me that there might be some cycling going on. So i
checked for a cycle and sure enough this was the fast way to get the answer. Iterate until you find a previous state
and this is then the start of the loop. Trivial to then find final array state.

## Day 15

Part A - easy

Part B - trivial logic to organise the lenses into boxes.

## Day 16

Part A - tricky to get all the logic implemented for handling the different objects in the map. I went with recursion
recursion to analyse all of the new beams produced during analysis.

Part B - brute forced across all of the possible start points - could be speeded up by passing on information about
internal beams.

## Day 17

Part A - took forever! I figured I either needed Djikstra or recursion. I started with a recursive solution but could
not seem to get it to work. I then started implementing Djikstra's algorithm with a prioity queue - I had not really
come across this stuff before so spent some time reading and understanding. Ended up implementing the A\* algorithm
whereby the priority of the next pointer in the queue is determined by the cost and the distance to the
goal. A\* should be used where there is only one end point. The tricky part was then
modifying the algorithm to account for the constraints on consecutative moves etc and how to correctly
track state to account for this.

Part B - once part A was working, it was relativley littel work to get Part B

## Day 18

Part A - trivial to implement logic for the instructions and create an array which could be manipulated with ndimage.

Part B - part A solution is now not feasible due to huge size of array. A similar problem was solved on day 10 using
Shoelace and Pick theorems.

## Day 19

Part A - easy, some fun with dynamically generating functions from the workflow strings.

Part B - took a bit of thinking about to implement a recursive solution to solve all ranges of values.

## Day 20

Part A - easy enough once I had written the logic for each time of module

Part B - I tried a few incorrect solutions such as caching (involved hashing the modules). This still took a
very long time so i figured there must be some kind of loop and sure enough the
penultimate module turns out to be conjunction with a cycle of memory. So finding the cycle time of
each input in the memory gets the answer.
