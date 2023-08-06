from solver import tsp_solver
import numpy as np 
import time 

nodes = 500
cost_mat = np.random.randint(100, size=(nodes, nodes))
cost_mat += cost_mat.T
np.fill_diagonal(cost_mat, 0)
dist_matrix = cost_mat.astype(np.float64).tolist()
start = time.time()
route, length = tsp_solver(dist_matrix)
print(f"Found route of length {length} in {time.time() - start} seconds.")

