function getStationName(code) {
    // Reverse stationMap: code → name
    const codeToName = {};
    for (const [name, c] of Object.entries(stationMap)) {
        codeToName[c] = name;
    }
    return codeToName[code] || code;
}

async function search() {
    const source = document.getElementById('source').value;
    const destination = document.getElementById('destination').value;
    const resDiv = document.getElementById('results');
    
    if (!source || !destination) return alert("Enter stations");
    resDiv.innerHTML = "<p style='text-align:center'>Finding routes...</p>";

    // Check if source and destination are the same
    if (source.trim().toUpperCase() === destination.trim().toUpperCase()) {
        resDiv.innerHTML = "<p style='text-align:center'>You are already there.</p>";
        return;
    }

    try {
        const response = await fetch('http://127.0.0.1:5000/find-route', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ source, destination })
        });
        const data = await response.json();
        resDiv.innerHTML = "";

        if (!data.routes || data.routes.length === 0) {
            resDiv.innerHTML = "<p style='text-align:center'>No route found.</p>";
            return;
        }

        data.routes.forEach((route, i) => {
            const srcName = getStationName(source);
            const destName = getStationName(destination);
            const summaryText = `${srcName} → ${destName}`;

            const card = document.createElement('div');
            card.className = 'route-card';
            card.innerHTML = `
                <div class="card-header" onclick="toggle(${i})">
                    <span>${route.summary}</span>
                    <span>
                        ${route.transfer_count === 0 ? 'Direct' : route.transfer_count + ' Transfer(s)'} ▾
                    </span>
                </div>
                <div id="det-${i}" class="details" style="display:none">
                    ${route.segments.map(s => {
                        // Extract codes from "SRE → GHY" style string
                        const parts = s.line.split(" → ");
                        const fromCode = parts[0];
                        const toCode   = parts[1];

                        const fromName = getStationName(fromCode);
                        const toName   = getStationName(toCode);

                        return `
                            <div class="segment">
                                <div style="color:var(--primary); font-weight:bold; margin-bottom:4px;">
                                    ${fromName} → ${toName}
                                </div>
                                <div style="font-size:14px; margin-bottom:8px;">${s.train_no} · ${s.train}</div>
                                <div style="display:flex; justify-content:space-between; font-size:13px; color:#636e72;">
                                    <span><b>Dep:</b> ${s.dep}</span>
                                    <span><b>Reach:</b> ${s.arr}</span>
                                </div>
                            </div>
                        `;
                    }).join('<div class="transfer-mark">CHANGE TRAIN</div>')}
                </div>
            `;
            resDiv.appendChild(card);
        });

    } catch (e) {
        resDiv.innerHTML = "<p style='text-align:center'>Server error.</p>";
        console.error(e);
    }
}

function toggle(id) {
    const el = document.getElementById(`det-${id}`);
    el.style.display = el.style.display === 'none' ? 'block' : 'none';
}

// stationMap should be defined in stations.js
// Example: const stationMap = { "New Delhi": "NDLS", "Dehradun": "DDN", "Saharanpur": "SRE", "Guwahati": "GHY" };

function setupSuggestions(inputId, suggestionsId) {
    const input = document.getElementById(inputId);
    const suggestions = document.getElementById(suggestionsId);

    input.addEventListener("input", () => {
        const query = input.value.trim().toLowerCase();

        if (query.length < 2) {
            suggestions.style.display = "none";
            return;
        }

        const matches = Object.entries(stationMap)
            .filter(([name, code]) => name.toLowerCase().startsWith(query))
            .slice(0, 10);

        if (matches.length === 0) {
            suggestions.style.display = "none";
            return;
        }

        suggestions.innerHTML = matches
            .map(([name, code]) => `
                <div class="suggestion-item" data-code="${code}">
                    ${name} (${code})
                </div>
            `)
            .join("");

        suggestions.style.display = "block";
    });

    suggestions.addEventListener("click", (e) => {
        if (e.target.classList.contains("suggestion-item")) {
            const code = e.target.dataset.code;
            input.value = code;           // store code in input
            suggestions.style.display = "none";
        }
    });

    document.addEventListener("click", (e) => {
        if (!input.contains(e.target) && !suggestions.contains(e.target)) {
            suggestions.style.display = "none";
        }
    });
}

// Initialize for both fields
setupSuggestions("source", "source-suggestions");
setupSuggestions("destination", "destination-suggestions");
