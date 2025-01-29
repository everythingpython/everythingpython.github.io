chrome.runtime.onInstalled.addListener(() => {
    chrome.storage.sync.set({
        blockedSites: {
            x: true,
            facebook: true,
            reddit: true,
            instagram: true,
            linkedin: true,
            youtube: true
        }
    });
});
