chrome.storage.sync.get(["blockedSites", "visitCounts"], (data) => {
    const blockedSites = data.blockedSites || {};
    const visitCounts = data.visitCounts || {};
    const hostname = window.location.hostname;
    let siteKey = "";

    if (hostname.includes("x.com")) siteKey = "x";
    else if (hostname.includes("facebook.com")) siteKey = "facebook";
    else if (hostname.includes("reddit.com")) siteKey = "reddit";
    else if (hostname.includes("instagram.com")) siteKey = "instagram";
    else if (hostname.includes("linkedin.com")) siteKey = "linkedin";
    else if (hostname.includes("youtube.com")) siteKey = "youtube";

    if (siteKey) {
        visitCounts[siteKey] = (visitCounts[siteKey] || 0) + 1;
        chrome.storage.sync.set({ visitCounts });

        console.log(`You've visited ${siteKey} ${visitCounts[siteKey]} times.`);

        if (blockedSites[siteKey]) {
            document.documentElement.innerHTML = `
                <div style="
                    position: fixed; top: 0; left: 0; width: 100%; height: 100%;
                    background: linear-gradient(135deg, #ff9aff, #fffaff);
                    display: flex; align-items: center; justify-content: center; 
                    flex-direction: column; text-align: center;
                    font-size: 26px; font-weight: bold; color: white;
                    font-family: 'Arial', sans-serif;
                ">
                    <div style="
                        background: rgba(0, 0, 0, 0.5);
                        padding: 20px 40px; border-radius: 15px;
                        box-shadow: 0px 4px 10px rgba(0,0,0,0.3);
                    ">
                        🚀 Stay Focused! <br>
                        You've visited <span style="color: #ffeb3b;">${siteKey}</span> 
                        <span style="color: #ffeb3b;">${visitCounts[siteKey]}</span> times.
                    </div>
                </div>
            `;
        }
    }
});
