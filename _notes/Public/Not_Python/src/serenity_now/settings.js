document.addEventListener("DOMContentLoaded", () => {
    const checkboxes = {
        x: document.getElementById("x"),
        facebook: document.getElementById("facebook"),
        reddit: document.getElementById("reddit"),
        instagram: document.getElementById("instagram"),
        linkedin: document.getElementById("linkedin"),
        youtube: document.getElementById("youtube")

    };

    chrome.storage.sync.get(["blockedSites", "visitCounts"], (data) => {
        console.log("Loaded settings:", data);
        const blockedSites = data.blockedSites || {};
        const visitCounts = data.visitCounts || {};

        Object.keys(checkboxes).forEach(site => {
            checkboxes[site].checked = blockedSites[site] ?? true;
            
            const countDisplay = document.createElement("span");
            countDisplay.innerText = ` (Visited: ${visitCounts[site] || 0} times)`;
            countDisplay.style.color = "#000b3b";
            checkboxes[site].parentElement.appendChild(countDisplay);
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
});
