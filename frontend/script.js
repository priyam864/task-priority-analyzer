function showLoading() {
    document.getElementById("loading").style.display = "block";
}

function hideLoading() {
    document.getElementById("loading").style.display = "none";
}

function getPriorityClass(score) {
    if (score >= 0.7) return "high";
    if (score >= 0.4) return "medium";
    return "low";
}

function displayResults(results) {
    let html = "";

    results.forEach(task => {
        const pClass = getPriorityClass(task.priority_score);

        html += `
            <div class="task-card ${pClass}">
                <h3>${task.title}</h3>
                <p><b>Due:</b> ${task.due_date || "N/A"}</p>
                <p><b>Importance:</b> ${task.importance}</p>
                <p><b>Estimated Hours:</b> ${task.estimated_hours || "N/A"}</p>
                <p><b>Score:</b> ${task.priority_score}</p>
                ${
                    task.explanation
                        ? `<p><b>Explanation:</b><br> ${task.explanation.join("<br>")}</p>`
                        : ""
                }
            </div>
        `;
    });

    document.getElementById("output").innerHTML = html;
}

async function analyzeTasks() {
    const input = document.getElementById("taskInput").value;

    let tasks;
    try {
        tasks = JSON.parse(input);
    } catch (e) {
        document.getElementById("output").innerHTML =
            "<b style='color:red'>Invalid JSON format!</b>";
        return;
    }

    const strategy = document.getElementById("strategy").value;

    showLoading();

    const response = await fetch(
        `http://127.0.0.1:8000/api/analyze/?strategy=${strategy}`,
        {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(tasks)
        }
    );

    hideLoading();

    if (!response.ok) {
        const err = await response.json();
        document.getElementById("output").innerHTML =
            `<pre style="color:red;background:#ffe6e6;padding:10px;border-radius:6px;">
             <b>Error:</b> ${JSON.stringify(err, null, 2)}
             </pre>`;
        return;
    }

    const data = await response.json();
    displayResults(data.results);
}

async function suggestTasks() {
    const input = document.getElementById("taskInput").value;

    let tasks;
    try {
        tasks = JSON.parse(input);
    } catch (e) {
        document.getElementById("output").innerHTML =
            "<b style='color:red'>Invalid JSON format!</b>";
        return;
    }

    showLoading();

    const response = await fetch(
        `http://127.0.0.1:8000/api/suggest/`,
        {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(tasks)
        }
    );

    hideLoading();

    if (!response.ok) {
        const err = await response.json();
        document.getElementById("output").innerHTML =
            `<pre style="color:red;background:#ffe6e6;padding:10px;border-radius:6px;">
             <b>Error:</b> ${JSON.stringify(err, null, 2)}
             </pre>`;
        return;
    }

    const data = await response.json();
    displayResults(data.suggestions);
}
