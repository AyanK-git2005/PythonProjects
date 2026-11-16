
def load_env(filename):
    '''Loads Environment text file and returns the tuple: (Grid Dimensions, Number of Obstacles,
     Obstacle Locations, Number of Dirts, Dirty Locations, Charger Location)'''
    
    try:
        with open(filename, "r") as env_file:
            env_info = env_file.read()
            env_file.close()

        lines = env_info.splitlines()
        grid_dimensions = lines[0]
        charge_loc = eval(lines[5])

        obst_num = lines[1]
        obst_loc = []
        for x in lines[2].split(', '):
            obst_loc.append(eval(x))

        dirt_num= lines[3]
        dirt_loc = []
        for x in lines[4].split(', '):
            dirt_loc.append(eval(x))

        return (grid_dimensions, obst_num, obst_loc, dirt_num, dirt_loc, charge_loc)
    
    except Exception:
        print('Error: Something went wrong! Returning None.')
        return None

#print(load_env("env1.txt"))