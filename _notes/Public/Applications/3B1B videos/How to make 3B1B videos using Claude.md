---
title: How to make 3B1B videos using Claude and Manim
feed: show
date: 2025-03-15
---
3 Blue 1 Brown is an amazing Youtube resource to learn Math and Physics concepts from!
Manim is an opensource package created by them to help generate the animations they use to teach these concepts. In this article, I will create a similar video with the help of Claude and Manim!

- Install [miktex](https://miktex.org/download)
- Install [ffmpeg](https://www.gyan.dev/ffmpeg/builds/)
	- Open powershell 
	- `choco install ffmpeg`
- Create a new virtual environment and install manim and manimgl
	- `uv pip install manim manimgl`
- Use Claude to generate a manim program for a formula or something you want to demonstrate - 
	- E.g. : https://claude.ai/share/4e8601c7-c2b1-42b6-95e0-52059378902f
- Create a program that you got out of claude - [[Manim Program for x-squared]] (https://claude.site/artifacts/fdfb2ed3-efcb-45df-b459-e0a32c5571a3)
	- Execute it - 
	- `manim -pql xsquared.py ExplainXSquared`
- This results in this beautiful 3 Blue 1 Brown like video!
	-
![[ExplainXSquared.mp4]]
References : 
- https://github.com/HarleyCoops/Math-To-Manim
- https://github.com/3b1b/manim