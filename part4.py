import math
import robot as r
import part2


def run(inputDir, outputDir, filename):
    robots, locations1 = loadData(inputDir, filename)
    outputPath(robots, locations1, outputDir, filename)

def loadData(inputDir, filename):
    f = open(inputDir + "/" + filename, "r")

    num_robots = 0
    num_locations = 0

    num_robots, num_locations, num_obstacles = f.readline().split()
    num_robots = int(num_robots)
    num_locations = int(num_locations)

    robots = [] # (name, moveEff, cleanEff)
    for rbt in range(num_robots):
        robots.append(f.readline().split())

    locations = {}

    for i in range(num_locations):
        location = f.readline().split() # (x, y, timeRequired)
        location.insert(0, i)
        location[1] = int(location[1])
        location[2] = int(location[2])
        location[3] = int(location[3])
        
        key = str(location[1])+" "+str(location[2])
        if locations.get(key):
            prev_loc = locations[key]
            locations[key][3] = max(location[3], prev_loc[3])
        else:
            locations[key] = location

    return robots, locations

def outputPath(robot_list, original_location_list, outputDir, filename):

    robot_energies = []

    for index, next_robot in enumerate(robot_list):
        total_energy = 0

        robot = r.Robot(next_robot[0], index, int(next_robot[2]))
        locations_list = list(original_location_list.values()).copy()

        # Goes through each location until all have been cleaned
        while len(locations_list) > 0:
            target = locations_list[0] # [index, x, y, time]

            # Set target to closest location
            for location in locations_list:
                dist_location = calculate_distance(robot.x, robot.y, location[1], location[2])
                dist_target = calculate_distance(robot.x, robot.y, target[1], target[2])


                if dist_location < dist_target:
                    target = location.copy()
            
            print("Num locations left: {0}".format(len(locations_list)))
            print(calculate_distance(robot.x, robot.y, target[1], target[2]))
            while calculate_distance(robot.x, robot.y, target[1], target[2]) > 0:
                delta_x = target[1]-robot.x;
                delta_y = target[2]-robot.y;
                
                if (delta_x > 0 and delta_y > 0): 
                    robot.x += 1
                    robot.y += 1
                    # situation where robot moves diagonal to top right
                    total_energy += robot.moveEff
                elif (delta_x < 0 and delta_y > 0):
                    robot.x -= 1
                    robot.y += 1
                    #situation where robot moves diagonal to top left
                    total_energy += robot.moveEff
                elif (delta_x > 0 and delta_y < 0):
                    robot.x += 1
                    robot.y -= 1
                    #situation where robot moves diagonal to bottom right
                    total_energy += robot.moveEff
                elif (delta_x < 0 and delta_y < 0):
                    robot.x -= 1
                    robot.y -= 1
                    #situation where robot moves diagonal to bottom left
                    total_energy += robot.moveEff
                elif (delta_x > 0):
                    robot.x += 1
                    # situation where robot moves to right
                    total_energy += robot.moveEff
                elif (delta_x < 0):
                    robot.x -= 1
                    # situation where robot moves to left
                    total_energy += robot.moveEff
                elif (delta_y > 0):
                    robot.y += 1
                    # situation where robot moves up
                    total_energy += robot.moveEff
                elif (delta_y < 0):
                    robot.y -= 1
                # situation where robot moves down
                total_energy += robot.moveEff

            # Clean target
            print(locations_list)
            total_energy += target[3] * robot.cleanEff
            locations_list.remove(target)

        # Store total energy
        robot_energies.append(total_energy)
    # Now we rank the robots
    best_index = 0
    best_robot = robot_energies[best_index];
    for i, robot_energy in enumerate(robot_energies): 
      if (best_robot > robot_energy) :
        best_robot = robot_energy
        best_index = i
      
    print(robot_list[best_index])
    cur_pos_x, cur_pos_y = part2.outputPath(robot_list[best_index], original_location_list, outputDir, filename)
    # this method returns the x and y position after the robot finishes cleaning

    print(cur_pos_x, cur_pos_y)
    # Return to origin --> (best_index, 0)

    out = open(outputDir + "/" + filename.split(".")[0]+".out.txt", "a")
    while calculate_distance(cur_pos_x, cur_pos_y, best_index, 0) > 0:
      delta_x = best_index - cur_pos_x;
      delta_y = 0 - cur_pos_y;
      
      if (delta_x > 0 and delta_y > 0): 
          cur_pos_x += 1
          cur_pos_y += 1
          out.write("move {0} {1}\n".format(cur_pos_x, cur_pos_y))
          # situation where robot moves diagonal to top right
          
      elif (delta_x < 0 and delta_y > 0):
          cur_pos_x -= 1
          cur_pos_y += 1
          out.write("move {0} {1}\n".format(cur_pos_x, cur_pos_y))
          #situation where robot moves diagonal to top left
      elif (delta_x > 0 and delta_y < 0):
          cur_pos_x += 1
          cur_pos_y -= 1
          out.write("move {0} {1}\n".format(cur_pos_x, cur_pos_y))
          #situation where robot moves diagonal to bottom right
      elif (delta_x < 0 and delta_y < 0):
          cur_pos_x -= 1
          cur_pos_y -= 1
          out.write("move {0} {1}\n".format(cur_pos_x, cur_pos_y))
          #situation where robot moves diagonal to bottom left
      elif (delta_x > 0):
          cur_pos_x += 1
          out.write("move {0} {1}\n".format(cur_pos_x, cur_pos_y))
          # situation where robot moves to right
      elif (delta_x < 0):
          cur_pos_x -= 1
          out.write("move {0} {1}\n".format(cur_pos_x, cur_pos_y))
          # situation where robot moves to left
      elif (delta_y > 0):
          cur_pos_y += 1
          out.write("move {0} {1}\n".format(cur_pos_x, cur_pos_y))
          # situation where robot moves up
      elif (delta_y < 0):
          cur_pos_y -= 1
          out.write("move {0} {1}\n".format(cur_pos_x, cur_pos_y))
      # situation where robot moves down
    out.write("rest \n")

    for index, next_robot in enumerate(robot_list):
      if (index != best_index):
        out.write("\nRobot " + next_robot[0] + "\n")
        out.write("rest\n")
      
    

        



def calculate_distance(robot_x, robot_y, location_x, location_y):
    return math.sqrt((robot_x - location_x)**2 + (robot_y - location_y)**2)