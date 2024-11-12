# Initialize matrix

```
name_matrix = [3, 1, 0, 2]
value_matrix = [[0, 0, 0, 0],
                [1/10, 0, 0, 1/15],
                [0, 1/10, 0, 1/5],
                [1/10, 0, 0, 0]
                ]
```

# Calculate the maximum flow from source (0) to sink (3)

```
mpm = MPM().pre_process(name_matrix, value_matrix)
max_flow = mpm.flow()
output_matrix = mpm.post_process(name_matrix, value_matrix)
```

# Expected output

```
print("The maximum flow from node 0 to node 3 is:", max_flow)
for i in range(len(output_matrix)):
print(output_matrix[i])
```
