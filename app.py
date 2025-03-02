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
prev_difficulty = 0
prev_peers = 0
prev_blockchain_size = "0B"
difficulty_change = 0
peers_change = 0
size_change = "N/A"
prev_difficulty_change = 0
prev_peers_change = 0
prev_size_change = 0

w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
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
    global current_block, current_difficulty, active_peers, blockchain_size, block_time
    global prev_difficulty, prev_peers, prev_blockchain_size
    global difficulty_change, size_change, peers_change
    global prev_difficulty_change, prev_peers_change, prev_size_change
    
    while True:
        block = w3.eth.get_block('latest')
        current_block = block.number
        current_difficulty = block.difficulty
        active_peers = w3.net.peer_count

        blockchain_size = os.popen("du -sh ~/AploNode-data/geth | awk '{print $1}'").read().strip()
        
        block_time = block.timestamp
        block_time = datetime.datetime.utcfromtimestamp(block_time)
        print(f"Current block: {current_block}, Current Difficulty: {current_difficulty}, Active peers: {active_peers}, Blockchain Size: {blockchain_size}, Block Time: {block_time}")

        # Calculate differences
        difficulty_change = ((current_difficulty - prev_difficulty) / prev_difficulty) * 100 if prev_difficulty else 0
        peers_change = ((active_peers - prev_peers) / prev_peers) * 100 if prev_peers else 0

        # Convert size to Gb
        current_size_gb = convert_size_to_gb(blockchain_size)
        prev_size_gb = convert_size_to_gb(prev_blockchain_size)

        size_change = ((current_size_gb - prev_size_gb) / prev_size_gb) * 100 if prev_size_gb > 0 else 0

        # Save not 0 changes only
        if difficulty_change != 0:
            prev_difficulty_change = difficulty_change
        if peers_change != 0:
            prev_peers_change = peers_change
        if size_change != 0:
            prev_size_change = size_change

        # Update previous
        prev_difficulty = current_difficulty
        prev_peers = active_peers
        prev_blockchain_size = blockchain_size

        print(f"Difficulty change: {difficulty_change:.2f}%, Peers change: {peers_change:.2f}%, Size change: {size_change:.2f}%")
        
        time.sleep(1)

def convert_size_to_gb(size_str):

    size_str = size_str.upper()
    
    if "G" in size_str:
        return float(size_str.replace("G", ""))
    elif "M" in size_str:
        return float(size_str.replace("M", "")) / 1024
    elif "T" in size_str:
        return float(size_str.replace("T", "")) * 1024
    else:
        return 0


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
    global current_block, current_difficulty, active_peers, blockchain_size, block_time
    global difficulty_change, size_change, peers_change

    return jsonify({'current_block': current_block, 
                    'current_difficulty': current_difficulty, 
                    'active_peers': active_peers, 
                    'blockchain_size': str(blockchain_size), 
                    'block_time': str(block_time),
                    'difficulty_change': f"{prev_difficulty_change:.2f}%",
                    'size_change': f"{prev_size_change:.2f}%",
                    'peers_change': f"{prev_peers_change:.2f}%"})

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
    app.run(host='0.0.0.0', port=8081, debug=True)
