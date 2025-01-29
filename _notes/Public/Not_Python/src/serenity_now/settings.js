document.addEventListener("DOMContentLoaded", () => {
    const checkboxes = {
        twitter: document.getElementById("twitter"),
        facebook: document.getElementById("facebook"),
        reddit: document.getElementById("reddit"),
        instagram: document.getElementById("instagram"),
        linkedin: document.getElementById("linkedin"),
    };

    chrome.storage.sync.get("blockedSites", (data) => {
        console.log("Loaded settings:", data);
        const blockedSites = data.blockedSites || {};

        Object.keys(checkboxes).forEach(site => {
            checkboxes[site].checked = blockedSites[site] ?? true;
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
