document.addEventListener("DOMContentLoaded", () => {
    let cpuData = [];
    let memoryData = [];
    let labels = [];

    // ✅ Initialize ApexCharts
    const cpuChart = new ApexCharts(document.querySelector("#cpuChart"), {
        chart: {
            type: "line",
            height: 200,
            animations: { enabled: true },
        },
        series: [{ name: "CPU Usage", data: cpuData }],
        xaxis: { categories: labels }
    });

    const memoryChart = new ApexCharts(document.querySelector("#memoryChart"), {
        chart: {
            type: "line",
            height: 200,
            animations: { enabled: true },
        },
        series: [{ name: "Memory Usage", data: memoryData }],
        xaxis: { categories: labels }
    });

    cpuChart.render();
    memoryChart.render();

    async function fetchStats() {
        try {
            const response = await fetch("http://localhost:8888/system/stats");
            const data = await response.json();

            document.getElementById("memory_usage").textContent = data.memory_usage_mb;
            document.getElementById("cpu_usage").textContent = data.cpu_usage_percent;

            // ✅ Update Graph Data
            if (labels.length > 10) {
                labels.shift();
                cpuData.shift();
                memoryData.shift();
            }

            labels.push(new Date().toLocaleTimeString());
            cpuData.push(data.cpu_usage_percent);
            memoryData.push(data.memory_usage_mb);

            cpuChart.updateSeries([{ data: cpuData }]);
            memoryChart.updateSeries([{ data: memoryData }]);
        } catch (error) {
            console.error("Error fetching system stats:", error);
        }
    }

    async function fetchAPILogs() {
        try {
            const response = await fetch("http://localhost:8888/logs/api");
            const data = await response.json();

            document.getElementById("api_logs").innerHTML = data.logs
                .map(log => `<p>[${log.time}] ${log.method} - Status: ${log.status}</p>`)
                .join('');
        } catch (error) {
            console.error("Error fetching API logs:", error);
        }
    }

    async function fetchBotLogs() {
        try {
            const response = await fetch("http://localhost:8888/logs/bot");
            const data = await response.json();

            document.getElementById("bot_logs").innerHTML = data.logs
                .map(log => `<p>[${log.time}] ${log.action}: ${log.message}</p>`)
                .join('');
        } catch (error) {
            console.error("Error fetching bot logs:", error);
        }
    }

    // ✅ Different Update Intervals
    fetchStats();
    fetchAPILogs();
    fetchBotLogs();
    setInterval(fetchStats, 5000);
    setInterval(fetchAPILogs, 10000);
    setInterval(fetchBotLogs, 300000);
});
