chrome.runtime.onInstalled.addListener(() => {
    chrome.storage.sync.set({
        blockedSites: {
            twitter: true,
            facebook: true,
            reddit: true,
            instagram: true,
            linkedin: true
        }
    });
});
