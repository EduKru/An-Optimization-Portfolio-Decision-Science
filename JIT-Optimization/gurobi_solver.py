import instance_and_solution_loading

def loadAndSolve(num_instance=1, num_c = 3,num_j = 15, num_m = 2,\
                                                        num_v = 2, Rho = 10,\
                                                            mu = 3, delta = 200,\
                                                            TimeLimit = 280):
    ##Loading instance data from json
    V,J,M,p,u,c,s,r,  q,r_hat,t,w_lower,w_upper,N,job_loc_assignment,\
    xc,yc = instance_and_solution_loading.load_problem_instance(num_instance, num_c,\
                                                        num_j, num_m,\
                                                            num_v, Rho,\
                                                                mu, delta)
    ##Solving the problem instance
    #MIP from chapter 4.2
    from gurobipy import Model, GRB, quicksum
    mdl = Model("ISVRPTW")
    mdl.setParam('TimeLimit', TimeLimit)
    C = mdl.addVars(J, vtype = GRB.CONTINUOUS, name= 'C')
    D = mdl.addVars(J, vtype = GRB.CONTINUOUS, name= 'D')
    S = mdl.addVars(V,J,vtype = GRB.CONTINUOUS, name= 'S')
    T = mdl.addVars(J,vtype = GRB.CONTINUOUS, name= 'T')
    x = mdl.addVars([(i,j) for i in J for j in J +[len(J) + 1] if i != j],\
                    vtype=GRB.BINARY, name = "x") #4.2.5
    y = mdl.addVars(M, J, vtype=GRB.BINARY, name = "y") #4.2.3
    g = mdl.addVars(J + [0] ,V,J, vtype=GRB.BINARY, name = "g") #4.2.10
    mdl.modelSense = GRB.MINIMIZE
    
    mdl.setObjective(quicksum(T[j] for j in J)) #4.2.1
    mdl.addConstrs(quicksum(y[m,j] for j in J) <= 1 for m in M); #4.2.2
    mdl.addConstrs(quicksum(x[j,i] for i in J + [len(J)+1] if i!=j) == 1 for j in J); #4.2.4
    
    mdl.addConstrs(quicksum(y[m,j] for m in M) + \
                   quicksum(x[i,j] for i in J if i!=j)  == 1 for j in J); #4.2.6
        
    mdl.addConstrs( C[j] >= y[m,j]*(r[m]+p[j]) for j in J for m in M);  #4.2.7
    
    mdl.addConstrs( C[j] >= C[i] + p[j] - q*(1 - x[i,j]) for i in J for j in J if i != j); #4.2.8
    
    mdl.addConstrs( 1 == quicksum(g[j,v,t] for v in V for t in J ) for j in J); #4.2.9
    
    mdl.addConstrs( g[0,v,t] >= g[j,v,t] for j in J for v in V for t in J); #4.2.11
    
    mdl.addConstrs( q * quicksum(g[j,v,t] for j in J) >= \
                   quicksum(g[j,v,t+1] for j in J) for v in V for t in J[:-1] ); #4.2.12
    
    z = mdl.addVars(J+[0], J+[0] ,V, J, vtype=GRB.BINARY, name= 'z') #4.2.15
    
    mdl.addConstrs( g[j,v,t] == quicksum(z[i,j,v,t] for i in [0] + J if i!=j) \
                   for j in J + [0] for v in V for t in J );#4.2.13
    
    mdl.addConstrs( g[j,v,t] == quicksum(z[j,i,v,t] for i in [0] + J if i!=j)\
                   for j in J + [0] for v in V for t in J );#4.2.14
    
    mdl.addConstrs( c[v] >= quicksum(u[j] * g[j,v,t]\
                                     for j in J) for v in V for t in J); #4.2.16
    
    mdl.addConstrs( S[v,1] >= r_hat[v]  + s[0] for v in V); #4.2.17
    
    mdl.addConstrs( S[v,t] >= C[j]  + s[0] - q * (1 - g[j,v,t]) \
                   for j in J for v in V for t in J ); #4.2.18
    
    mdl.addConstrs( S[v,i+1] >= D[j] + s[j] + t[j,0] + s[0] - q * (1-g[j,v,i])\
                   for j in J for v in V for i in J[:-1] ); #4.2.19
    
    mdl.addConstrs( D[j] >= w_lower[j] for j in J); #4.2.20
    mdl.addConstrs( D[j]  >= S[v,i] + t[0,j] - q*(1 - g[j,v,i]) \
                   for j in J for v in V for i in J); #4.2.21
        
    mdl.addConstrs( D[j] >=  D[i] + s[i] + t[i,j] - q * (1 - z[i,j,v,k]) \
                   for i in J for j in J if i!=j for v in V for k in J); #4.2.22
        
    mdl.addConstrs(T[j] >= 0 for j in J); #4.2.23
    mdl.addConstrs(T[j] >= D[j] - w_upper[j] for j in J); #4.2.24
    mdl.optimize()
    #mdl.write("mip.lp");    
    path = f"./instances/{num_c}c{num_j}j{num_m}m{num_v}v___" +\
    f"{Rho}Rho{mu}Mu{delta}delta/#{num_instance}___" +\
    f"{num_c}c{num_j}j{num_m}m{num_v}v___" +\
    f"{Rho}Rho{mu}Mu{delta}delta_"    
    mdl.write(path + "puregurobi.sol")  
      
    sol_dict = {}
    sol_dict["D"] = {id:D[id].X for id in D}
    sol_dict["C"] = {id:C[id].X for id in C}
    sol_dict["T"] = {id:T[id].X for id in T}
    sol_dict["S"] = {id:S[id].X for id in S}    
    sol_dict["x"] = {id:x[id].X for id in x}
    sol_dict["y"] = {id:y[id].X for id in y}
    sol_dict["z"] = {id:z[id].X for id in z}
    sol_dict["g"] = {id:g[id].X for id in g}
    sol_dict["runTime"]  = mdl.Runtime
    sol_dict["gap"] = mdl.MIPGap
    sol_dict["objval"] = mdl.ObjVal
        
    path = f"./instances/{num_c}c{num_j}j{num_m}m{num_v}v___" +\
        f"{Rho}Rho{mu}Mu{delta}delta/#{num_instance}___" +\
        f"{num_c}c{num_j}j{num_m}m{num_v}v___" +\
        f"{Rho}Rho{mu}Mu{delta}delta_SOLUTION"

    #--------------saving solution dictionary as .pickle file------------#
    import pickle
    with open(path +'.pickle', 'wb') as handle:
        pickle.dump(sol_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
    return sol_dict
    
if __name__ == "__main__":
    sol_dict = loadAndSolve(num_instance= 1,num_c = 3, num_j = 8, num_m=2,\
                         num_v = 2, Rho = 10, mu = 3, delta = 200)
    import heuristic_gurobi_solver as hs
    sched = hs.xybinaries_to_job_order(sol_dict["x"], sol_dict["y"])
    
    
