import numpy as np
import random
import json
import os
import math
#random parameters. num_v num_m num_j need to be set for instance size
def generateInstance(num_instance = 1, num_c = 3, num_j = 10, num_m=2, num_v = 2,\
                     Rho = 10, mu = 3, delta = 200, fixed_seed = False):
    """
    Parameters
    ----------
    num_instance : unique instance number
    num_c : number of customers
    num_j : number of jobs
    num_m : number machines
    num_v : number vehicles
    Rho : influences job processing time and capacity utilization on vehicle
    mu : influences vehicle capacities
    delta : high delta means high travel distances
    fixed_seed : default False, 

    Returns a dict with all data
    """
    
    if fixed_seed:
        seed = 100
    else:
        seed = random.randint(0, 10000)
    rnd = np.random
    rnd.seed(seed)
    #number of vehicles
    V = [i for i in range(1,num_v+1)]
    #number of jobs
    J = [j for j in range(1,num_j+1)]
    # J + 1: artifical job
    #number of machines
    M = [m for m in range(1,num_m+1)]
    #number of locatations : 0 is production facility and others are customers
    #num_c = round(num_j / 3) - 1 #one could just divide number of jobs by 3..
    N = [n for n in range(0, num_c + 1)]
    #processing due date job j (if scheduling problem only)
    p = {j: math.ceil(np.random.uniform(1,0.5 * Rho)) if j != 0 else 0 for j in J} 
    #processing time of job j
    u = {j: math.ceil(np.random.uniform()*p[j]) if j != 0 else 0 for j in J} 
    #size of job j regarding vehicle loading
    #make sure job with largest size can be loaded somewhere
    job_no_maxSize = max(u, key=u.get)
    #capacity of vehicle
    c = {v: u[job_no_maxSize] + math.ceil(np.random.uniform(1,mu * u[job_no_maxSize]))  for v in V} #capacity vehicle v
    s = {j: math.ceil(np.random.uniform(1, p[j])) if j!=0 else 0 for j in J + [0]}
    r = {m: math.ceil(np.random.uniform(0, 1 * Rho)) for m in M} #ready time machine m
    q = 1000 # Big M 
    r_hat = {v: rnd.randint(0.5*Rho,1.5*Rho) for v in V} #ready time vehicle v
    #service time
    #-------------------------------------------------------------------------
    #setup coordinates for production site and customer sites. converting back to list..
    xc = [math.ceil(np.random.uniform(1, delta)) for i in range(num_c+1)] 
    #+1 for production site
    yc = [math.ceil(np.random.uniform(1, delta)) for i in range(num_c+1)]
    #rounding euclidian distances
    distances_locations = {(i,j): math.ceil(np.hypot(xc[i]-xc[j], yc[i]-yc[j])) for i,j in [(i,j) for i in N for j in N if i != j]}
    #randomly assign jobs to customer locations    
    job_loc_assignment = {}
    customers = list(range(1,num_c+1))
    J_ = J.copy()
    random.shuffle(J_)
    counter = 0
    for j in J_:
        #selection = random.choice(customers)       
        job_loc_assignment[j] = customers[counter%num_c]  
        counter += 1
    job_loc_assignment[0] = 0
    t = {}
    for i in [0] + J:
        for j in [0] + J:
            if i!=j and job_loc_assignment[i] != job_loc_assignment[j]:
                t[(i,j)] = distances_locations[(job_loc_assignment[i],job_loc_assignment[j])]
            #if both jobs are assigned to the same site then the distance is 0
            if(job_loc_assignment[i] == job_loc_assignment[j]):
                t[(i,j)] = 0
    w_lower = {j: math.ceil(np.random.uniform(2 * Rho, 3 * Rho)) for j in J}
    w_upper = {j: w_lower[j] + math.ceil(np.random.uniform(0, 0.5 * Rho)) for j in J}
    data_collection = {}    
    data_collection["V"] = V
    data_collection["J"] = J
    data_collection["M"] = M 
    data_collection["p"] = p    
    data_collection["u"] = u    
    data_collection["c"] = c
    data_collection["s"] = s
    data_collection["r"] = r    
    data_collection["q"] = q
    data_collection["r_hat"] = r_hat
    #this dict has tuple as keys and json doesnt support this...
    t_new = {}
    for e in t:
        t_new[str(e)] = t[e]
    data_collection["t"] = t_new
    data_collection["w_lower"] = w_lower
    data_collection["w_upper"] = w_upper    
    #Nonessential data...
    #number of physical locations 0 being the production site
    data_collection["N"] = N
    #there might be multiple orders per location/customer
    data_collection["job_loc_assignment"] = job_loc_assignment    
    data_collection["xc"] = xc
    data_collection["yc"] = yc

    with open(f"./instances/{num_c}c{num_j}j{num_m}m{num_v}v___{Rho}Rho{mu}Mu{delta}delta/#{num_instance}___{num_c}c{num_j}j{num_m}m{num_v}v___{Rho}Rho{mu}Mu{delta}delta.json", 'w') as f:
        json.dump(data_collection, f)
    return data_collection

def create_folder_for_instance_batch(num_c = 3,num_j = 10, num_m =2, num_v = 2,\
                                     Rho = 10, mu = 3, delta = 200):
    path = os.getcwd()
    try:
        os.mkdir(path +"\instances")
    except OSError:
        print ("Creation of the directory %s failed" % path)
    else:
        print ("Successfully created the directory %s " % path)
    print("__________________________________\n")
    
    # define the name of the directory to be created
    try:
        os.mkdir(path +f"\instances\{num_c}c{num_j}j{num_m}m{num_v}v___{Rho}Rho{mu}Mu{delta}delta")
    except OSError:
        print ("Creation of the directory %s failed" % path)
    else:
        print ("Successfully created the directory %s " % path)
if __name__ == "__main__":
    x1 = create_folder_for_instance_batch(num_c = 4, num_j = 15, num_m=2,\
                                          num_v = 2, Rho = 10, mu = 3, delta = 200)
    x = generateInstance(num_instance= 1,num_c = 3, num_j = 8, num_m=2,\
                         num_v = 2, Rho = 10, mu = 3, delta = 200, fixed_seed = False)