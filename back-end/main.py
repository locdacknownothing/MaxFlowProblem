from flask import Flask
from binary_blocking_flow import binary_blocking_flow
from algorithm.mpm import mpm
from algorithms.ford_fulkerson import capacity_scaling, edmonds_karp, ford_fulkerson
from push_relabel_with_fifo import fifo_push_relabel_adj_list, fifo_push_relabel_adj_matrix

app = Flask(__name__)


@app.route('/')
def home():
    return "Hello, Flask!"

if __name__ == '__main__':
    app.run(debug=True)
