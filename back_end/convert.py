import numpy as np 

def adj_matrix2edges(matrix): 
    try:
        print(np.array(matrix))
    except:
        pass
    
    edges = []

    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] != 0:
                edges.append({
                    "src": i,
                    "dst": j,
                    "capacity": str(matrix[i][j])
                })

    return edges
