---
title: Focus mode - A "kutty" chrome extension
feed: show
date: 2025-01-29
tags:
  - not-python
  - llms
---

By now you've seen a lot of stuff being built using ChatGPT. A lot, Jerry. A LOT. 

I've built a few apps and extensions as well, but this is the first I'm writing about. 

Over the last 3-4 years, "building"  software on any scale has seen quite a radical shift. 

> Here's an image to scale -


![Alt Text](/assets/img/non-python/chrome-extension-focus/productivity.png)


So when I first tried to build a Chrome extension for a company hackathon in 2022, I took around 12 hours, pulling an all-nighter. 
I looked up documentation, Stack Overflow answers, sample blogs and trudged through the whole process - The way god intended it. And finally completed...something. 
The end result was something that did the job I wanted but it looked absolutely horrendous and I had to hand-wave over the UX because I had no time before the presentation. 

Cut to late 2023 - another company hackathon - this time the result was much more polished, thanks to ChatGPT but it was still lacking here and there. I also took 4-5 hours to complete it, even with the crutch. 

And earlier today, when I found myself on the distracted side of a productive day, browsing on Twitter and Reddit, I decided to channel my distraction into something positive - YACE .

**Y**et **A**nother **C**hrome **E**xtension.

This time my mission was very targeted. I just wanted something that would block the sites that were distracting me on-demand and I should be able to pick the sites I wanted to block and which I wanted to unblock at will. 

This was the prompt I provided ChatGPT and with some prompt-tweaking and some code-tweaking, this is where I ended up - 

![Alt Text](/assets/img/non-python/chrome-extension-focus/chrome-ext-preview.png)

I might have been able to wire the pieces together and come up with this fairly quickly. But the real goal was also to understand what all go into making a Chrome extension. 
For this particular usecase of blocking access to certain sites, this is what I needed - 

- manifest.json
- background.js
- content.js
- settings.html
- settings.js

I looked into what each of these mean - 
A manifest.json is apparently the skeleton of a Chrome extension. It needs some properties like "name", "version", "description", "permissions" etc. .
For this usecase, it also needed to know what files need to work in the background -`background.js` - a watcher. And what the "action" should be - which is the invocation of `settings.html`
The manifest file also allows for the registering of icon files - which are images for the icon of the chrome extension - a profile pic for the extension, if you will. 

In `background.js` , I set which all sites are to be set as blocked. 

In `content.js`, I put the meat of the logic as to what needs to happen when any of the websites registered in `background.js` are accessed. 
Everytime one of the mentioned sites are accessed, a counter is incremented for that access and the website's innerHtml is overwritten with a custom splash screen that displays a message to Focus and the number of times the site has been attempted to be accessed. 

The settings.json and settings.html focus on (surprise, surprise) the settings for the extension where I specify whether a certain site is to be blocked or not and the preference is saved. 

All these files were placed in a folder. I then opened up the `chrome://extensions` page on my Chrome window, turned on Developer mode on the top right and then clicked on "Load unpacked".
After navigating to the folder I had just created for the extension, I loaded it and I was able to see my extension sitting pretty alongside rest of Chrome's extensions. 

### Now, was this completely smooth?

Yes and no. The base version of the extension was able to be set up in less than 15 minutes. 
But then it looked so ...bland. 

I asked ChatGpt for a few tweaks which when I dutifully copied over to my codebase, the whole thing broke. 
The way I was able to diagnose what went wrong was to use Chrome's Developer Tools and go to the Console Logs and when I navigated to Linkedin or any of the other sites I had blocked, I was able to see the error that had caused the extension to crash. 

This was the real combination of Man and Machine - Power Extreme

![Alt Text](/assets/img/non-python/chrome-extension-focus/power-extreme.gif)

Ultimately after some more code-tweaking, I was able to get the desired effects I wanted, CSS modifications and all. 

### What next?

I want to make this a little more flexible, so I can add any websites I want to block on the fly. After all, storage of state is within the browser (as is evident by the incrementing counter of visits). 

I also want to eventually publish this extension to the Chrome webstore. I would have done it already but there's a $5 cost to registering yourself as a "Chrome Developer" and I'm not quite interested in bearing that cost yet. 

All in all, a satisfying creation, even if simplistic :)


Here's a quick video demonstrating it - 

<iframe width="560" height="315" src="https://www.youtube.com/embed/1t9hAi6DUnc?si=caJldMAgyZPZrkUP" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>


All the code mentioned above is available [here](https://github.com/everythingpython/everythingpython.github.io/tree/main/_notes/Public/Not_Python/src/serenity_now).

