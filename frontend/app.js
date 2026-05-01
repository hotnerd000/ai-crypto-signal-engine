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
}