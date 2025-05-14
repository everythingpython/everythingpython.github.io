---
title: Vibecoding a status dashboard
feed: show
date: 2025-05-08
---
I work in the engineering division of  a supply chain company and our development process, as most companies do, involves the setting up of our SaaS platform locally. 
This means that there are a lot of dependent services that need to be run first that support the overall execution of the platform. 

For e.g. - 
Our platform's stack requires SQL Server, Solr, Redis, Postgres, RabbitMQ, MongoDB as core services to be running first. 
Once these are all running and available, a service called WebAPI can be run that makes use of some of the above to run as well. 
Following this, there are a few more microservices that need to run, but that need not be part of this article since the underlying concept will already come through with the above being demonstrated. 

It all started when in practice on a day-to-day basis, whenever I spun up these services, every now and then, at least ONE of them would go down and at best, the error trace was clear enough from the dependent services as to what the issue was. 
But at worst, it's a rabbit hole of errors to wade through before I would land on the root cause and if one of the service's unavailability was the cause, I would feel really sad about having lost all that time. 

So having gone through this time and time again, I thought I could do something about this. 

**The first iteration of this thought was simply - a checklist.**

![Alt Text](/assets/img/applications/textual/status/t1.png)

While it got the bare minimum accomplished, in that, I now had a ready reckoner of all the services that needed to be up each time, I had no way of tracking when something went Down during operations. Additionally, if any of the services were not started , either at startup or by me, the service would simply be neglected till such time as an error would alert me. 

<div style="background-color:#ffcc00; border: 0.5px solid #5078f0; padding: 8px; border-radius: 5px; color:black"> <p> <b>🚨 Rejected coz :</b> </p> <p></p> <p> <em>Tick-boxes fixed my <b> forgetfulness</b>  but still left me blind to mid-session crashes.</em></p> </div>

---

This was not working out. 

Over time, I tried/considered a few more things - 
<ol>
<li> <b>writing a script</b> to start them all at once at startup - this failed miserably more often than not since there were some interfering services running because of other ongoing experiments.</li>
<li> <b>Creating batch scripts</b> since aliases were missing in Windows and this is predominantly a Windows based platform</li>
<li> <b>Docker-izing</b> All the services. But the amount of RAM that was consumed when I ran all the services (except SQL Server and company-specific-services) was a bit more than I liked - speaks to my lack of knowledge in optimizing Docker, I'm sure.</li>
</ol>

---
So after months of this sort of juggling, a few weeks ago, I thought - 

<div style="background-color:#ffcc00; border: 0.5px solid #5078f0; padding: 8px; border-radius: 5px; color:black"> <p> </p> <p></p> <p> <em>I've enjoyed using Textual for other projects. 
Many of these services can be polled for their status from their ports / Win process running status
Why not write a Textual app combining these two facts?</em></p> </div>

---

#### Actually let's back up - Iteration 2. 

I did not think of Textual right from the start. Because initially all I knew was, I wanted a dashboard that would monitor all the services I have running and I could look at for when something went down. 

So the first iteration of the program resulted in something like this - 
![Alt Text](/assets/img/applications/textual/status/t2.png)

<div style="background-color:#ffcc00; border: 0.5px solid #5078f0; padding: 8px; border-radius: 5px; color:black"> <p> <b> 🚨 Rejected coz :</b> </p> <p></p> <p> <em>Curling ports gave me machine-readable truth, but staring at raw JSONs is still annoying. </em></p> </div>


I was also suggested a Prometheus dashboard that I summarily rejected because of the unnecessary level of complexity I was inviting for myself for a personal setup. (Although, I Will set something up with Prometheus eventually - just for masochism's sake.)

---

####  Iteration 3

The improvement on the above was a CLI based table with ASCII ✔ and ✖ . Like so - 

![Alt Text](/assets/img/applications/textual/status/t3.png)

<div style="background-color:#ffcc00; border: 0.5px solid #5078f0; padding: 8px; border-radius: 5px; color:black"> <p> <b> 🚨 Rejected coz :</b> </p> <p></p> <p> <em>A CLI table with ✔/✖ cut my scan-time, yet couldn’t _alert_ me when a cell flipped.</em></p> </div>


---
####  Iteration 4

This is where I thought of Textual. And I asked for a service monitoring dashboard which did not look as plain as the JSON response above . The result was a little error-ridden but this is where Knowing programming while 'vibe-coding' helps. 
The changes I had to make were around providing the right command to obtain the statuses of different services, modifying the ports, fixing the styles etc. 
After the  manual fixes, which admittedly took lesser time than if I'd had to hand-code the whole script, the result was something like this - 

![Alt Text](/assets/img/applications/textual/status/t4.png)

<div style="background-color:#ffcc00; border: 0.5px solid #5078f0; padding: 8px; border-radius: 5px; color:black"> <p> <b> 🎉 NOT REJECTED!! PROGRESS  :</b> </p> <p></p> <p> <em>Now for the final lap. </em></p> </div>

---
#### Final set of iterations and the end result!

From here on, it was mostly smooth sailing. 
I got ChatGPT to fix the universal status symbols to be indicators of Success and Failure - green and red dots, tweak the borders etc. 


![Alt Text](/assets/img/applications/textual/status/t5.png)

All in all, the exercise took me less than an hour and I was very happy with it!


#### Next steps 

- I'd like to make this an installer so that it can be easily installed without the dependency installation hassle. 
- Want to implement an exponential retry and backoff when a service goes down
- ON/OFF controls for the services
	