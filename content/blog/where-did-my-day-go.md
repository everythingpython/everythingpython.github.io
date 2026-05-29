---
title: "Where did my day go? "
date: 2026-05-28
slug: where-did-my-day-go
---

We live in distracting times. An article from the [Harvard Business Review](https://hbr.org/2022/08/how-much-time-and-energy-do-we-waste-toggling-between-applications) says


> To execute a single supply-chain transaction, each person involved switched about 350 times between 22 different applications and unique websites. Over the course of an average day, that meant a single employee would toggle between apps and windows more than 3,600 times. That’s … a lot. This kind of toggling is often dismissed as simply “how we work now,” even though it’s also taxing for people and a waste of time, effort, and focus. Yet these trends are likely to continue or get worse in an increasingly digital and remote work world. This should give companies pause.

Now I'm not proposing a cure for this cancer. I don't have one. 

But I **have** always been a big fan of knowing how productive I am in a work day vs not. How many times do I switch contexts? How many websites do I visit in the course of an hour? 

The earliest instance of a solution I can remember is when I found [ManicTime](https://www.manictime.com/) in 2017. I immediately installed it on my laptop. I Loved it. It gave me all the information I needed about what I was doing during work, where my time was going, how long I was away and more. It looked like this - 

<img src="/assets/img/activity-monitor/image1.png" style="max-width: 100%;" />

Then I heard about **Rize** last year . It looked much better than ManicTime. Understandable since it was actually built for a consumer rather than for a service based company. But it cost way too much for a personal tracking software. 
<img src="/assets/img/activity-monitor/image-2.png" style="max-width: 100%;" />

In the pursuit of finding a better Manictime and a cheaper Rize, I landed last year on [Activity Watch](https://activitywatch.net/). It came close to the best activity monitor I had ever used. It was opensource, configurable and I could add my own watchers. 

<img src="/assets/img/activity-monitor/image-3.png" style="max-width: 100%;" />

I think even now it might be something I could configure for my Mac. 

But the lure of vibecoding something for myself was too strong. 
Why, even Bilbo struggled with the dilemma - 

<img src="/assets/img/activity-monitor/image-4.png" style="max-width: 50%;" />

That's how I ended up creating the configurable, highly imaginatively named - **"Where Did My Day Go"**. The caveat is that this is built only for the Mac as of this writing. I plan to extend it to Windows and Linux as well. 

It runs completely locally and tracks all my activities - which applications were used, which websites were accessed, how long I was away from my desk, how long I was active on certain applications I care about (Chrome, VS Code, Terminal etc. )

Now, I have never built anything for the Mac OS before. Even now, this is a Webapp. But the tricky parts were understanding how the monitoring and collection of metrics For the Mac OS was possible. Something that Claude taught me quite a bit about. 


{{< callout type="note" >}}
Claude Code stores conversation history locally as JSONL files. If you want to check yours out, look them up at ~/.claude/projects
 {{< /callout >}}

I asked Claude to fetch all my prompts from the JSONL file it creates under Projects. 

Here was my initial prompt - 
{{< callout type="prompt" >}}
I want a detailed web-app based activity monitor dashboard that tracks when I've not been at desk, when I've been using claude code via desktop or terminal, when I've been using google chrome, vscode etc.
{{< /callout >}}

The next set of exchanges were about the choice of tech stack and the tracking mechanism. It asked me to pick from a set of stacks that it seemed to find apt for the task and on the basis of my preferences from other applications "vibe-built" - 

{{< callout type="prompt" >}}
Choices selected - 
Stack: Python + Flask + SQLite - easiest for macOS system APIs (idle detection via Quartz, frontmost app via AppKit), single-file backend with vanilla JS + Chart.js frontend, no build step.

Collector: Manual start script + launchd plist - a start.sh plus a com.user.activitymonitor.plist to launchctl load so it runs at login, with the user controlling when it runs.
{{< /callout >}}

{{< callout type="prompt" >}}

Tracking granularity choices: 
1. Active app + window title - Captures the frontmost app every N seconds and its window title (to distinguish Claude Code in terminal vs Chrome tabs vs VSCode projects).
2. Idle / away-from-desk detection - Tracks when there's been no keyboard/mouse input for more than N seconds (uses macOS HIDIdleTime).
3. Per-Chrome-tab URL tracking - Captures the active Chrome tab URL via AppleScript (requires Automation permission for Chrome).
{{< /callout >}}

While it helped me sort out 95% of the job, it still needed a few nudges. I captured the parts where I had to probe it - parts where it seemed extremely confident. 

{{< callout type="prompt" >}}
Top Chrome tabs — "No Chrome tab data yet. Grant Automation permission to Chrome when prompted." It hasn't prompted.
{{< /callout >}}

{{< callout type="response" >}}
The Chrome prompt only fires when the collector executes the AppleScript, which only happens when Chrome is frontmost. You've probably been on Claude Desktop/Terminal, so it never tried. Click into Chrome for ~15 seconds.
{{< /callout >}}

{{< callout type="prompt" >}}
Still not able to capture Chrome.
{{< /callout >}}

{{< callout type="response" >}}
(investigates, claims permissions are fine, blames Chrome never being frontmost, builds a probe endpoint) The only thing missing is that Chrome hasn't been frontmost during a sample tick…
{{< /callout >}}

{{< callout type="prompt" >}}
(pastes collector log) → terminal | iTerm2 | url=— | title=osascript
{{< /callout >}}

{{< callout type="response" >}}
Click into Chrome and stay ~10 seconds, paste what shows up.
{{< /callout >}}

{{< callout type="prompt" >}}
No entry.
{{< /callout >}}

{{< callout type="response" >}}
I see the bug now. The DB shows iTerm2 for everything — that's impossible. The long-running collector has stale state: `NSWorkspace.frontmostApplication()` updates via run-loop notifications, and our loop never pumps the run loop, so it froze on whatever was frontmost at launch. Switching to `Quartz.CGWindowListCopyWindowInfo`.
{{< /callout >}}

It took four rounds before Claude found the actual issue : a stale run-loop in the long-running process.
Then came the time inconsistencies. 

---

{{< callout type="prompt" >}}
How can it be idle for 80 minutes?
{{< /callout >}}

{{< callout type="response" >}}
"Away from desk" just means no input for ≥60s. Your DB shows two big idle blocks totaling ~1h 43m — that's legitimate.
{{< /callout >}}

{{< callout type="prompt" >}}
No but for an hour it can only be a max of 60 mins.
{{< /callout >}}

{{< callout type="response" >}}
You're right — let me actually check. You're right, this is a real bug. Hour 11 sums to ~113 minutes, which is impossible. Wait, I owe you a correction — the server does split across hour boundaries; my SQL query was the thing that was buggy. Confirmed — your instinct was right. Hour 11 = 88.3 minutes, still impossible. Root cause: the splitting logic snaps to UTC hour boundaries, but you're on IST (UTC+5:30), so hours fall at :30 past in local time and chunks get miscredited.
{{< /callout >}}

{{< callout type="thought" >}}
My callout of "max 60 mins" seems to have caught a genuine timezone bug Claude had initially explained away as legitimate.
{{< /callout >}}

---

{{< callout type="prompt" >}}
Why aren't the other applications showing up?
{{< /callout >}}

{{< callout type="response" >}}
Because you haven't focused any of those apps since the collector restarted. Categorization happens at sample time.
{{< /callout >}}

{{< callout type="prompt" >}}
But I opened Finder and it didn't show up.
{{< /callout >}}

{{< callout type="response" >}}
(several probes later) Found the bug. The collector uses `CGWindowListCopyWindowInfo`, which returns windows in stacking order — it picks the topmost visible window, not the focused app. Finder was active but behind Chrome. And it's bigger than Finder — `lsappinfo` says Claude is active right now but the collector returned Chrome. We've been misattributing Claude time to Chrome whenever Chrome is visible behind it. Switching the primary signal to `lsappinfo front`.
{{< /callout >}}


---

{{< callout type="prompt" >}}
Some of the hours don't seem to be accounted for the full 60 minutes.
{{< /callout >}}

{{< callout type="response" >}}
Found it. Hundreds of 5–7 second gaps between intervals — the collector drops the time between samples whenever the app/URL changes (the previous row isn't extended to bridge the gap). ~20 minutes lost per day, and 4,597 gaps across the whole DB ≈ 4.9 hours of lost time. Fixed the loop to bridge gaps and backfilled history.
{{< /callout >}}

Claude was confident most of the time. But the bugs came from pressing it anyway. Goes to show that HITL is still relevant and will be for some time.
But after all the battling, it finally it came up with a decent UI and correct metrics.

<img src="/assets/img/activity-monitor/image-6.png" style="max-width: 100%;" />


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
<img src="/assets/img/activity-monitor/image-7.png" style="max-width: 100%;" />
 and writes the answer to SQLite. To get the "focused app" right means using lsappinfo (LaunchServices) rather than AppKit or window-stacking order. 

 I tried to understand why `lsappinfo front` is better than AppKit or window-stacking order. 

{{< callout type="explanation-from-claude" >}} 

**AppKit** (NSWorkspace.frontmostApplication()) is event-driven, not poll-driven. It updates via run-loop notifications — meaning it only knows the frontmost app has changed
if the Cocoa run loop is actively spinning to process those events. A plain Python while True: sleep(5) loop never pumps the run loop, so it just freezes on whatever app
was frontmost when the process started. That's the exact bug Claude found: iTerm2 was showing for everything because that was the frontmost app at collector launch.

To use AppKit correctly you'd need to either run a full NSApplication event loop (heavyweight, turns your script into a proper Mac app) or use CFRunLoop to tick it
manually. Overkill for a 5-second poller.

**Window-stacking order** (CGWindowListCopyWindowInfo) is a different problem. Z-order (which window is visually on top) isn't the same as focus. You could have a floating
utility window from one app sitting above the window you're actively typing in. Dialogs, sheets, and menu bar apps make it worse — some apps receive keyboard focus without
having a traditional visible window at the top of the stack.

**`lsappinfo front`** sidesteps both issues. It calls into LaunchServices, which is the low-level macOS framework that manages app registration and tracks which app actually has
input focus — not visual stacking order, not a cached notification. And because it's invoked as a subprocess each time, there's no stale state: every call is a fresh
synchronous query to the OS. The downside is subprocess overhead, but at 5-second intervals that's irrelevant.
{{< /callout >}}

I also found an excellent follow-up read for [lsappinfo](https://eclecticlight.co/2020/03/04/learn-almost-everything-about-an-app-with-lsappinfo/). 


 ## So Where Did my day go?

 Let's take today as a usecase. 

<img src="/assets/img/activity-monitor/example-today.png" style="max-width: 100%;" />

I seem to have spent ~52 minutes using VSCode and 45 minutes on Chrome. 
I was away from my desk for 9 hours and 59 minutes. This is understandable since I'm tracking a 12 AM to 11.59 PM day and a large chunk of that time was spent sleeping. 
This is a great side benefit I've found to understand when I'm turning off for the day and an approximate time of when I'm back at my desk. For today, that seems to be from 12.45 AM to 8 AM. Not too bad I'd say!

 ## How can you set this up?

 Just follow the Quick Start section from the Readme file. There's a simple bootstrap file you can use at `install_launchd`. 
If you have doubts, DM me or raise an issue on the [Github repo](https://github.com/abhiramr/where-did-my-day-go). 

 ## Future work (for me) 

 - I want to try and get more insights out of this. For example, can I sync my phone activity to this dashboard on a LAN? That way I can get proper , bifurcated sleep tracking as well since as a troubling consequence of the times, the phone **is** the last and first device I use before sleeping and after I rise. 
 - I also want to try and see if I can capture the time for which the mac was shut down explicitly. 
 - Thirdly I want to be able to add applications to be tracked a little more easy to configure. Right now, adding a new app to the dashboard is a spectrum. "Just track the time" needs zero config; every focused app gets logged regardless. "Give it its own category in the API" is one line in `collector.py`. "Give it a colored donut slice and a legend label" is a few edits across three files. "Give it a top-level KPI card" is two more. The data and the visuals aren't yet driven by a single config today.
