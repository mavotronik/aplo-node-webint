const previousChanges = {
    difficulty: '--',
    peers: '--',
    size: '--'
};

async function fetchStats() {
    const response = await fetch('/get_node_stats');
    const data = await response.json();

    // Обновление основных значений
    document.getElementById('currentBlock').innerText = `Current Block: ${data.current_block}`;
    document.getElementById('difficultyValue').innerText = data.current_difficulty;
    document.getElementById('peersValue').innerText = data.active_peers;
    document.getElementById('sizeValue').innerText = data.blockchain_size;
    document.getElementById('blockTime').innerText = `Last Block Time: ${data.block_time}`;

    // Обновление изменений, если новое значение не 0
    updateChangeElement('difficultyChange', data.difficulty_change, 'difficulty');
    updateChangeElement('peersChange', data.peers_change, 'peers');
    updateChangeElement('sizeChange', data.size_change, 'size');
}

// Функция обновления изменений с сохранением состояния
function updateChangeElement(elementId, value, key) {
    const element = document.getElementById(elementId);
    
    // Если новое изменение не 0, обновляем сохранённое значение
    if (parseFloat(value) !== 0) {
        previousChanges[key] = value;
    }

    // Отображаем последнее ненулевое изменение
    element.innerText = `Δ ${previousChanges[key]}`;

    // Убираем старые классы
    element.classList.remove('positive', 'negative');

    // Проверяем знак и добавляем цвет (кроме размера)
    const numericValue = parseFloat(previousChanges[key]);
    if (!isNaN(numericValue) && key !== 'size') {
        if (numericValue > 0) {
            element.classList.add('positive');
        } else if (numericValue < 0) {
            element.classList.add('negative');
        }
    }
}

async function fetchSysStats() {
    const response = await fetch('/get_sys_stats');
    const data = await response.json();
    document.getElementById('cpu').innerText = `CPU: ${data.cpu_stat}%`;
    document.getElementById('ram').innerText = `RAM: ${data.ram_stat}%`;
    document.getElementById('uptime').innerText = `Uptime: ${data.uptime_stat}`;
}

async function fetchLastBlocks() {
    const response = await fetch('/get_last_blocks');
    const data = await response.json();
    const lastBlocksContainer = document.getElementById('lastBlocks');
    lastBlocksContainer.innerHTML = '';
    data.forEach(block => {
        const blockElement = document.createElement('div');
        blockElement.className = 'block-item';
        blockElement.innerText = `Block #${block.number}\nTime: ${block.time_utc}`;
        lastBlocksContainer.appendChild(blockElement);
    });
}

setInterval(fetchStats, 5000);
setInterval(fetchSysStats, 5000);
setInterval(fetchLastBlocks, 5000);
fetchStats();
fetchSysStats();
fetchLastBlocks();
