---
title: GoogleNews using Python
feed: show
date: 2024-11-22
---
### 22nd Nov 2024

*This article is part of something I'm building up to* 

I wanted to find a way in which I can get news off of Google News programatically and something that doesn't need to me be authenticated for it. I wondered if I should build a scraper for it, but thankfully, there's a Python package already that does it  - [GoogleNews on Pypi](https://pypi.org/project/GoogleNews/)

I installed it in a new [`uv` virtual environment](https://everythingpython.substack.com/p/virtual-environments-using-uv) using `pip install googlenews` and it was pretty easy to use . 

For example, if I want to fetch the news for the last 1 day for Bangalore - 

```python
>>> from GoogleNews import GoogleNews
>>> googlenews = GoogleNews(period='1d')
>>> googlenews.get_news('Bangalore')
>>>for i in googlenews.results()[:10]:
       print(i["title"])
```

This prints (as of today, the 22nd) the news for yesterday, the 21st of Nov - 

```text
Bangalore Races
Why a Man With MS Degree From Germany is Begging on Bengaluru Streets
Bengaluru ranks 7th in APAC on residential price rise
Bengaluru police bust honey-trapping gang for extorting ₹2.25 crore from techie
Bengaluru traffic police issue advisory against scams: ‘verify identities before providing information’
Air India to begin training facility and courses in Bengaluru for Air Craft engineers
Congress plans to shift winning MLAs to Bengaluru, Karnataka’s dy CM to help party’s Maha unit
Drug Racket Busted In Bengaluru, 318 Kg Marijuana Worth Rs 3 Crore Seized
IndiGo Launches Direct Flights to Mauritius from Bengaluru; Check Days, Time, & More
Viral video: Techie found begging on Bengaluru streets
```

And as we can see from Google News, this is decently accurate! 

![Alt Text](/assets/img/Applications/GoogleNews.png)


If a new topic is desired, we must first run `googlenews.clear()` to flush the earlier records. 

For example, if I now want to fetch the latest news about GenAI, I'll execute -

```python
>>> googlenews.clear()
>>> googlenews.get_news('Gen AI')
>>> for i in googlenews.results()[:10]:
...     print(f'- {i["title"]}')
```

Which gives me - 

```markdown
- Samsung introduces its second-gen AI model 'Gauss2': All you need to know
- Philips set to unveil next-gen AI MRI system
- The AI agenda
- CIOs contend with gen AI growing pains
- Samsung Gauss 2: Next-Gen AI Models for Efficiency, Performance, and Multilingual Support
- The mesmerising blue eyes of generative AI
- Deloitte: GenAI paving the way for transformative future for comms
- Capgemini, Mistral AI and Microsoft collaborate to further accelerate adoption of generative AI technologies
- Generative AI Tracker: Tech Industry Activity in Q2FY2025
- AI to amplify the $2 trillion market opportunity for cybersecurity providers – McKinsey
```

