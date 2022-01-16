# UTEK2022

The main repository for our submission to UTEK2022 Programming Competition.

Team
------------
- Mustafa Abdulrahman
- Michael Venier
- Isaac Muscat

Problem Description
------------
Main Problem: Optimizing the paths and the uses of different cleaning robots in a 100*100 grid to conserve the most energy. The main objective is to develop an algorithm to determine the most optimal cleaning robot, and the best paths to clean multiple locations in the most energy efficient manner.


Run Instructions
------------
Download all the necessary files(the txt input files) into InputFiles, and type into command line `python <script_name>.py`.

For us the `<script_name>.py` is main.py

Our Algorithm
------------
Part 1: We aggregated all of the files into lists.
Part 2: The targets were chosen by looking at the ones minimally distant from the robot. The robot then travels in a diagonal path as much as possible to reach the target. This minimized time travelled.
Part 3: The A* algorithm [1][2] was used to devise the optimal path for the robot to take to its targets
Part 4: The same process was used in part 2, but we calculated which robot would have the least energy usage by running part 2 for all of them and used the best robot.

In the Future...
-----------------------
For part 2 of our algorithm, we calculated the distances of the locations from the robot, and then called that function every time we cleaned a new location location. These calls could have been reduced or alternatively we used an algorithm to do all the steps for us in finding the optimal path that contained each location.
For part 4 of our algorithim, we found the best robot, and made the other robots rest, which was inefficient, because they were not used.

Citations
------------------------
[1]“A* search algorithm,” GeeksforGeeks, 24-Dec-2021. [Online]. Available: https://www.geeksforgeeks.org/a-search-algorithm/. [Accessed: 15-Jan-2022]. 


[2]“A* search algorithm,” Wikipedia, 13-Dec-2021. [Online]. Available: https://en.wikipedia.org/wiki/A*_search_algorithm. [Accessed: 15-Jan-2022]. 




