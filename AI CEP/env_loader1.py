
def load_env(filename):
    """Loads environment configuration from a text file.

    Parameters:
    - filename (str): The path to the environment text file.

    Returns:
    - tuple: A 6-tuple containing:
        - grid_dimensions (tuple): (rows, cols) of the grid.
        - obst_num (int): Total number of obstacles.
        - obst_loc (list of tuples): Coordinates of all obstacle cells.
        - dirt_num (int): Total number of dirt locations.
        - dirt_loc (list of tuples): Coordinates of all dirt cells.
        - charge_loc (tuple): Coordinates of the charger station.
    - Returns `None` if an error occurs during parsing or file loading.
    """
    
    try:
        with open(filename, "r") as env_file:
            env_info = env_file.read()
            env_file.close()

        lines = env_info.splitlines()
        grid_dimensions = eval('('+ lines[0] +')')
        charge_loc = eval(lines[5])

        obst_num = eval(lines[1])
        obst_loc = []
        for x in lines[2].split(', '):
            obst_loc.append(eval(x))

        dirt_num= eval(lines[3])
        dirt_loc = []
        for x in lines[4].split(', '):
            dirt_loc.append(eval(x))

        return (grid_dimensions, obst_num, obst_loc, dirt_num, dirt_loc, charge_loc)
    
    except Exception:
        print('Error: Something went wrong! Returning None.')
        return None

#print(load_env("env1.txt"))