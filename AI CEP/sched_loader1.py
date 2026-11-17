
def load_sched(filename):
    """Loads scheduling, precedence, and time constraints from a text file.

    Parameters:
    - filename (str): The path to the schedule text file.

    Returns:
    - tuple: A 5-tuple containing:
        - timeslots_num (int): Total number of available timeslots.
        - prec_constraints_num (int): Number of precedence constraints.
        - prec_constraints (list of tuples): Parsed pairs of precedence constraints with 'D' prefix removed.
        - time_constraints_num (int): Number of time constraints.
        - time_constraints (list of tuples): Parsed time constraints with 'D' and 'T' prefixes removed.
    - Returns `None` if an error occurs during parsing or file loading.
    """
    
    try:
        with open(filename, "r") as sched_file:
            sched_info = sched_file.read()
            sched_file.close()

        lines = sched_info.splitlines()
        timeslots_num = eval(lines[0])
        prec_constraints_num = eval(lines[1])

        l = 2
        prec_constraints = []
        for p in range(prec_constraints_num):
            prec_constraints.append(eval(lines[p+2].replace('D','').replace('d','')))
            l += 1
        
        time_constraints_num = eval(lines[l])
        time_constraints = []
        
        l += 1
        for t in range(time_constraints_num):
            time_constraints.append(eval(lines[t+l].replace('D','').replace('d','').replace('T','').replace('t','')))

        return (timeslots_num, prec_constraints_num, prec_constraints, time_constraints_num, time_constraints)

    except Exception:
        print('Error: Something went wrong! Returning None.')
        return None

#print(load_sched("sched1.txt"))