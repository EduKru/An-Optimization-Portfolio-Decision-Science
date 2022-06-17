import instance_and_solution_loading
import json
import pickle
import matplotlib
import matplotlib.pyplot as plt
import math

def visualize_solution(num_instance=1, num_c = 5,num_j = 8, num_m = 2,\
                                                        num_v = 1, Rho = 10,\
                                                            mu = 3, delta = 200):
    #Loading problem instance/solution
    V,J,M,p,u,c,s,r,  q,r_hat,t,w_lower, \
    w_upper,N,job_loc_assignment,xc,yc = instance_and_solution_loading.load_problem_instance(num_instance, num_c, num_j, num_m,\
                          num_v, Rho, mu, delta)
    
    D,C,T,S,x,y,z,g,runTime,gap,objval,\
   w = instance_and_solution_loading.load_problem_solution(num_instance,\
                                                     num_c, num_j, num_m,\
                          num_v, Rho, mu, delta, "")
    
    ##Creating matplotlib visualization
    #----------------Loading color palette..------
    import matplotlib.colors as mcolors
    di = mcolors.CSS4_COLORS.copy()
    #removing bright colors from dict
    for k in mcolors.CSS4_COLORS:
        h  = mcolors.CSS4_COLORS[k]
        h = h.lstrip('#')
        di[k] = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
        if sum(di[k]) > 600:
            del di[k]
    
    #----------------Picking colors for jobs...-------
    import matplotlib.colors as mcolors
    fullcolorlist = [i for i in di]
    for i in fullcolorlist:
        if "grey" in i or "gray" in i:
            fullcolorlist.remove(i)
            
    tableaucolorlist = [i for i in mcolors.TABLEAU_COLORS]
    import random
    
    selected_c = []
    
    job_color_allocation = {}
    job_color_allocation[0] = "gray"
    for j in J:
        while True:
            if len(tableaucolorlist) > 0:
                sel = random.choice(tableaucolorlist)
                tableaucolorlist.remove(sel)
            
            sel = random.choice(fullcolorlist[j:int(len(fullcolorlist)/len(J))*j])
            if sel not in selected_c:
                break
        job_color_allocation[j] = sel
        selected_c.append(sel)
        fullcolorlist.remove(sel)
    #----------------------------------------------------
    import matplotlib.pyplot as plt
    import random
    # Declaring a figure "gnt"
    fig, gnt = plt.subplots()
    # Setting Y-axis limits
    gnt.set_ylim(0, len(M))
    # Setting labels for x-axis and y-axis
    gnt.set_xlabel('minutes since start')
    gnt.set_ylabel('machines')
    # Setting ticks on y-axis
    gnt.set_yticks([j*10 for j in M])
    # Labelling tickes of y-axis
    gnt.set_yticklabels([f"{j}" for j in M])
    # Setting graph attribute
    gnt.grid(True)
    for m in M:
        job_start_time = r[m]
        gnt.annotate((job_order_machines[m]), (40,10*m-5))
        for j in job_order_machines[m]:
            gnt.broken_barh([( C[j]-p[j], p[j])], (10*m-10, 9), facecolors =[job_color_allocation[j]])
            job_start_time += p[j]
     
    # Setting X-axis limits
    gnt.set_xlim(0, 100)    
    #------------------creation of labeling for tour edges------------
    tour_labels = {}
    for e in vehicle_tours_customerbased_tour_cluster:
        labels = []
        for s in vehicle_tours_customerbased_tour_cluster[e]:
            y = ""
            if len(s) == 1:
                y = f"{s[0][0]} -> {s[0][1]}"
            else:
                y = f"{s[0][0]} -> {s[0][1]}"
                for el in s[1:]:
                    y += f",{el[1]}"
            labels.append(y)
        tour_labels[e] = labels    
    
    #---------------creating a complete schedule-------------------------------------
    # Importing the matplotlib.pyplot
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    
    # Declaring a figure "gnt"
    fig, gnt = plt.subplots()
    
    obj = math.ceil(objval)
    rt = round(runTime, 4)
    g = round(gap, 4)*100
    p1 = mpatches.Patch(color='black', label= f'obj-value: {obj}')
    p2 = mpatches.Patch(color='black', label= f'cpu-time: {rt} s')
    p3 = mpatches.Patch(color='black', label= f'opt-gap: {g} %')
    
    plt.legend(handles=[p1,p2,p3])
    # Setting Y-axis limits
    gnt.set_ylim(0, 100)
    # Setting X-axis limits
    #gnt.set_xlim(0, 500)
    # Setting labels for x-axis and y-axis
    
    plt.title(f" instance: #{num_instance}___" + \
              f"{num_c}c{num_j}j{num_m}m{num_v}v___"+
              f"{Rho}Rho{mu}Mu{delta}delta")
    plt.rcParams.update({'font.size': 17})
    plt.rcParams["font.size"] = "17"
    gnt.set_xlabel('minutes since start')
    gnt.set_ylabel('machine schedule          /        vehicle schedule')
    # Setting ticks on y-axis
    gnt.set_yticks([v*10+5 for v in V])
    # Labelling tickes of y-axis
    gnt.set_yticklabels([f"{v}" for v in V])
    # Setting graph attribute
    gnt.grid(True)
    
    for vt in vehicle_tours_customerbased_tour_cluster:
        startTime = S[vt[0],vt[1]]
        counter = 0
        for subtour in vehicle_tours_customerbased_tour_cluster[vt]:
            
            for edge in subtour:   
                #set the vehicle line above the machine lines which is card(M)*10 + 10
                gnt.broken_barh([( startTime,  t[edge[0],edge[1]])], (10*vt[0] + len(M)*10+10, 9), facecolors =[job_color_allocation[edge[1]]])        
                #Routing ANNOTATION
                if t[edge[0],edge[1]] != 0:
                    gnt.annotate((f"{tour_labels[vt][counter]}"), (startTime,10*vt[0] + len(M)*10+10 +5)) 
                    counter += 1
                startTime += t[edge[0],edge[1]]

                
    for m in M:
        job_start_time = r[m]
        for j in job_order_machines[m]:
            gnt.broken_barh([( C[j]-p[j], p[j])], (10*m, 9), facecolors =[job_color_allocation[j]])
            job_start_time += p[j]
    
    #find last completion time of job for annotations after it..
    max_c_time = max([C[ic] for ic in C])
    for m in M:
        gnt.annotate((f"job order: {job_order_machines[m]}"), (max_c_time,10*m+5))    
        
    fig = matplotlib.pyplot.gcf()
    fig.set_size_inches(18.5, 10.5)
    
    x = f"#{num_instance}___" +\
        f"{num_c}c{num_j}j{num_m}m{num_v}v___"+\
            f"{Rho}Rho{mu}Mu{delta}delta.png"
    
    fig.savefig(x, dpi=100)
    
    # Declaring a figure "gnt"
    fig, gnt = plt.subplots()

    # Setting Y-axis limits
    gnt.set_ylim(0, len(M))
    # Setting labels for x-axis and y-axis
    gnt.set_xlabel('minutes since start')
    gnt.set_ylabel('machines')
    # Setting ticks on y-axis
    gnt.set_yticks([j*10 for j in M])
    # Labelling tickes of y-axis
    gnt.set_yticklabels([f"{j}" for j in M])
    # Setting graph attribute
    gnt.grid(True)
    for m in M:
        job_start_time = r[m]
        gnt.annotate((job_order_machines[m]), (40,10*m-5))
        for j in job_order_machines[m]:
            gnt.broken_barh([( C[j]-p[j], p[j])], (10*m-10, 9), facecolors =[job_color_allocation[j]])
            job_start_time += p[j]    

    fig = matplotlib.pyplot.gcf()
    fig.set_size_inches(18.5, 10.5)
    
    x = f"#{num_instance}___" +\
        f"{num_c}c{num_j}j{num_m}m{num_v}v___"+\
            f"{Rho}Rho{mu}Mu{delta}delta_machine_schedule.png"
    
    fig.savefig(x, dpi=100)
    
    
    
if __name__ == "__main__":

    #visualize_solution(num_instance= 1,num_c = 4, num_j = 15, num_m=2, num_v = 2, delta=200)
    visualize_solution(num_instance= 1,num_c = 5, num_j = 6, num_m=2, num_v = 1)
    