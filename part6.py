import math
import pygame
import robot as r
import time

def run(inputDir, outputDir, filename):
    robot1, locations1 = loadData(inputDir, filename)
    outputPath(robot1, locations1, outputDir, filename)

def loadData(inputDir, filename):
    f = open(inputDir + "/" + filename, "r")

    num_robots = 0
    num_locations = 0

    num_robots, num_locations, num_obstacles = f.readline().split()
    num_robots = int(num_robots)
    num_locations = int(num_locations)

    robot = f.readline().split() # (name, moveEff, cleanEff)
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

    return robot, locations

def outputPath(robot_list, locations_list, outputDir, filename):

    pygame.init()
    width = 640
    height = 480
    screen = pygame.display.set_mode((width, height))

    robot = r.Robot(robot_list[0], int(robot_list[1]), int(robot_list[2]))
    locations_list = list(locations_list.values())


    # Goes through each location until all have been cleaned
    while len(locations_list) > 0:
        target = locations_list[0] # [index, x, y, time]

        # Set target to closest location
        for location in locations_list:
            dist_location = calculate_distance(robot.x, robot.y, location[1], location[2])
            dist_target = calculate_distance(robot.x, robot.y, target[1], target[2])


            if dist_location < dist_target:
                target = location.copy()
        
        while calculate_distance(robot.x, robot.y, target[1], target[2]) > 0:

            delta_x = target[1]-robot.x;
            delta_y = target[2]-robot.y;
            
            if (delta_x > 0 and delta_y > 0): 
              robot.x += 1
              robot.y += 1
              # situation where robot moves diagonal to top right
            elif (delta_x < 0 and delta_y > 0):
              robot.x -= 1
              robot.y += 1
              #situation where robot moves diagonal to top left
            elif (delta_x > 0 and delta_y < 0):
              robot.x += 1
              robot.y -= 1
              #situation where robot moves diagonal to bottom right
            elif (delta_x < 0 and delta_y < 0):
              robot.x -= 1
              robot.y -= 1
              #situation where robot moves diagonal to bottom left
            elif (delta_x > 0):
              robot.x += 1
              # situation where robot moves to right
            elif (delta_x < 0):
              robot.x -= 1
              # situation where robot moves to left
            elif (delta_y > 0):
                robot.y += 1
              # situation where robot moves up
            elif (delta_y < 0):
              robot.y -= 1
              # situation where robot moves down

            # PYGAME
            time.sleep(0.1)
            screen.fill((255, 255, 255))
            for loc in locations_list:
                pygame.draw.circle(screen, (0, 255, 0), (loc[1]/100*width, loc[2]/100*height), 5)
            pygame.draw.circle(screen, (255, 0, 0), (robot.x/100*width, robot.y/100*height), 5)




            pygame.display.update()

            # END PYGAME
        locations_list.remove(target)
    pygame.quit()
    return robot.x, robot.y      


def calculate_distance(robot_x, robot_y, location_x, location_y):
    return math.sqrt((robot_x - location_x)**2 + (robot_y - location_y)**2)