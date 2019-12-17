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
* Reuse Day02's computer program, had to rewrite many things for Part1, but the OOP base was strong, so it was straightforward. Lesson learned: no need to remove code duplication now, further iterations might require it.
* Part2 added more instructions only basically. Also read carefully, WHEN the instruction pointer has to remain, basically it changes only once for every operation, but it changes once.

## DAY 6
* Part1, build a tree data structure with a simple recursive algorithm
* Part2, as the example shows and one can feel it, this is a find-the-common-ancestor problem, easy if you have built the data structure

## DAY 7
* Part1 again reusing the computer program from 2 days ago, and abstracting out the IO into a class did the trick
* Part2 required a complete overhaul of the logic and required threading, queues, and the abstraction of the computer/amp itself: I put an amp into a thread with its own memory, io and everything, and then start them all with pre-fed queue input data and wait, while at the very end the answer is in AmpE's output queue, which I just need to read out. At the end it finally just clicked together.

## DAY 8
* Part1 is easy if you notice that the abount of layers has nothing to do with width or height, it is based on how many numbers you got.
* Part2 was straightforward with a little bit of 2D array handling. Start with the back of the image (reverse the layers) to build upwards.

## DAY 9
* For Part1 I reused not Day05's program, but rather Day07, as it was much better in architecture, modifying it is much easier. I lost a lot of time by a bug in the new opcode implementation, but after that it was straightforward
* Part2 was immediate, nothing has to be changed on Part1

## DAY 10
* Part1 was very tricky, as I ended up debugging a floating point rounding error and this was only happening in the 20x20 testcase, and only for 2-3 asteroids. Implemented the visibility check in two flavors: 1st is the classic y=mx+b equation in program (this is where floating point arithmetics can fool you if you look for whole numbers), the 2nd is based on similar proportions and still looking for whole numbers, but avoids floating-point multiplication. The issue with the 1st one was was that python did not show the rounding errors, and kept printing out the integer-lookalike floats (the documentation says this is intentional, while repr() shows the true float), and I used the is_integer() helper method, which knew it was not integer, although it looked like one. Ended up using the classic tolerance check, but sure this was a frustrating debugging session...
* Part2 was more straightforward, I ended up using trigonometry to order the visible asteroids (calculating tangents), and redoing the visibility checks in a loop until only one asteroid was left

## DAY 11
* Both Part1 and Part2 is easy enough, maybe my OOP code helps a lot. I created another IO variant for this challenge, and stored the already visited hull-parts in a map, and dynamically constructed the printout itself even for Part1. It was surprisingly easy, however for Part1, the drawing is slow, so I turned it off eventually.

## DAY 12
* Part1 is super simple
* For Part2, I had to peek into the solutions of Reddit, and used the hint of finding the LCM of the periods of the axis returning to 0, multiplying by 2. For me this is magic now, will investigate further later.

## DAY 13
* Part1 is easy, implemented yet another IO class for this
* Part2 was super fun, once I realised this is a boulder-dash simulator. I run a simulation in another computer in every read to determine where I would need to pull the joystick. If the ball is right above the paddle I do not run the simulation because that would immediatelly instruct a movement and this in 50% of the time is a wrong move just then. And finally there is some randomness in it because if not, the game became an endless loop, so since there are two perfectly valid spots to move the paddle to, I do the random-choice between them. Sometimes the play is a lose, because the randomness picks a choice and drives itself into a situation when the paddle cannot reach the destination in time, but it is possible to finish the game in a few tries.

## DAY 14
* Part1 is easy, start from 1 FUEL, then work backwards, luckily the transformation rules are unique
* For Part2, I first quickly set an interval of the powers of 2 where to look for the answer, and then I reduce this interval by binary search to the answer

## DAY 15
* For Part1, I reused the latest IntCode program, and implemented yet another IO class. For this, I build a tree of neighboring Area tiles, and using some kind of path-finding algorithm to wander around, and backtrack if no non-visited tiles are in the neighboring list. Collecting the solutions, but there seems to be only one.
* For Part2, simply extract the final map from the computer, and while there are empty areas, loop through the Oxygen-filled area and mark all the neighbors also with Oxygen, and count the steps required

## DAY 16
* Part1 was easy, even naive algos work, python provides many convenience functions for this problem
* Part2 required a completely new approach, and a few insights (that I need to peek into the Reddit posts for): 1) the offset points to the second half of the number, 2) the pattern at the second half of the number is simply just a bunch of zeroes and a bunch of ones, 3) one can calculate the new number using hint No2, and you do not even need to take the absolute-value and not even the mod2 all the time. This solution is running in 30 seconds, but there are ways to make it super-fast with more techniques. Unfortunately the first half of the number cannot be calculated like this, it remains garbage.

## DAY 17
* Part1 is really just the warmup, again another IntCode IO class, very simple
* Part2 was tricky. First, we need the trajectory of the robot with the turns and the number of steps, this turned out to be the simplest, luckily the path is simple and unique. Then one needs to find solutions to the problem of having A,B,C path-fragments, that could fully cover the previosuly calculated path but any of A,B,C could be reused. I ended up brute-forcing it, as the path is short and the 3 sub-paths are not that big of a problem domain, however implementing this is very tricky and I did not want to convert to String (the biggest number is less than 16, so a hexadecimal storage would have worked out well, and strings have so many cool features for this). Ended up doing so many debugging runs, but after I got a fine answer for the test-case, everything was easy, just feed the calculated data into another round of IntCode computing.

## DAY 18

## DAY 19

## DAY 20

## DAY 21

## DAY 22

## DAY 23

## DAY 24

## DAY 25
