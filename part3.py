import math
import robot as rbt
def run(inputDir, outputDir, filename):
    robot_list, locations_list, obstacles = loadData(inputDir, outputDir, filename)

    # Initialize variables
    robot = rbt.Robot(robot_list[0], int(robot_list[1]), int(robot_list[2]))
    locations = []
    grid = [[0 for i in range(100)] for j in range(100)]

    for i, location in enumerate(locations_list):
        loc_obj = rbt.Location(location[1], location[2], location[3])
        locations.append(loc_obj)
    

    for obstacle in obstacles:
        x1 = obstacle[0]
        y1 = obstacle[1]
        x2 = obstacle[2]
        y2 = obstacle[3]

        for i in range(x1, x2+1):
            for j in range(y1, y2+1):
                grid[i][j] = 1
    
    
    out = open(outputDir + "/" + filename.split(".")[0]+".out.txt", "w")

    robot = rbt.Robot(robot_list[0], int(robot_list[1]), int(robot_list[2]))
    
    out.write("Robot " + robot.name + "\n")

    # Goes through each location until all have been cleaned
    while len(locations_list) > 0:
        target = locations_list[0] # [index, x, y, time]

        # Set target to closest location
        for location in locations_list:
            dist_location = calculate_distance(robot.x, robot.y, location[1], location[2])
            dist_target = calculate_distance(robot.x, robot.y, target[1], target[2])


            if dist_location < dist_target:
                target = location.copy()
        
        path = a_star((robot.x, robot.y), (target[1], target[2]), grid)
        while len(path) > 0:
            next_path = path.pop()
            delta_x = next_path[0]-robot.x;
            delta_y = next_path[1]-robot.y;
            
            if (delta_x > 0 and delta_y > 0): 
              robot.x += 1
              robot.y += 1
              # situation where robot moves diagonal to top right
              out.write("move {0} {1}\n".format(robot.x, robot.y))
            elif (delta_x < 0 and delta_y > 0):
              robot.x -= 1
              robot.y += 1
              #situation where robot moves diagonal to top left
              out.write("move {0} {1}\n".format(robot.x, robot.y))
            elif (delta_x > 0 and delta_y < 0):
              robot.x += 1
              robot.y -= 1
              #situation where robot moves diagonal to bottom right
              out.write("move {0} {1}\n".format(robot.x, robot.y))
            elif (delta_x < 0 and delta_y < 0):
              robot.x -= 1
              robot.y -= 1
              #situation where robot moves diagonal to bottom left
              out.write("move {0} {1}\n".format(robot.x, robot.y))
            elif (delta_x > 0):
              robot.x += 1
              # situation where robot moves to right
              out.write("move {0} {1}\n".format(robot.x, robot.y))
            elif (delta_x < 0):
              robot.x -= 1
              # situation where robot moves to left
              out.write("move {0} {1}\n".format(robot.x, robot.y))
            elif (delta_y > 0):
              robot.y += 1
              # situation where robot moves up
              out.write("move {0} {1}\n".format(robot.x, robot.y))
            elif (delta_y < 0):
              robot.y -= 1
              # situation where robot moves down
              out.write("move {0} {1}\n".format(robot.x, robot.y))
        out.write("clean {0} {1}\n".format(robot.x, robot.y))
        locations_list.remove(target)

              
    out.close()
    
    



    
        
def a_star(start, goal, grid):

    f = {start: 0}
    g = {start: 0}
    h = {}

    opened = [start]
    closed = []

    cameFrom = {start: start}
    while len(opened) > 0:
        opened = sorted(opened, key=lambda x: f[x])
        current = opened[0]

        opened.remove(current)


        neighbours = getNeighbours(current, grid)

        for neighbour in neighbours:
            if neighbour == goal:
                cameFrom[neighbour] = current
                path = []
                cur = goal
                while cameFrom[cur] != cur:
                    path.append(cur)
                    cur = cameFrom[cur]

                return path
                
            gScore = g[current] + calculate_distance(current[0], current[1], neighbour[0], neighbour[1])
            hScore = calculate_distance(goal[0], goal[1], neighbour[0], neighbour[1])
            fScore = gScore + hScore
            if neighbour in opened or neighbour in closed:
                pass
            else:
                cameFrom[neighbour] = current
                opened.append(neighbour)
                g[neighbour] = gScore
                h[neighbour] = hScore
                f[neighbour] = fScore
        closed.append(current)




def getNeighbours(current, grid):
    neighbours = []

    x = current[0]
    y = current[1]

    if x>0 and grid[x-1][y] == 0:
        neighbours.append((x-1, y))

    if x < 99 and grid[x+1][y] == 0:
        neighbours.append((x+1, y))

    if y>0 and grid[x][y-1] == 0:
        neighbours.append((x, y-1))

    if y < 99 and grid[x][y+1] == 0:
        neighbours.append((x, y+1))


    if x > 0 and y > 0 and grid[x-1][y-1] == 0:
        neighbours.append((x-1, y-1))

    if x < 99 and y < 99 and grid[x+1][y+1] == 0:
        neighbours.append((x+1, y+1))

    if y > 0 and x < 99 and grid[x+1][y-1] == 0:
        neighbours.append((x+1, y-1))

    if y < 99 and x > 0 and grid[x-1][y+1] == 0:
        neighbours.append((x-1, y+1))

    return neighbours

def loadData(inputDir, outputDir, filename):
    f = open(inputDir + "/" + filename, "r")

    num_robots = 0
    num_locations = 0
    num_obstacles = 0

    num_robots, num_locations, num_obstacles = list(map(int, f.readline().split()))
    num_robots = int(num_robots)
    num_locations = int(num_locations)
    num_obstacles = int(num_obstacles)

    robot = f.readline().split() # (name, moveEff, cleanEff)
    locations = {}
    obstacles = []

    for i in range(num_locations):
        location = f.readline().split() # (x, y, timeRequired)
        location.insert(0, i)
        location = list(map(int, location))
        
        key = str(location[1])+" "+str(location[2])
        if locations.get(key):
            prev_loc = locations[location[1]+" "+location[2]]
            locations[key][3] = max(location[3], prev_loc[3])
        else:
            locations[key] = location
    
    for i in range(num_obstacles):
        o = f.readline().split() # (x1, y1, x2, y2)
        o = list(map(int, o))
        obstacles.append(o)

    return robot, list(locations.values()), obstacles


def calculate_distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)