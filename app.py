from flask import Flask, render_template, request, jsonify
import threading
import time
import psutil
import datetime

app = Flask(__name__)

counter = 0
auto_counter = 0
cpu = 0
ram = 0
uptime = ""

def increment_auto_counter():
    global auto_counter
    while True:
        auto_counter += 1
        time.sleep(1)

def sys_stats():
    global cpu
    global ram
    global uptime
    while True: 
        cpu = psutil.cpu_percent()

        ram = psutil.virtual_memory()
        ram = float(ram.percent)

        uptime = datetime.timedelta(seconds=time.time() - psutil.boot_time())
        

        time.sleep(1)

auto_counter_thread = threading.Thread(target=increment_auto_counter)
auto_counter_thread.daemon = True # Чтобы поток завершался вместе с основным потоком
auto_counter_thread.start()
sys_stats_thread = threading.Thread(target=sys_stats)
sys_stats_thread.daemon = True
sys_stats_thread.start()


@app.route('/', methods=['GET', 'POST'])
def index():
    global counter
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'increment':
           counter += 1
        elif action == 'decrement' and counter > 0:
           counter -= 1
    return render_template('index.html', counter=counter, auto_counter=auto_counter)

@app.route('/get_counter', methods=['GET'])
def get_counter():
    global counter
    return jsonify({'counter': counter})


@app.route('/get_auto_counter', methods=['GET'])
def get_auto_counter():
    global auto_counter
    return jsonify({'auto_counter': auto_counter})

@app.route('/get_sys_stats', methods=['GET'])
def get_sys_stats():
    global cpu
    global ram
    global uptime
    return jsonify({'cpu_stat': cpu, 'ram_stat': ram, 'uptime_stat': str(uptime)})

if __name__ == '__main__':
    app.run(debug=True)
