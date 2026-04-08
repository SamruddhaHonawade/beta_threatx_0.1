let chart;
let allLogs = [];

async function sendPrompt() {
    let prompt = document.getElementById("promptInput").value;

    let res = await fetch("/api/analyze", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({prompt})
    });

    let data = await res.json();

    let riskLevel = "low";
    if (data.risk_score > 70) riskLevel = "high";
    else if (data.risk_score > 40) riskLevel = "medium";

    document.getElementById("analysisResult").innerHTML = `
        <p class="${data.blocked ? 'blocked':'allowed'}">
            ${data.blocked ? '🚨 BLOCKED' : '✅ ALLOWED'}
        </p>
        <p>Risk Score: <span class="${riskLevel}">${data.risk_score}</span></p>
    `;

    loadLogs();
}

async function loadLogs() {
    let res = await fetch("/api/logs");
    allLogs = await res.json();
    renderLogs(allLogs);
}

function renderLogs(data) {
    let table = document.getElementById("logs");
    table.innerHTML = "";

    let blocked = 0, allowed = 0;

    data.forEach(log => {
        let status = log.blocked ? "BLOCKED" : "ALLOWED";

        if (log.blocked) blocked++;
        else allowed++;

        table.innerHTML += `
        <tr>
            <td>${log.time}</td>
            <td>${log.prompt}</td>
            <td class="${log.blocked ? 'blocked':'allowed'}">${status}</td>
            <td>${log.risk_score}</td>
        </tr>`;
    });

    document.getElementById("total").innerText = data.length;
    document.getElementById("blocked").innerText = blocked;
    document.getElementById("allowed").innerText = allowed;

    updateChart(blocked, allowed);
}

function filterLogs(type) {
    if (type === "blocked")
        renderLogs(allLogs.filter(l => l.blocked));
    else if (type === "allowed")
        renderLogs(allLogs.filter(l => !l.blocked));
    else
        renderLogs(allLogs);
}

function updateChart(blocked, allowed) {
    let ctx = document.getElementById("chart");

    if (chart) chart.destroy();

    chart = new Chart(ctx, {
        type: "doughnut",
        data: {
            labels: ["Blocked", "Allowed"],
            datasets: [{
                data: [blocked, allowed]
            }]
        }
    });
}

setInterval(loadLogs, 3000);
loadLogs();