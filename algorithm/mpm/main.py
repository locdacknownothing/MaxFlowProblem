import numpy as np
from mpm import MPM 

if __name__ == "__main__":
    # value_matrix = [[0, 10, 5, 0],
    #             [0, 0, 15, 10],
    #             [0, 0, 0, 10],
    #             [0, 0, 0, 0]
    #             ]
    # start = 0
    # sink = 3
    value_matrix = np.load("data\\results\\sample_adj_matrix.npy").tolist()
    start, sink = 0, 5

    mpm = MPM().pre_process(start, sink, value_matrix)
    max_flow = mpm.flow()
    output_matrix = mpm.post_process(value_matrix)

    print("Max flow:", max_flow)
    for i in range(len(output_matrix)):
        print(output_matrix[i])
