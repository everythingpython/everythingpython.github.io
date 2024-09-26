---
title: Reading DDIA - Part 3
date: 26-09-2024
feed: show
---
## Chapter 1 - Thoughts - Cont.d 

In [[Reading DDIA - Part 2]] , I read about the second way in which design decisions are typically driven - Scalability.
This section is about what the book says is the third factor - Maintainability. 



## <u>What is a maintainable system?</u>

### My  thoughts prior to reading the section - 

Something they said in the San Diego ML Meetup struck me as my reaction as well - Maintainability is not one of the "concerns" I would have listed for a data intensive system.
But now that it is, let's think about it - 
What does it mean to **maintain** a system?
My interpretation is - how would the system be set up for functioning smoothly over time?
To that end, 
1. Part of what makes a maintainable system is something that needs minimal handholding/refactoring when a new feature is to be added. 
For e.g if a system is using cloud storage as a source or a sink and for a long time it's on Google; if for some reason, the maintainers want to support Azure or AWS, it shouldn't be too much of a hassle. This architecture should have been pre-emptively thought of. 
2. In my opinion, good documentation makes a system maintainable. In the sense that, if anyone has to be onboarded into using a platform or writing code to augment it in any way, it has to be easy to follow along and understand how to use/contribute to the platform without much difficulty. 
3. Periodic inspection of the architecture to see if there have been iterative, unintentional tech-debt creeps or something that was introduced that should not have been and fix it sooner than later. 

---

Now let's read the section .

*Reading section*

---

### Thoughts after reading the section

As in the previous two sections, the topic of maintainability is also broached by Martin along 3 design principles : 
- Operability
- Simplicity
- Evolvability
1) <u>Operability</u> - making life easy for operations involves having an "ops" team that takes care of system health monitoring, tracking root causes of platform degradation, system failures, keeping softwares up-to-date, application migration, retaining documentation as systems and personnel change etc. 
   Documentation management and maintenance is also mentioned as important as I've experienced. 
   This makes sense. For a system to stay robust over time, a dedicated team makes a lot of sense. My earliest memory of being in a software company over 12 years ago, the closest we had to "ops" teams were system administration and Database administration teams - abbreviated Sys Admins or DBAs. Over time the role has evolved to being Ops and now to Devops and now even MLOps (although the latter was not much in existence at the time of this book's writing)
1)  <u>Simplicity</u> - Managing complexity - Here the main crux is around not just keeping the architecture simple but also avoiding "accidental complexity" . Moseley and Marks define accidental complexity as complexity that does not manifest in the problem that is being solved by the software, but rather when it is being implemented. 

> [!Question Time]
>
 >❓  *Can you think of an example of this?*

One of the ways of making software simple is via abstraction, where the complex details are hidden and simple ways to interact with the system are provided - e.g. APIs for web apps, SQL for database management, high level programs that are used to interact with the machine without writing machine code  etc. 

3) <u>Evolvability</u> - Making change easy . Since with time, the only thing that remains constant is change, it's no surprise that even software systems are expected to evolve - either in user base or requirements/features or business priorities, internal components due to newer and better software being developed etc. Now how best can we introduce these changes without having to massively break what's existing? That is what is being mentioned in this subsection. Martin makes a mention of the "Agile" software practice. The Agile methodology is a whole bunch of books in itself but in short, it's a practice that believes in quick, iterative delivery that involves constant feedback and is adaptive to change. 

This brings us to the end of Chapter 1. 

Looking forward to getting into the weeds with Chapter 2 - Data Models and Query Languages!

---
*Note to self - Let's keep this up!*