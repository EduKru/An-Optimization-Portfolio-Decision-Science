import heuristic_gurobi_solver as hs
import instance_and_solution_loading as isl
import random
import numpy as np

import time

def generate_Q_0(r,p,w_upper,job_loc_assignment,num_m = 2, num_c = 3):
    """
    1The jobs get grouped by customer. 
    2The average of the due date (w_upper) gets calculated for the job groups.
    3a group with the lowest average gets picked and removed from the grouplist
    until no more groups are there
    4jobs are put on a queue in that order
    example : Q= [1, 4, 5, 3, 6, 8, 2, 7]
    """
    customer_jobs = {}
    for i in range(1,num_c+1):
        customer_jobs[i] = []
    for j in job_loc_assignment:
        if j != 0:
            customer_jobs[job_loc_assignment[j]].append(j)
    avg_duedate = {}
    for c in customer_jobs:
        sum_duedates = 0
        for j in customer_jobs[c]:
            sum_duedates += w_upper[j]
        avg_duedate[c] = sum_duedates / len(customer_jobs[c])    
    job_queue = []
    while len(avg_duedate) > 0:
        urg_c = min(avg_duedate, key=avg_duedate.get)
        arr = customer_jobs[urg_c]
        arr.sort()
        job_queue += arr
        del avg_duedate[urg_c]
    return job_queue

def Q_to_S(Q,r, p, num_m = 2):
    """
    example: Q= [1, 4, 5, 3, 6, 8, 2, 7]
    returns {1: [1, 5, 6, 8], 2: [4, 3, 2, 7]}
    """
    machine_occup = np.zeros(num_m)    
    for m in r:
        machine_occup[m-1] = r[m]
    machine_job_order = {}
    for m in range(1,num_m+1):
        machine_job_order[m] = []     
    for idx in range(0,len(Q)):
        lowest_occ_m = np.argmin(machine_occup)
        machine_job_order[lowest_occ_m + 1].append(Q[idx])
        machine_occup[lowest_occ_m] += p[Q[idx]]
    return machine_job_order

def compute_ASAP_delivery_times(J,r,p,r_hat,t):
    ASAP_delivery_times = {}
    for j in J:
        E_processing = min(r.values()) + p[j]
        E_departure = max(E_processing, min(r_hat.values()))
        ASAP_delivery = E_departure + t[(0,j)]
        ASAP_delivery_times[j] = ASAP_delivery
    return ASAP_delivery_times

def moveJobInQueue(Q, sel_job, step):
    Q_copy = Q.copy()
    for idx, j in enumerate(Q_copy):
        if j == sel_job:
            del Q_copy[idx]
            Q_copy.insert(idx-step, j)
    return Q_copy


def solve_with_IIH(numInstance = 1, numC = 3, numJ = 8, numM = 2,\
                   numV = 2, r = 10, m = 3, d = 200):
    V,J,M,p,u,c,s,r,  q,r_hat,t,w_lower, \
    w_upper,N,job_loc_assignment,xc,yc = isl.load_problem_instance(num_instance= numInstance,\
                          num_c = numC, num_j = numJ, num_m= numM,\
                          num_v = numV, Rho = r, mu = m, delta = d)
    
    t_start = time.time()
    
    #---------------initialization phase---------------#
    Q_0 = generate_Q_0(r,p,w_upper,job_loc_assignment,num_m = 2, num_c = 3)
    S_0 = Q_to_S(Q_0,r, p, num_m = 2)
    x,y = hs.job_order_to_xybinaries(S_0)
    sol_dict = hs.load_X_Y_ProblemAndSolveRouting(x,y,num_instance= 1,num_c = 3,\
                                                  num_j = 8, num_m=2,\
                          num_v = 2, Rho = 10, mu = 3, delta = 200)
    
    Q_best = Q_0
    S_best = S_0
    obj_best = sol_dict["objval"]
    _Q_visited = []
    _Q_visited.append(Q_0)
    
    ##---------track progress of every iteration------#
    counter = 0
    iter_dict = {}
    iter_dict[counter] = obj_best
    
    
    ASAP = compute_ASAP_delivery_times(J,r,p,r_hat,t)
    #-------------iterative improvement--------------------#
    while True:
        _Q_Q_best = []
    #---------evaluate jobs based on possible improvement gap--#
        IMPR = {}
        for j in J:
            IMPR[j] = sol_dict["D"][j] - ASAP[j]
    #-------------select job for the moves -----------#        
        J_Selection = []
        for m in M:
            sel_job = max(IMPR, key=IMPR.get)
            J_Selection.append(sel_job)
            del IMPR[sel_job]
    #------------create neighborhood------------------#        
        for j in J_Selection:
            for m in M:
                Q_new = moveJobInQueue(Q_best,j,m)
                if Q_new not in _Q_visited:
                    _Q_visited.append(Q_new)
                    _Q_Q_best.append(Q_new)
        _S_S_best = []
        for Q in _Q_Q_best:
            S_0 = Q_to_S(Q, r, p, num_m = 2)
            _S_S_best.append(S_0)
    #------------compute obj val. for neighbors ------#        
        sols = []
        for S in _S_S_best:
            x,y = hs.job_order_to_xybinaries(S)
            sol_dict = hs.load_X_Y_ProblemAndSolveRouting(x,y,num_instance= 1,\
                          num_c = 3, num_j = 8, num_m=2,\
                          num_v = 2, Rho = 10, mu = 3, delta = 200)
                
            sols.append(sol_dict["objval"])
    #------------check for improved obj. val---------#
        t_end = time.time()    
        solving_time = t_end - t_start
    
        if min(sols) < obj_best:
               idx_min_sol = np.argmin(sols)
               obj_best = min(sols)
               S_best = _S_S_best[idx_min_sol]
               Q_best = _Q_Q_best[idx_min_sol]
               counter += 1
               iter_dict[counter] = obj_best
               if solving_time > 50:
                   break
        else:
            break

    
    return obj_best, solving_time
    
    
    
    
    









