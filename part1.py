import os

def aggregateAllInputs(dir, outputDir):
    directory = os.fsencode(dir)  
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".in.txt"):
            print(dir + "/" + filename) 
            run(dir, outputDir, filename)

def run(inputDir, outputDir, filename):
    f = open(inputDir + "/" + filename, "r")

    num_robots = 0
    num_locations = 0
    num_obstacles = 0

    num_robots, num_locations, num_obstacles = f.readline().split()
    num_robots = int(num_robots)
    num_locations = int(num_locations)
    num_obstacles = int(num_obstacles)

    robots = []
    locations = {}

    for i in range(num_robots):
        robot = f.readline().split() # (name, moveEff, cleanEff)
        robots.append(robot)

    for i in range(num_locations):
        location = f.readline().split() # (x, y, timeRequired)
        location.insert(0, i)
        
        if locations.get(location[1]+" "+location[2]):
            prev_loc = locations[location[1]+" "+location[2]]
            locations[location[1]+" "+location[2]][3] = max(location[3], prev_loc[3])
        else:
            locations[location[1]+" "+location[2]] = location


    out = open(outputDir + "/" + filename.split(".")[0]+".out.txt", "w")
    for robot in robots:
        line = "Robot Name: {0}; Movement Efficiency: {1}; Cleaning Efficiency: {2};\n"
        out.write(line.format(robot[0], robot[1], robot[2]))

    for key in locations:
        line = "Location Number: {0}; Time required: {1}; Location: {2} {3};\n"
        location = locations[key]
        out.write(line.format(location[0], location[3], location[1], location[2]))

    out.close()