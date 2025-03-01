function updateSysStats() {
    fetch('/get_sys_stats')
        .then(response => response.json())
         .then(data => {
            document.getElementById('cpu').innerHTML = data.cpu_stat;
            document.getElementById('ram').innerHTML = data.ram_stat;
            document.getElementById('uptime').innerHTML = data.uptime_stat;
      });
}


// Обновление автоматического счетчика каждую секунду
setInterval(updateSysStats, 1500);