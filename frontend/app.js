let chart;
async function analyze() {
    const coin = document.getElementById("coin").value;
    const days = parseInt(document.getElementById("days").value || "30");
    const future = parseInt(document.getElementById("future").value || "7");

    const res = await fetch("http://localhost:8000/analyze", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            coin: coin,
            days: days,
            future_days: future
        })
    });

    const data = await res.json();

    document.getElementById("output").textContent =
        JSON.stringify(data, null, 2);

    renderChart(data.history);
}

function renderChart(history) {
    const labels = history.map(d => new Date(d.timestamp).toLocaleDateString());
    const prices = history.map(d => d.price);
    const ma = history.map(d => d.ma);
    const signals = history.map(d => d.signal);

    const ctx = document.getElementById("priceChart").getContext("2d");

    // destroy old chart
    if (chart) {
        chart.destroy();
    }

    chart = new Chart(ctx, {
        type: "line",
        data: {
            labels: labels,
            datasets: [
                {
                    label: "Price",
                    data: prices,
                    borderWidth: 2
                },
                {
                    label: "MA",
                    data: ma,
                    borderWidth: 2
                },
                {
                    label: "BUY Signals",
                    data: history.map(d => d.signal === "BUY" ? d.price : null),
                    pointRadius: 5,
                    showLine: false
                },
                {
                    label: "SELL Signals",
                    data: history.map(d => d.signal === "SELL" ? d.price : null),
                    pointRadius: 5,
                    showLine: false
                }
            ]
        },
        options: {
            responsive: true,
            interaction: {
                mode: "index",
                intersect: false
            },
            plugins: {
                legend: {
                    display: true
                }
            },
            scales: {
                x: {
                    display: true
                },
                y: {
                    display: true
                }
            }
        }
    });
}