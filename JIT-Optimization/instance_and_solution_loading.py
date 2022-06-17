import json
import pickle
def load_problem_instance(num_instance=1, num_c = 5, num_j = 8, num_m = 2,\
                          num_v = 1, Rho = 10, mu = 3, delta = 200):
    with open(f"./instances/{num_c}c{num_j}j{num_m}m{num_v}v___" +
              f"{Rho}Rho{mu}Mu{delta}delta/#{num_instance}___" + 
              f"{num_c}c{num_j}j{num_m}m{num_v}v___"+
              f"{Rho}Rho{mu}Mu{delta}delta.json") as json_file:
        data = json.load(json_file)
    data2 = {}        
    for e in data:
        if type(data[e]) is dict and e != "t":
            d = {int(k):int(v) for k,v in data[e].items()}
            data2[e] = d
            #exec(f"{e} = {d}")        
        elif f"{e}" == "t":
            global t
            t = data["t"]
            data2[e] = t
        else:
            exec(f"{e} = {data[e]}")
            data2[e] = data[e]   
    #convert back to tuple-key from a string-key        
    t_new = {}
    for e in t:
        left, right = e.split(",")
        ex = (int(left[1:]), int(right[:-1]))
        t_new[ex] = t[e]      
    t = t_new
    data2["t"] = t
    return data2.values()
def load_problem_solution(num_instance=1, num_c = 3, num_j = 6, num_m = 2,\
                          num_v = 2, Rho = 10, mu = 3, delta = 200,\
                              pathaddition = ""):    
    with open(f"./instances/{num_c}c{num_j}j{num_m}m{num_v}v___" +
              f"{Rho}Rho{mu}Mu{delta}delta/#{num_instance}___" + 
              f"{num_c}c{num_j}j{num_m}m{num_v}v___"+
              f"{Rho}Rho{mu}Mu{delta}"+
              f"delta_SOLUTION{pathaddition}.pickle",'rb') as handle:
        data = pickle.load(handle)
    return data.values()
if __name__ == "__main__":
    #V,J,M,p,u,c,s,r,  q,r_hat,t,w_lower, \
    #w_upper,N,job_loc_assignment,xc,yc = load_problem_instance()
    """
    D,C,T,S,x,y,z,g,runTime,gap,objval,vehicle_tours_customerbased_tour_cluster,\
        job_order_machines, job_tour_map = load_problem_solution(num_instance=5,\
                                        num_c = 3,num_j = 8,num_m = 2,num_v = 2,\
                                                  pathaddition = "_1stHeuristic")
"""
    V,J,M,p,u,c,s,r,  q,r_hat,t,w_lower, w_upper,N,job_loc_assignment,xc,yc  =\
        load_problem_instance(num_instance= 1,num_c = 4, num_j = 8, num_m=2,num_v = 1)                                                                
        


    