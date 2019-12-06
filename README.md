# adventofcode-2019

These are my solutions for the Advent of Code 2019 Challenges (https://adventofcode.com/).

* All of them is written with Python 2.7
* None of the solutions require special packages, only the core Python environment
* All of them are unique solutions that was not done with any peeking on existing ones, there are few exceptions though when I hopelessly got stuck and I went to the Reddit page of solutions to see how people approached the problem
* Many of them take parameters (like the input file to read, or how many cycles to execute, etc...)
* Some of them provide visual representation of the problem (maybe there is code inside but switched off)
* Some of them may be not optimal, but they finish on time, some of them are really quick though


# Challenges

## DAY 1
* Part1 is trivial
* Part2, pay attention to the suggestion: calculate the extra mass for each module separately, not for the whole all at once, different results may come

## DAY 2
* Part1, read the instructions :)
* Part2, I rewrote to have some OOP, lets see if it is usable or not, not using any pretty exceptions or non-globals, not needed to be pretty

## DAY 3
* Part1 is trivial if you know your 2D arrays
* Part2, it is crucial to chose a lightweight data structure, as the 2D matrix is huge, takes up lots of memory. I ended up storing only the Wire1 distance, hoping it will be enough and it was. A completely new approach also popped up in my mind about converting the input data into Edges, calculating their position with coordinates, calculating their intersections pairwise, then going through the data input once more and just store the distance for these calculated intersection coordinates. This approach was not needed luckily, as it would have meant a complete rewrite.

## DAY 4
* Both was easy, for Part2, I only extended the filtering because then I could utilize Counter (as numbers do not decrease, the counts are actually the length of the groups)

## DAY 5
* Reuse Day02's computer program, had to rewrite many things for Part1, but the OOP base was strong, so it was straightforward. Lesson learned: no need to remove code duplication now, further iterations might require it..
* Part2 added more instructions only basically. Also read carefully, WHEN the instruction pointer has to remain, basically it changes only once for every operation, but it changes once.

## DAY 6
* Part1, build a tree data structure with a simple recursive algorithm
* Part2, as the example shows and one can feel it, this is a find-the-common-ancestor problem, easy if you have built the data structure

## DAY 7

## DAY 8

## DAY 9

## DAY 10

## DAY 11

## DAY 12

## DAY 13

## DAY 14

## DAY 15

## DAY 16

## DAY 17

## DAY 18

## DAY 19

## DAY 20

## DAY 21

## DAY 22

## DAY 23

## DAY 24

## DAY 25
