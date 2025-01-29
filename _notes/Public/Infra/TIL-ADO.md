---
title: Azure Devops TIL
date: 22-01-2025
feed: show
---

#### 22nd Jan 2025

TIL about the importance of buildContext in Azure Devops Pipelines for a Docker@2 task. 😵

Kept breaking my head trying to copy files over to an image and it kept saying they weren't found. Tried a hundred combinations of paths and folder structures. 

Finally after some github-repo-hunting and documentation reading (No, LLMs didn't help) , turned out I was building a dockerfile two levels deeper from my root path and the context was set by default as the path where the Dockerfile was present. 

Once I explicitly set the buildContext, everything else fell in place. 😪 

Here's the net snippet for the Docker part of the ADO YAML :

```yaml
  - job: Build
    displayName: Build Docker Image
    steps:
      - task: Docker@2
        displayName: Build image and tag
        inputs:
          command: 'build'
          Dockerfile: ./src/intermediate_folder/Dockerfile
          buildContext: './src/'
          arguments: "--no-cache --build-arg <arg1> --build-arg <arg2> --pull -t latest "
          tags: $(Build.BuildNumber)
```

Since I had omitted the buildContext, I couldn't access the files in the src folder. 
Took me a while to figure this out. 😅

---

### Reference - 

- [ADO Documentation](https://learn.microsoft.com/en-us/azure/devops/pipelines/tasks/reference/docker-v2?view=azure-pipelines&tabs=yaml)
