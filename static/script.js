async function fetchStats() {
    const response = await fetch('/get_node_stats');
    const data = await response.json();
    document.getElementById('currentBlock').innerText = `Current Block: ${data.current_block}`;
    document.getElementById('difficulty').innerText = `Difficulty: ${data.current_difficulty}`;
    document.getElementById('peers').innerText = `Peers: ${data.active_peers}`;
    document.getElementById('size').innerText = `Size: ${data.blockchain_size}`;
    document.getElementById('blockTime').innerText = `Last Block Time: ${data.block_time}`;
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
