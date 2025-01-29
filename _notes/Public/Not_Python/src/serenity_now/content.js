chrome.storage.sync.get("blockedSites", (data) => {
    const blockedSites = data.blockedSites || {};
    const hostname = window.location.hostname;

    console.log("Blocked sites settings loaded:", blockedSites);
    console.log("Current hostname:", hostname);

    if (
        (blockedSites.twitter && hostname.includes("twitter.com")) ||
        (blockedSites.facebook && hostname.includes("facebook.com")) ||
        (blockedSites.reddit && hostname.includes("reddit.com")) ||
        (blockedSites.instagram && hostname.includes("instagram.com")) ||
        (blockedSites.linkedin && hostname.includes("linkedin.com"))
    ) {
        console.log("Blocking site with splash screen");

        document.documentElement.innerHTML = `
            <div style="position: fixed; top: 0; left: 0; width: 100%; height: 100%;
                        background: white; display: flex; align-items: center;
                        justify-content: center; font-size: 24px; font-weight: bold;">
                Stay Focused! 🚀
            </div>
        `;
    } else {
        console.log("Site is not blocked.");
    }
});
