---
title: "Understanding Deepagents: Building Agents for Complex Tasks"
date: 2026-08-07
slug: understanding-deepagents-building-agents-for-complex-tasks
tags:
  - Agents
  - LLMs
  - Talks
  - Deepagents
  - Langgraph
  - Observability
  - Production
---

Notes from a talk on [Deepagents](https://www.youtube.com/watch?v=GbzEDgcuGJU) - Building agents for complex & long-running tasks.

## What is Deepagents?

**Deepagents** is a [batteries-included harness](https://github.com/langchain-ai/langgraph) for building agents that excel at **complex or long-running tasks**.

It's not just a model + tool calling framework. It's a complete infrastructure that provides everything you need to build production-grade agents.

### What is a Harness?

A harness is **surrounding support for the model and tool calling loop**{{< sidenote id="1" >}}This is the fundamental difference between a simple chatbot and a production agent—the harness is what transforms a model into a reliable system.{{< /sidenote >}}. Building an agent isn't trivial—there's a lot of engineering needed around the core concept:

- Memory management (short-term & long-term)
- Context handling
- Durable execution
- Observability
- Streaming
- Recovery & rollbacks

A harness encapsulates all of this. It's the scaffolding that makes agents reliable and production-ready{{< marginnote id="1" >}}Think of it like the suspension system in a car—you don't notice it until it's missing, but it's essential for the ride.{{< /marginnote >}}.

---

## Real-World Use Cases

Deepagents power actual Claude products:

1. **Claude Coder** — A deep agent that performs longer-running coding tasks with complex context management
2. **Deep Research** — Agents that conduct thorough research over extended periods, managing memory and accumulating findings

These aren't theoretical; they're shipping today.

---

## Architecture: Components of a Deepagent

### 1. Planning Tool

Agents perform better with structured approaches, just like humans with checklists.

**Why it works:** Breaking complex tasks into manageable steps improves execution quality and reduces errors.

### 2. Subagents

The ability to spawn and manage specialized sub-agents for delegating work. Compose complex behavior from simpler agents.

### 3. Skills

**Skills are reusable, shared prompts**{{< sidenote id="2" >}}Skills can be simple system prompts or complex workflows—what matters is that they're designed to solve specific problems consistently.{{< /sidenote >}} that help agents excel at specific tasks. By "narrowing in" on a particular task, skills enable specialized work more effectively. Think of them as expertise modules.

#### Skills Ecosystem & Standardization

**Why share skills? Why have a Skillhub?**

Skills create a standard that makes agents more capable. Instead of each agent reimplementing PowerPoint expertise, Excel analysis, or GitHub workflows from scratch, they can discover and use community-built skills{{< marginnote id="2" >}}Similar to how developers rely on npm packages instead of reinventing every library—skills reduce duplication and accelerate development.{{< /marginnote >}}. It's like npm for agent capabilities.

**The Productivity Angle:** Just as developers improve code quality through shared tools and standards, skills improve agent productivity. High-quality, shared skills make all agents more capable and productive.

### 4. Persistent Storage (File System / Abstract Backend)

Access to storage for:
- File management
- Memory and state tracking
- Sandboxed execution

### 5. Auto-Compaction Tool

Deepagents includes built-in auto-compaction{{< sidenote id="3" >}}Context window is one of the primary constraints in LLM agent design—auto-compaction helps agents stay efficient as they run longer and accumulate trace history.{{< /sidenote >}} to manage trace history and context. Users can manually summarize information, but Deepagents is exploring automatic compaction where the system condenses trace history and logs as agents run longer, keeping the system efficient without losing critical information{{< marginnote id="3" >}}This is crucial for long-running agents that might generate thousands of intermediate steps—without compaction, context becomes unmanageable.{{< /marginnote >}}.

### 6. Code Execution Sandboxes

Instead of (or in addition to) tool calling, agents can execute code in isolated sandboxes.

**Why Code Execution?**
- Powerful for data analysis—agents can write Python, JavaScript, etc. to process data
- More flexible than predefined tools—agents can solve novel problems
- Safe isolation—sandboxes prevent malicious or buggy code from affecting the system

Code execution often outperforms tool calling for computational tasks because agents have complete freedom to implement exactly what they need.

### 7. Built-in Summarization

For long-running tasks, automatic summarization prevents context window exhaustion. As tasks extend, essential knowledge is compressed and retained.

---

## Context Engineering: Progressive Disclosure

### Why Local Filesystems Are Critical

Local filesystems are **key to context engineering**. They solve the fundamental tension:

- ❌ Too much in context → bloated, slow, loses focus
- ❌ Too little in context → agent forgets, repeats work
- ✅ Right amount, at right time → optimal performance

### Storing Tool Call Results

**Why use a filesystem for live tool calls?**

When tools return large results (data analysis, multimodal content, etc.), they fill up the context window quickly and the agent may lose access to them.

**Solution:** Offload tool results to the filesystem in sequence (chronologically ordered). The agent can:
- Execute tools and capture large results
- Store results on disk in sequence
- Reference/retrieve them on demand without bloating context

### Progressive Disclosure in Action

The file system enables **progressive disclosure**—revealing and loading only information the agent needs at each step.

**Example: Skills Loading** — If an agent has access to a PowerPoint skill, it won't load it upfront. Instead, it loads the skill only when it's actually needed—when the agent detects it needs to create or modify a presentation. This keeps context clean until that moment.

---

## Productionizing Deepagents

### Technical Stack

**Deepagents is built on:**
- **Local File System** — Built-in storage for results and memory
- **[Langgraph](https://github.com/langchain-ai/langgraph)** — The underlying framework for agent orchestration
- **Dual Memory Architecture:**
  - Short-term memory — For active context
  - Long-term memory — For persistent knowledge

### Extensibility

Deepagents provides a **generic backend protocol** that allows you to add custom filestores. You're not locked into the default filesystem—you can plug in your own storage solution (S3, cloud storage, databases, etc.).

### From Local to Abstract Backends

In production, "file systems" become **abstract backends**—places where agents query for relevant information on demand:

- **Database** — Structured data and queries
- **Notion** — Documentation & knowledge bases
- **GitHub** — Code repositories & version control
- **Any API** — Custom backends via the protocol

**The Abstraction Principle:** The agent doesn't care WHERE information comes from—database, API, file, cloud storage. It just needs a consistent interface to query and retrieve data on demand.

---

## Deployment Challenges

### Human Oversight & Approval

Agents need human oversight before taking actions in the real world.

**Example:** An agent can generate a comprehensive travel plan, but a human should review and approve it before booking flights, hotels, or committing resources.

This is a critical deployment consideration—agents are powerful, but final approval should remain with humans for consequential decisions.

### Durable Execution

All agent steps must be **observable** and **reversible**.

**Requirements:**
- **Observable:** Every step the agent takes must be logged and traceable—full audit trail
- **Rollback Capability:** If something goes wrong, you must be able to undo actions

Without durable execution, agents are too risky for production. You need complete visibility and the ability to recover from failures.

### Infrastructure for Long-Running Tasks

**Streaming as a First-Class Citizen**

Users shouldn't experience latency waiting for a long-running task to complete. **Streaming results in real-time** is essential.

**Why Streaming Matters:**
- Users see progress immediately, not after 30 minutes
- Results stream back as they're generated (like Claude's token-by-token response)
- Creates better UX for long agent operations

**Debugging & Tracing**

Long-running agents are complex. You need robust debugging and tracing infrastructure. With durable execution, observable steps, and streaming, operators and developers need tools to understand what the agent is doing at each point. Full tracing enables rapid diagnosis and improvement.

### The Complexity Jump: Observability Challenges

**Simple Agents (Before):**
- Input → Tool Call → Output
- Easy to debug

**Deep Agents (Now):**
- Hundreds of tool calls, minutes of processing
- Complex to observe

**Critical debugging questions for long-running agents:**
- Is the agent on track toward its goal?
- When is the agent failing?
- Can we predict failures before they happen?

These questions require sophisticated monitoring and analysis—you can't just look at a single input/output pair.

---

## Tools & Ecosystem for Observability

### LangSmith for Debugging Long-Running Agents

[LangSmith](https://smith.langchain.com) provides tools specifically designed for the observability challenges of deep agents.

#### AI-Powered Run Analysis

LangSmith includes an AI assistant that helps you **access and understand agent runs**.

**What this enables:**
- Natural language queries over agent execution traces
- AI helps identify where things went wrong
- Understand complex multi-step agent behavior without manual inspection
- Ask questions like "why did this run fail?" and get AI-powered answers

Instead of manually sifting through hundreds of tool calls and logs, an AI assistant can help you understand what happened at a high level.

#### Quantitative Evaluation

Beyond debugging, LangSmith enables **quantitative evaluation** of agent performance. Measure success metrics, track improvements, and evaluate agents systematically rather than anecdotally.

### Getting Started with LangSmith

**Free Tier Available:**
- ✅ No credit card required
- ✅ Sign up via Google, GitHub, or email at [smith.langchain.com](https://smith.langchain.com)
- ✅ Full access to observability features (tracing, debugging, run analysis)

**Paid Tiers:** Scale with [LCUs (Compute Units) @ $1.50 each](https://www.langchain.com/pricing) and LSUs (Storage Units @ $1.00 each) for production workloads.

**Documentation:** [LangSmith Docs](https://docs.smith.langchain.com)

---

## Getting Started with Deepagents

### The Developer Experience

Deepagents is designed to make agent building easy for users. The barrier to entry is low:

1. **Write a Good Prompt** — Describe what you want the agent to do, tailored to your use case
2. **Define Prompts & Tools** — Give the agent the specific skills and capabilities it needs
3. **You're Off!** — Start building—the harness handles the rest

**Key Insight:** The complexity of the harness is hidden. Users don't need to worry about memory management, durable execution, or streaming—they just define the agent's behavior and let Deepagents handle the infrastructure.

## Resources & Documentation

- [Deepagents / Langgraph GitHub](https://github.com/langchain-ai/langgraph) — Open source framework
- [Langgraph Docs](https://langchain-ai.github.io/langgraph/) — Official documentation
- [LangSmith](https://smith.langchain.com) — Observability platform
- [Anthropic Models](https://www.anthropic.com/models) — Claude models that power agents
- [YouTube Talk](https://www.youtube.com/watch?v=GbzEDgcuGJU) — Original source

---

## Key Takeaways

- Deepagents = batteries-included harness for building sophisticated agents
- A harness is the supporting infrastructure around the model + tool loop
- Planning tools help agents break down complex tasks
- File systems enable context engineering via progressive disclosure
- In production, backends abstract away where data comes from
- Long-running agents need built-in summarization to manage context
- Subagents enable delegation and specialized task execution
- Human oversight and durable execution are critical for production
- Streaming keeps users engaged during long operations
- LangSmith provides AI-powered debugging for complex agent behavior


