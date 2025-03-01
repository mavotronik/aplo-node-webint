function updateAutoCounter() {
    fetch('/get_auto_counter')
        .then(response => response.json())
         .then(data => {
            document.getElementById('auto-counter').innerHTML = data.auto_counter;
      });
}

function updateSysStats() {
    fetch('/get_sys_stats')
        .then(response => response.json())
         .then(data => {
            document.getElementById('cpu').innerHTML = data.cpu_stat;
            document.getElementById('ram').innerHTML = data.ram_stat;
            document.getElementById('uptime').innerHTML = data.uptime_stat;
      });
}

function incrementCounter() {
      fetch('/', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/x-www-form-urlencoded',
          },
          body: 'action=increment'
      }).then(response => {
           fetch('/get_counter')
            .then(response => response.json())
            .then(data => {
               document.getElementById('counter').innerHTML = data.counter;
               });
      });
  }

function decrementCounter() {
      fetch('/', {
           method: 'POST',
           headers: {
               'Content-Type': 'application/x-www-form-urlencoded',
           },
           body: 'action=decrement'
     }).then(response => {
          fetch('/get_counter').then(response => response.json())
              .then(data => {
                 document.getElementById('counter').innerHTML = data.counter;
             });
     });
 }

setInterval(updateAutoCounter, 500); // Обновление автоматического счетчика каждую секунду
setInterval(updateSysStats, 1500);