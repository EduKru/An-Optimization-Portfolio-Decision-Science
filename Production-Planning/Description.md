implementation gurobi/anaconda python/jypiter notebook
1. pip install -i https://pypi.gurobi.com gurobipy (anaconda prompt)


![image](https://user-images.githubusercontent.com/29587190/150485879-cc85d450-a78b-4f31-b543-4682ca7c396e.png)

This supply chain setup can be modeled in the following way:

![image](https://user-images.githubusercontent.com/29587190/150771323-504572e0-3862-4220-b49b-1fa584be5a33.png)

- (1): The objective function consists of production-, remanufacturing-, setup-, storage-, substituion-, order-cost.
- (2): Constraints control the inventory in the raw material storage.
- (3), (4), (5): are more constraints which control the inventory levels in the storages for newly produced, remanufactured and returned products.
- (6), (7): Constraints make sure the machine capacities are not exceeded
- (8), (9): are Big-M-Constraints which chain the binary setup-variable and the production-amount-variables together
- (10) make sure that period-vise emissions aren't exceeded through production
- (11) is an alternative emission constraint which considers the whole planning horizon
- (12) - (14) are constraints which allow at most one choice of discount level. Also order quantitiy is chained to the discount level.
- (15), (16) sets variables to either non-negative or binary

![image](https://user-images.githubusercontent.com/29587190/150771491-c9d08a6d-19b6-408f-8f0d-d2ea879333c6.png)


