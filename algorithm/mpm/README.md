# Initialize matrix

```
value_matrix = [[0, 10, 5, 0],
                [0, 0, 15, 10],
                [0, 0, 0, 10],
                [0, 0, 0, 0]
                ]
start = 0
sink = 3
```

# Calculate the maximum flow from source (0) to sink (3)

```
mpm = MPM().pre_process(start, sink, value_matrix)
max_flow = mpm.flow()
output_matrix = mpm.post_process(value_matrix)
```

# Expected output

```
print("The maximum flow from node 0 to node 3 is:", max_flow)
for i in range(len(output_matrix)):
    print(output_matrix[i])
```
