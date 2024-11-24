import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json 
from copy import deepcopy 

from flask import Flask, request, jsonify
from flask_cors import CORS 
import numpy as np

from binary_blocking_flow import binary_blocking_flow
from algorithm.mpm import mpm
from algorithms.ford_fulkerson import capacity_scaling, edmonds_karp, ford_fulkerson
from push_relabel_with_fifo import fifo_push_relabel_adj_matrix
from back_end.convert import adj_matrix2edges 

app = Flask(__name__)
CORS(app)

node_data = "front-end/src/data/manual_node_data.json"
edge_data = "front-end/src/data/manual_edge_data.json"

mapDataPath = './data/results/manual_adj_matrix.npy'
mapData = np.load(mapDataPath).tolist()

testMapDataPath = './data/results/sample_adj_matrix.npy'
testMapData = np.load(testMapDataPath).tolist()


@app.route('/')
def home():
    return "Hello, Flask!"

@app.route('/nodes')
def get_nodes(): 
    """
    Get all nodes in the graph.

    Returns:
        200: A JSON object where each key is a node ID and each value is a dictionary
            with the 'lat' and 'lon' of the node.
        404: If no nodes are found.
        500: If an error occurs, a JSON object with an 'error' key and a string value
            describing the error.
    """
    try:
        with open(node_data) as f:
            data = json.load(f)
        return jsonify(data), 200 if data else 404
    except Exception as e:
        # Handle exceptions and return an error message
        return jsonify({"error": str(e)}), 500
    
@app.route('/edges')
def get_edges():
    """
    Get all edges in the graph.

    Returns:
        200: A JSON object where each key is an edge ID and each value is a dictionary
            with the 'src' and 'dst' nodes, and the 'capacity' of the edge.
        404: If no edges are found.
        500: If an error occurs, a JSON object with an 'error' key and a string value
            describing the error.
    """
    
    try:
        with open(edge_data) as f:
            data = json.load(f)
        return jsonify(data), 200 if data else 404 
    except Exception as e:
        # Handle exceptions and return an error message
        return jsonify({"error": str(e)}), 500
    
@app.route('/node')
def get_node_by_index():
    """
    Get a node by its index.

    Args:
        index (int): The index of the node to retrieve.

    Returns:
        200: A JSON object with the 'node_id', 'lat', and 'lon' of the node.
        404: If no node is found with the given index.
        500: If an error occurs, a JSON object with an 'error' key and a string value
            describing the error.
    """

    try:
        with open(node_data) as f:
            data = json.load(f) 

        index = request.args.get('index')
        node = [node for node in data if node["index"] == int(index)]
        if not node:
            return jsonify({"message": "Node not found"}), 200
        else:
            return jsonify(node[0]), 200
    except Exception as e:
        # Handle exceptions and return an error message
        return jsonify({"error": str(e)}), 500

@app.route('/edge')
def get_edge_by_src_dst():
    """
    Get an edge by its source and destination nodes.

    Args:
        src (int): The source node ID of the edge to retrieve.
        dst (int): The destination node ID of the edge to retrieve.

    Returns:
        200: A JSON object with the 'src', 'dst', and 'capacity' of the edge.
        404: If no edge is found with the given source and destination nodes.
        500: If an error occurs, a JSON object with an 'error' key and a string value
            describing the error.
    """
    try:
        with open(edge_data) as f:
            data = json.load(f)

        src = request.args.get('src')
        dst = request.args.get('dst')
        edge = [edge for edge in data if edge["src"] == int(src) and edge["dst"] == int(dst)]
        if not edge:
            return jsonify({"message": "Edge not found"}), 200
        else: 
            return jsonify(edge[0]), 200
    except Exception as e:
        # Handle exceptions and return an error message
        return jsonify({"error": str(e)}), 500

@app.route('/ford_fulkerson', methods=['POST'])
def executeFordFulkerson():
    """
    Execute the Ford-Fulkerson algorithm on the graph.

    Args:
        source (int): The source node ID.
        sink (int): The sink node ID.

    Returns:
        200: A JSON object with the 'MaximumFlow' and 'edges' of the result.
        400: If no 'source' or 'sink' is provided.
        500: If an error occurs, a JSON object with an 'error' key and a string value
            describing the error.
    """

    data = request.get_json()
    
    if 'source' not in data or 'sink' not in data:
        return jsonify({"error": "Please provide both 'source' and 'sink' values."}), 400
    
    source = int(data['source'])
    sink = int(data['sink'])

    testOnly = data.get('test', 0)
    map_data = testMapData if testOnly else mapData 
    map_data = deepcopy(map_data) 

    g = ford_fulkerson.Graph(len(map_data), map_data)
    matrix = g.create_result_graph()
    edges = adj_matrix2edges(matrix)
    
    try:
        response = {
            "MaximumFlow": int(g.ford_fulkerson(source, sink)),
            # "ResultMatrix": matrix,
            "edges": edges,
        }
        return jsonify(response), 200

    except Exception as e:
        # Handle exceptions and return an error message
        return jsonify({"error": str(e)}), 500

@app.route('/edmonds_karp', methods=['POST'])
def executeEdmondsKarp():
    """
    Execute the Edmonds-Karp algorithm on the graph.

    Args:
        source (int): The source node ID.
        sink (int): The sink node ID.

    Returns:
        200: A JSON object with the 'MaximumFlow' and 'edges' of the result.
        400: If no 'source' or 'sink' is provided.
        500: If an error occurs, a JSON object with an 'error' key and a string value
            describing the error.
    """
    data = request.get_json()
    
    if 'source' not in data or 'sink' not in data:
        return jsonify({"error": "Please provide both 'source' and 'sink' values."}), 400
    
    source = int(data['source'])
    sink = int(data['sink']) 

    testOnly = data.get('test', 0)
    map_data = testMapData if testOnly else mapData 
    map_data = deepcopy(map_data) 

    g = edmonds_karp.Graph(len(map_data), map_data)
    matrix = g.create_result_graph()
    edges = adj_matrix2edges(matrix)

    try:
        response = {
            "MaximumFlow": int(g.edmonds_karp(source, sink)),
            # "ResultMatrix": matrix, 
            "edges": edges
        }
        return jsonify(response), 200

    except Exception as e:
        # Handle exceptions and return an error message
        return jsonify({"error": str(e)}), 500

@app.route('/capacity_scaling', methods=['POST'])
def executeCapacityScaling():
    """
    Execute the Capacity Scaling algorithm on the graph.

    Args:
        source (int): The source node ID.
        sink (int): The sink node ID.

    Returns:
        200: A JSON object with the 'MaximumFlow' and 'edges' of the result.
        400: If no 'source' or 'sink' is provided.
        500: If an error occurs, a JSON object with an 'error' key and a string value
            describing the error.
    """
    data = request.get_json()
    
    if 'source' not in data or 'sink' not in data:
        return jsonify({"error": "Please provide both 'source' and 'sink' values."}), 400
    
    source = int(data['source'])
    sink = int(data['sink'])

    testOnly = data.get('test', 0)
    map_data = testMapData if testOnly else mapData 
    map_data = deepcopy(map_data)
    
    g = capacity_scaling.Graph(len(map_data), map_data)
    matrix = g.create_result_graph()
    edges = adj_matrix2edges(matrix)
    
    try:
        response = {
            "MaximumFlow": int(g.capacity_scaling(source, sink)),
            # "ResultMatrix": matrix,
            "edges": edges
        }
        return jsonify(response), 200

    except Exception as e:
        # Handle exceptions and return an error message
        return jsonify({"error": str(e)}), 500

@app.route('/fifo_push_relabel', methods=['POST'])
def executeFifoPushRelabel():
    """
    Execute the FIFO Push-Relabel algorithm on the graph.

    Args:
        source (int): The source node ID.
        sink (int): The sink node ID.

    Returns:
        200: A JSON object with the 'MaximumFlow' and 'edges' of the result.
        400: If no 'source' or 'sink' is provided.
        500: If an error occurs, a JSON object with an 'error' key and a string value
            describing the error.
    """
    data = request.get_json()
    
    if 'source' not in data or 'sink' not in data:
        return jsonify({"error": "Please provide both 'source' and 'sink' values."}), 400
    
    source = int(data['source'])
    sink = int(data['sink'])

    testOnly = data.get('test', 0)
    map_data = testMapData if testOnly else mapData 
    map_data = deepcopy(map_data)

    fifo = fifo_push_relabel_adj_matrix.FifoPushRelabel(map_data, source, sink) 
    maxFlow = fifo.process()
    matrix = fifo.result_flow_graph() 
    edges = adj_matrix2edges(matrix)
    
    try:
        response = {
            "MaximumFlow": int(maxFlow),
            # "ResultMatrix": matrix,
            "edges": edges
        }
        return jsonify(response), 200

    except Exception as e:
        # Handle exceptions and return an error message
        return jsonify({"error": str(e)}), 500

@app.route('/mpm', methods=['POST'])
def executeMPM():
    req = request.get_json()
    
    if 'source' not in req or 'sink' not in req:
        return jsonify({"error": "Please provide both 'source' and 'sink' values."}), 400
    
    source = int(req['source'])
    sink = int(req['sink'])

    testOnly = req.get('test', 0)
    value_matrix = testMapData if testOnly else mapData 
    value_matrix = deepcopy(value_matrix)

    mpm_inst = mpm.MPM().pre_process(source, sink, value_matrix)
    max_flow = mpm_inst.flow()
    output_matrix = mpm_inst.post_process(value_matrix)
    edges = adj_matrix2edges(output_matrix)
    
    try:
        response = {
            "MaximumFlow": int(max_flow),
            "edges": edges,
        }
        return jsonify(response), 200
    
    except Exception as e:
        # Handle exceptions and return an error message
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
