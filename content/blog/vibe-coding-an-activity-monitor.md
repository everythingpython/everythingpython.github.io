---
title: "Vibe Coding an Activity monitor"
date: 2026-05-28
slug: vibe-coding-an-activity-monitor
---

We live in distracting times. An article from the [Harvard Business Review](https://hbr.org/2022/08/how-much-time-and-energy-do-we-waste-toggling-between-applications) says


> To execute a single supply-chain transaction, each person involved switched about 350 times between 22 different applications and unique websites. Over the course of an average day, that meant a single employee would toggle between apps and windows more than 3,600 times. That’s … a lot. This kind of toggling is often dismissed as simply “how we work now,” even though it’s also taxing for people and a waste of time, effort, and focus. Yet these trends are likely to continue or get worse in an increasingly digital and remote work world. This should give companies pause.

Now I'm not proposing a cure for this cancer. I don't have one. 

But I **have** always been a big fan of knowing how productive I am in a work day vs not. How many times do I switch contexts? How many websites do I visit in the course of an hour? 

The earliest instance of a solution I can remember is when I found [ManicTime](https://www.manictime.com/) in 2017. I immediately installed it on my laptop. I Loved it. It gave me all the information I needed about what I was doing during work, where my time was going, how long I was away and more. It looked like this - 

<img src="/assets/img/activity-monitor/image1.png" style="max-width: 100%;" />

I used it for quite a while. 

Then I heard about **Rize** last year . It looked much better than ManicTime. Understandable since it was actually built for a consumer rather than for a service based company. But it cost way too much for a personal tracking software. 
<img src="/assets/img/activity-monitor/image-2.png" style="max-width: 70%;" />

In the pursuit of finding a better Manictime and a cheaper Rize, I landed last year on [Activity Watch](https://activitywatch.net/). It came close to the best activity monitor I had ever used. It was opensource, configurable and I could add my own watchers. 

<img src="/assets/img/activity-monitor/image-3.png" style="max-width: 70%;" />

I think even now it might be something I could configure for my Mac. 

But the lure of vibecoding something for myself was too strong. 
Why, even Bilbo struggled with the dilemma - 

<img src="/assets/img/activity-monitor/image-4.png" style="max-width: 50%;" />

That's how I ended up creating the configurable, highly imaginatively named - "Where Did My Day Go". The caveat is that this is built only for the Mac as of this writing. I plan to extend it to Windows and Linux as well. 

It runs completely locally and tracks all my activities - which applications were used, which websites were accessed, how long I was away from my desk, how long I was active on certain applications I care about (Chrome, VS Code, Terminal etc. )

<img src="/assets/img/activity-monitor/image-6.png" style="max-width: 100%;" />

Now, I have never built anything for the Mac OS before. Even now, this is a Webapp. But the tricky parts were understanding how the monitoring and collection of metrics For the Mac OS was possible. Something that Claude taught me quite a bit about. 

## The Stack

  Two long-running processes, one SQLite file.

  **Collector** (`collector.py`) : runs forever, samples every 5 seconds:
  - **Python 3.12** with [`pyobjc`](https://pyobjc.readthedocs.io/) for the macOS bindings (Cocoa + Quartz frameworks)
  - **`lsappinfo front`** (subprocess to the macOS LaunchServices CLI) : the focused app
  - **AppleScript** via `osascript` : the active Chrome tab URL
  - **`Quartz.CGEventSourceSecondsSinceLastEventType`** : idle time (seconds since last keyboard/mouse event)
  - **`launchd`** : auto-start at login via a `.plist` user agent in `~/Library/LaunchAgents/`

  **Storage** (`db.py`):
  - **SQLite** : single file, `WAL` mode + `synchronous=NORMAL` so the collector and the dashboard can hit it concurrently
  - **Schema: intervals, not samples.** One row per consecutive run of identical `(category, app, bundle, url, is_idle)`. The collector extends
  `end_ts` while the key matches, opens a new row when it changes. Months of data fits in ~40K rows.

  **Dashboard** (`server.py`, frontend):
  - **Flask** : three JSON endpoints and one HTML template, bound to `127.0.0.1` only
  - **Plain HTML / CSS / vanilla JS** : no build step, no framework, no `node_modules`
  - **Chart.js 4** from a CDN : the only outbound network request the app makes; vendor it if you care
  - **CSS custom properties as design tokens** : color variables like `--c-claude_desktop` live in `styles.css` and are read from JS via
  `getComputedStyle`, so chart colors and KPI border colors stay in sync from one source of truth

  **Project tooling:**
  - **`uv`** + `pyproject.toml` + `.python-version` : no `pip`, no manual venv. 
  - `uv sync` is the entire bootstrap; 
  - `uv run python collector.py` is how you run it.

The collector is the fun part . It is a single Python process supervised by launchd. Every 5 seconds it asks macOS four questions:
![alt text](image-7.png)
 and writes the answer to SQLite. To get the "focused app" right means using lsappinfo (LaunchServices) rather than AppKit or window-stacking order. I found an excellent follow-up read for [this](https://eclecticlight.co/2020/03/04/learn-almost-everything-about-an-app-with-lsappinfo/). 


 ## How to Setup

 Just follow the README. If you have doubts, ping me or raise an issue on the [Github repo](https://github.com/abhiramr/where-did-my-day-go). 