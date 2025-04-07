document.addEventListener("DOMContentLoaded", () => {
    const checkboxes = {
        x: document.getElementById("x"),
        facebook: document.getElementById("facebook"),
        reddit: document.getElementById("reddit"),
        instagram: document.getElementById("instagram"),
        linkedin: document.getElementById("linkedin"),
        youtube: document.getElementById("youtube"),
    };

    const countLabels = {
        x: document.getElementById("x-count"),
        facebook: document.getElementById("facebook-count"),
        reddit: document.getElementById("reddit-count"),
        instagram: document.getElementById("instagram-count"),
        linkedin: document.getElementById("linkedin-count"),
        youtube: document.getElementById("youtube-count"),
    };

    chrome.storage.sync.get(["blockedSites", "visitCounts"], (data) => {
        console.log("Loaded settings:", data);
        const blockedSites = data.blockedSites || {};
        const visitCounts = data.visitCounts || {};

        Object.keys(checkboxes).forEach(site => {
            checkboxes[site].checked = blockedSites[site] ?? true;
            countLabels[site].innerText = ` (Visited: ${visitCounts[site] || 0} times)`;
        });
    });

    document.getElementById("save").addEventListener("click", () => {
        const newBlockedSites = {};
        Object.keys(checkboxes).forEach(site => {
            newBlockedSites[site] = checkboxes[site].checked;
        });

        chrome.storage.sync.set({ blockedSites: newBlockedSites }, () => {
            console.log("Settings saved:", newBlockedSites);
            alert("Settings saved!");
        });
    });

    document.getElementById("downloadLogs").addEventListener("click", () => {
        chrome.storage.local.get(["accessLogs"], (data) => {
            const logs = data.accessLogs || {};
            let csvContent = "Site,Access Time\n";

            Object.keys(logs).forEach(site => {
                logs[site].forEach(time => {
                    csvContent += `${site},${time}\n`;
                });
            });

            const blob = new Blob([csvContent], { type: "text/csv" });
            const url = URL.createObjectURL(blob);

            const a = document.createElement("a");
            a.href = url;
            a.download = "access_logs.csv";
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
        });
    });
});
