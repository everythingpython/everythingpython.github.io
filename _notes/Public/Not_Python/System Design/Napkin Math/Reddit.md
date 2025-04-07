---
title: Napkin Math-ing Reddit
feed: show
date: 2025-04-07
---
I've done **some** Napkin Math in my different jobs in the last decade but it's been ad-hoc or purpose driven at that moment and I've not thought about it much . Today, I came across a tweet and a rabbit hole of a blog recently and I thought I'd consciously think about it for a few usecases. I'm sure I will get a lot of things wrong but over time I hope to tune it to be right. 

The first case I'm thinking about is Reddit - the self proclaimed newspaper of the Internet. It's more of a Consumer facing Online service, rather than a system level service but I think Napkin Math could apply here. 

Let's look at the front page of Reddit for starters - 

![alt-text](/assets/img/non-python/napkin-math/reddit/Napkin-Math-Reddit-1.png)

So there's a lot happening on this page. 
If we wanted to do some Napkin Math for Reddit, what all would we consider?

1)  Number of users online at any given point of time (expecting a frontpage screen)
2) Total number of users trying to log in at a single point in time (concurrent authentication)
3) Response time when any subreddit is accessed
4) Number of trending results when you click on the Search bar

I sat down and first thought of these and then I tried to ask Grok to critique my thoughts - 

- Here's what I learnt : 

<ol>
	<li> On the right track, but <b>number of users online</b> is a very vague metric. It could mean total number of users online or just those hitting the front page. A better metric would be "<b>peak concurrent users</b>"
	<li> <b>Authentication load<b> is a bit too niche a usecase unless I'm focussing on backend infrastructure. Without login behaviour data, this might also be difficult to estimate. 
	   A better metric would be "<b>peak logins per second<b>" apparently.
	<li> <b>Response time<b> does not typically fall under the umbrella of "napkin math" since Napkin math is more for quantities (e.g. users, posts) rather than performance metrics that are dependent on the system design itself. In retrospect, this seems obvious (facepalm). This should not be on the list or should be reframed as "<b>Number of subreddit page requests per second<b>" which is estimable (estimatable?) from user activity. 
	<li> <b>Number of Trending results<b> is more of a UI choice than a Napkin math metric. This could be replaced with "<b>Number of searches per second<b>" - again estimable from user activity.
</ol>
---

The initial consensus was that while my thought process was on the right track with respect to breaking up of Reddit into components, Napkin Math is all about answering a question wrt understanding a part of a system or a goal for a system - 
For e.g. perhaps Reddit's scale or its system demand. 

---

I was still a little fuzzy about what worked by way of Napkin Math for Reddit, so I Grokked a little more and it was actually helpful : 

---
>**Making It Less Fuzzy**
>
>Think of Reddit as a giant beehive: you don’t count every bee, but you can guess the swarm size, honey output, or buzzing intensity. Napkin math factors should:
>
>  - Be countable (users, posts, requests—not response times or UI elements).
>  - Be big-picture (platform-wide, not subreddit-specific or feature-specific).
> - Answer a “how much” or “how many” question you’d scribble down in a chat.
---

This was excellent. Okay, now I was starting to understand what qualified for Napkin math.

So let's say I wanted to estimate :

### How much activity happens on Reddit in an hour?

I asked this to Grok and it started with this - 

- Assuming 10M users online.

---

<div style="background-color:lightblue; border: 0.5px solid #5078f0; padding: 6px; border-radius: 5px; color:black"> <p></p><p> <b><u><i>Trust but verify</i></u><p/>
This was seemingly convincing, but what I still didn't understand was where do you pull these numbers out of for a social media site? Another question to Grok - 
<p/>

<img src="assets/img/non-python/napkin-math/reddit/Napkin-Math-Reddit-2.png" />

</div>
<div style="background-color:lightblue; border: 0.5px solid #5078f0; padding: 6px; border-radius: 5px; color:black"> <p></p><p> <p/>
I tried verifying this claim and it Was apparently close to 450 MAU as of 2023. A few more sources give me 600 MAU in 2025. But Napkin math does allow for some roughness. So let's estimate 500 MAU.
<p/>
Then the DAU, estimated as a 10th of the MAU would be 50M DAU - Grok has already rounded up to that. 
<p/>
Then accounting for the fact that maybe around 20% of the DAU are simultaneously online - that's 10M users online. Very cool to have landed here. 
</b>
</div>


---

Here's the rest of what it said - 

>- Each does 5 things (views, votes) → 50M actions/hour.
>- Let me add approx 1M comments (50M DAUs × 2% commenting ÷ 24).

So if there are 5 actions done per user per hour that includes viewing posts, upvoting them etc. and there are 10M online users, that's 50M actions per hour.

Grok estimates 2% of the 50M Daily active Users indulge in commenting every hour.

---

Here I had one more "***trust but verify***" moment.

<div style="background-color:lightblue; border: 0.5px solid #5078f0; padding: 6px; border-radius: 5px; color:black"> <p></p><p> <b><u><i>Trust but verify</i></u><p/>

<img src="assets/img/non-python/napkin-math/reddit/Napkin-Math-Reddit-3.png" />
</div>
<div style="background-color:lightblue; border: 0.5px solid #5078f0; padding: 6px; border-radius: 5px; color:black"> 
I learnt one more hindsight-is-20-20 thing from Grok in that - 
<p>
<ul>
<li>While it's tempting to conclude the number of comments occurring based on the number of users online, it's not reflective of the overall load over the course of the day for Napkin Math.</li>
<p>
<li>If I concluded that 2% of the 10M users were commenting, that could be peak online behavior activity captured. - Good for realtime capture/ AMA-type situations but not "big-picture" enough.</li></ul>
<p>
That was convincing enough for me to understand why comments were being captured at the DAU level.
</b></p></div>

**So roughly, total number of activities per hour : 51M things/hour.**

Great learning for a first use-case. 

I need to stretch my guesstimating muscles a little more over time to align better with the AI overlords and hopefully outthink them at some point. 

But for today , high five Grok!

---

PS - This, like all following posts has been a lot of discovery-during-writing type process. Hope it wasn't too jarring to read. Comments/feedback most welcome!