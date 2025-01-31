async function fetchSystemDesignTip() {
    const csvUrl = chrome.runtime.getURL("data/system_design_tips.csv"); // Local CSV file
    try {
        const response = await fetch(csvUrl);
        if (!response.ok) throw new Error("Failed to load CSV");

        const csvText = await response.text();
        const lines = csvText.split("\n").filter(line => line.trim() !== "");
        const randomTip = lines[Math.floor(Math.random() * lines.length)];

        return randomTip || "Always design for scalability!";
    } catch (error) {
        console.error("Error fetching System Design tip:", error);
        return "Could not load tip.";
    }
}

chrome.storage.sync.get(["blockedSites", "visitCounts"], async (data) => {
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

        const systemDesignTip = await fetchSystemDesignTip();

        if (blockedSites[siteKey]) {
            document.documentElement.innerHTML = `
            <div style="
                position: fixed; top: 0; left: 0; width: 100%; height: 100%;
                background: linear-gradient(135deg, #0d1b2a, #1b263b);
                display: flex; align-items: center; justify-content: center; 
                text-align: center;
                font-size: 24px; font-weight: bold; color: white;
                font-family: 'Arial', sans-serif; padding: 20px;
            ">
                <div style="
                    background: rgba(0, 0, 0, 0.85);
                    padding: 20px 40px; border-radius: 15px;
                    box-shadow: 0px 6px 15px rgba(0,0,0,0.4);
                    width: 50%;
                    max-width: 600px;
                    text-align: left;
                ">
                    <h2>🚀 Focus Mode</h2>
                    <hr style="margin: 15px 0; border-color: #29b6f6;">
                    You've visited <span style="color: #29b6f6;">${siteKey}</span> 
                    <span style="color: #29b6f6;">${visitCounts[siteKey]}</span> times.
                    <span style="color: #29b6f6;">Stay focused.</span>
                    <hr style="margin: 15px 0; border-color: #29b6f6;">
                    <div style="
                        background: #263238; color: yellow; 
                        font-family: 'Courier New', monospace;
                        padding: 15px; border-radius: 10px;
                        font-size: 18px;
                        white-space: pre-wrap;
                        display: block;
                        width: 100%;
                        box-sizing: border-box;
                    ">
                        
                        <div style="white-space: pre-wrap; display: block;">📌 System Design Tip:</span><br><br><br><br>${systemDesignTip}</code>
                    </div>
                </div>
            </div>
        `;
        
        }
    }
});
