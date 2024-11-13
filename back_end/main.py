from flask import Flask, request, jsonify
from flask_cors import CORS
from binary_blocking_flow import binary_blocking_flow
from algorithm.mpm import mpm
from algorithms.ford_fulkerson import capacity_scaling, edmonds_karp, ford_fulkerson
from push_relabel_with_fifo import fifo_push_relabel_adj_matrix
import numpy as np

app = Flask(__name__)
CORS(app)

mapDataPath = 'data/results/adj_matrix3.npy'
mapData = np.load(mapDataPath)

@app.route('/')
def home():
    return "Hello, Flask!"

@app.route('/ford_fulkerson', methods=['POST'])
def executeFordFulkerson():
    data = request.get_json()
    
    if 'source' not in data or 'sink' not in data:
        return jsonify({"error": "Please provide both 'source' and 'sink' values."}), 400
    
    source = data['source']
    sink = data['sink']

    g = ford_fulkerson.Graph(len(mapData), mapData)
    
    try:
        response = {
            "MaximumFlow": g.ford_fulkerson(source, sink).item(),
            "ResultMatrix": g.create_result_graph() 
        }
        return jsonify(response), 200

    except Exception as e:
        # Handle exceptions and return an error message
        return jsonify({"error": str(e)}), 500

@app.route('/edmonds_karp', methods=['POST'])
def executeEdmondsKarp():
    data = request.get_json()
    
    if 'source' not in data or 'sink' not in data:
        return jsonify({"error": "Please provide both 'source' and 'sink' values."}), 400
    
    source = data['source']
    sink = data['sink']

    g = edmonds_karp.Graph(len(mapData), mapData)
    
    try:
        response = {
            "MaximumFlow": g.edmonds_karp(source, sink).item(),
            "ResultMatrix": g.create_result_graph() 
        }
        return jsonify(response), 200

    except Exception as e:
        # Handle exceptions and return an error message
        return jsonify({"error": str(e)}), 500

@app.route('/capacity_scaling', methods=['POST'])
def executeCapacityScaling():
    data = request.get_json()
    
    if 'source' not in data or 'sink' not in data:
        return jsonify({"error": "Please provide both 'source' and 'sink' values."}), 400
    
    source = data['source']
    sink = data['sink']

    g = capacity_scaling.Graph(len(mapData), mapData)
    
    try:
        response = {
            "MaximumFlow": g.capacity_scaling(source, sink).item(),
            "ResultMatrix": g.create_result_graph() 
        }
        return jsonify(response), 200

    except Exception as e:
        # Handle exceptions and return an error message
        return jsonify({"error": str(e)}), 500

@app.route('/fifo_push_relabel', methods=['POST'])
def executeFifoPushRelabel():
    data = request.get_json()
    
    if 'source' not in data or 'sink' not in data:
        return jsonify({"error": "Please provide both 'source' and 'sink' values."}), 400
    
    source = data['source']
    sink = data['sink']

    maxFlow = fifo_push_relabel_adj_matrix.FifoPushRelabel(mapData, source, sink)
    
    try:
        response = {
            "MaximumFlow": maxFlow.process().item(),
            "ResultMatrix": maxFlow.result_flow_graph() 
        }
        return jsonify(response), 200

    except Exception as e:
        # Handle exceptions and return an error message
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
