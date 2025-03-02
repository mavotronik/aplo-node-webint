from flask import Flask, render_template, request, jsonify
import threading
import time
import psutil
import datetime
import os

from web3 import Web3

app = Flask(__name__)

cpu = 0
ram = 0
uptime = ""
current_block = 0
current_difficulty = 0
transactions = 0
active_peers = 0
blockchain_size = 0
block_time = 0 

w3 = Web3(Web3.HTTPProvider('http://192.168.1.22:8545'))
w3_connected = w3.is_connected()
print(w3_connected)


def sys_stats():
    global cpu
    global ram
    global uptime
    while True: 
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory()
        ram = float(ram.percent)
        uptime = datetime.timedelta(seconds=time.time() - psutil.boot_time())
        
        time.sleep(5)

def node_stats():
    global current_block
    global current_difficulty
    global active_peers
    global blockchain_size
    global block_time

    while True:
        block = w3.eth.get_block('latest')
        current_block = block.number
        current_difficulty = block.difficulty
        active_peers = w3.net.peer_count

        blockchain_size = os.popen("du -sh ~/AploNode-data/geth | awk '{print $1}'").read().strip()
        
        block_time = block.timestamp
        block_time = datetime.datetime.utcfromtimestamp(block_time)
        #print(current_block, current_difficulty, active_peers, blockchain_size, block_time)

        time.sleep(1)


sys_stats_thread = threading.Thread(target=sys_stats)
sys_stats_thread.daemon = True
sys_stats_thread.start()

node_stats_thread = threading.Thread(target=node_stats)
node_stats_thread.daemon = True
node_stats_thread.start()

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/get_sys_stats', methods=['GET'])
def get_sys_stats():
    global cpu
    global ram
    global uptime
    return jsonify({'cpu_stat': cpu, 'ram_stat': ram, 'uptime_stat': str(uptime)})

@app.route('/get_node_stats', methods=['GET'])
def get_node_stats():
    global current_block
    global current_difficulty
    global active_peers
    global blockchain_size
    global block_time
    return jsonify({'current_block': current_block, 'current_difficulty': current_difficulty, 'active_peers': active_peers, 
                    'blockchain_size': str(blockchain_size), 'block_time': str(block_time)})

@app.route('/get_last_blocks', methods=['GET'])
def get_last_blocks():
    last_blocks = []
    latest_block = w3.eth.get_block('latest').number
    for i in range(5):
        block_data = w3.eth.get_block(latest_block - i)
        block_info = {
            "number": block_data.number,
            "timestamp": block_data.timestamp,
            "time_utc": str(datetime.datetime.utcfromtimestamp(block_data.timestamp))
        }
        last_blocks.append(block_info)
    return jsonify(last_blocks)


if __name__ == '__main__':
    app.run(debug=True)
