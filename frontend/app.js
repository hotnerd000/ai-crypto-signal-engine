let chart;
async function analyze() {
    showLoading();
    document.getElementById("error").textContent = "";

    try{
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

        if (!res.ok) {
            const err = await res.json();
            throw new Error(err.detail || "Analyze failed");
        }

        const data = await res.json();

        document.getElementById("output").textContent =
            JSON.stringify(data, null, 2);

        renderChart(data.history);
    } catch(err) {
        showError(err.message);
    }  finally {
        hideLoading();   // 🔥 always runs
    }
    
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
                    label: "BUY",
                    data: history.map(d => d.signal === "BUY" ? d.price : null),
                    showLine: false,

                    pointStyle: "triangle",
                    rotation: 0,              // ▲ (up)
                    pointRadius: 8,
                    pointHoverRadius: 10,

                    backgroundColor: "green",
                    borderColor: "green"
                },
                {
                    label: "SELL",
                    data: history.map(d => d.signal === "SELL" ? d.price : null),
                    showLine: false,

                    pointStyle: "triangle",
                    rotation: 180,            // ▼ (down)
                    pointRadius: 8,
                    pointHoverRadius: 10,

                    backgroundColor: "red",
                    borderColor: "red"
                },
                {
                    label: "ALL SIGNAL POINTS",
                    data: history.map(d => d.price),
                    pointRadius: 2,
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
                },
                 tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `${context.dataset.label} @ ${context.raw.toFixed(2)}`;
                        }
                    }
                }
            },
            scales: {
                x: {
                    display: true
                },
                y: {
                    display: true
                }
            },
            borderWidth: 2
        }
    });
}

async function runBacktest() {
    showLoading();
    document.getElementById("error").textContent = "";

    try{
        const coin = document.getElementById("coin").value;

        const days = parseInt(
            document.getElementById("bt_days").value || "90"
        );

        const balance = parseFloat(
            document.getElementById("bt_balance").value || "1000"
        );

        const res = await fetch("http://localhost:8000/backtest", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                coin: coin,
                days: days,
                balance: balance
            })
        });

        if (!res.ok) {
            const err = await res.json();
            throw new Error(err.detail || "Backtest failed");
        }

        const data = await res.json();

        console.log("Backtest result:", data);

        renderBacktestChart(data.history, data.trades);
    }  catch (err) {
        showError(err.message);
    }   finally {
        hideLoading();   // 🔥 always runs
    }

}

function renderBacktestChart(history, trades) {
    const labels = history.map(d =>
        new Date(d.date).toLocaleDateString()
    );

    const prices = history.map(d => d.price);

    // 🔥 Map trades to chart points
    const buyPoints = history.map(h => {
        const trade = trades.find(t =>
            t.type === "BUY" && new Date(t.date).getTime() === new Date(h.date).getTime()
        );
        return trade ? h.price * 0.995 : null;
    });

    const sellPoints = history.map(h => {
        const trade = trades.find(t =>
            t.type === "SELL" && new Date(t.date).getTime() === new Date(h.date).getTime()
        );
        return trade ? h.price * 1.005 : null;
    });

    const ctx = document.getElementById("priceChart").getContext("2d");

    if (chart) chart.destroy();

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
                    label: "BUY",
                    data: buyPoints,
                    showLine: false,
                    pointStyle: "triangle",
                    rotation: 0,
                    pointRadius: 8,
                    backgroundColor: "green"
                },
                {
                    label: "SELL",
                    data: sellPoints,
                    showLine: false,
                    pointStyle: "triangle",
                    rotation: 180,
                    pointRadius: 8,
                    backgroundColor: "red"
                }
            ]
        },
        options: {
            responsive: true,
            plugins: {
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `${context.dataset.label} @ ${context.raw?.toFixed(2)}`;
                        }
                    }
                }
            }
        }
    });
}

function showError(message) {
    document.getElementById("error").textContent = message;
}

function showLoading() {
    document.getElementById("loading").style.display = "block";
    disableButtons(true);
}

function hideLoading() {
    document.getElementById("loading").style.display = "none";
    disableButtons(false);
}

function disableButtons(disabled) {
    document.querySelectorAll("button").forEach(btn => {
        btn.disabled = disabled;
         btn.textContent = disabled ? "Processing..." : btn.dataset.original || btn.textContent;
    });
}