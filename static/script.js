function updateSysStats() {
    fetch('/get_sys_stats')
        .then(response => response.json())
         .then(data => {
            document.getElementById('cpu').innerHTML = data.cpu_stat;
            document.getElementById('ram').innerHTML = data.ram_stat;
            document.getElementById('uptime').innerHTML = data.uptime_stat;
      });
}

function updateNodeStats() {
    fetch('/get_node_stats')
        .then(response => response.json())
         .then(data => {
            document.getElementById('current_block').innerHTML = data.current_block;
            document.getElementById('current_difficulty').innerHTML = data.current_difficulty;
            document.getElementById('active_peers').innerHTML = data.active_peers;
            document.getElementById('blockchain_size').innerHTML = data.blockchain_size;
      });
}

// Обновление автоматического счетчика каждую секунду
setInterval(updateSysStats, 1500);
setInterval(updateNodeStats, 1000)