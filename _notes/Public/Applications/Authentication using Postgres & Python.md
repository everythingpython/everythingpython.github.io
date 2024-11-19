---
title: Authentication using Postgres & Python
feed: hide
date: 09-08-2024
tags:
  - draft
---
### 9th Aug 2024

In the edition before last, I spoke about setting up Postgres locally. If you'd like a revision, here it is - [[Postgres (post 1)]]

In this article, I wanted to learn and talk about how we can set up a basic authentication flow in Python and leverage Postgres to both register a user and then authenticate said user if they wanted to login to a page post registration. This is a classic scenario in most application workflows where user based customization is desired. 

First I need a USER table in postgres - 
What fields do I need? Really depends on the application tbh.

```
- Name
- TimeCreated
- TimeModified
- Role
- Active
```