---
title: LLM Trials 1
feed: show
date: 2025-01-03
tags:
  - ollama
  - llms
---
### 3rd Jan 2024

### How to run models locally

One of the most sought after things to learn right now is about how to set up your own local LLM server and how to use LLM models locally.
With the arrival of some things like Ollama and LM Studio etc, it has become very easy.
Ollama is an orchestrator that lets you serve up models locally, models like Llama 3.1, Qwen-2.5, Phi, whatever models you have on HuggingFace.
These are available to be served up and many more.

### Setting up Ollama - 

- Depending on your operating system, download the corresponding Ollama executable from the official website - https://ollama.com/download

- Once you download and run it, it should be running as a small service in the background of your operating system. For example, if you're on Windows, you should be able to see it running on the tray on your screen's bottom right corner. 
- To download any models, check out https://ollama.com/search
- Smaller models are better for lower config laptops/desktops.

The next thing to do to mimic a local Chat-GPT-ish experience is to hook this backend Ollama server to a front-end web interface. This is where https://openwebui.com/ comes in.

### Setting up OpenWebUI - 

The Github README for OpenWebUI is extremely helpful. A few months ago when I tried it out, they only had the Docker based offering but now it seems that all that is to be done to set it up is - 

- Create a virtual environment
- Activate virtual environment
- `pip install open-webui`
- `open-webui serve`

So when you visit localhost:8000 on your browser you should be able to see a chatgpt-ish interface and the list of models you downloaded on Ollama on a top-left corner dropdown.

Happy local chatting!
