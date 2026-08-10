---
title: "Building a Controlled Voice Expense Agent: An IIM Mumbai Workshop"
date: 2026-08-08
slug: iim-mumbai-voice-expense-agent-workshop
tags:
  - Agents
  - LangGraph
---

I ran an online workshop for IIM Mumbai's Blended MBA students on building a **Controlled Voice Expense Agent** : going from a multilingual voice note all the way to a human-approved expense ledger.

The core idea was: agents that touch real workflows (like expense reporting) shouldn't get free rein to write data on their own. This workshop walks through a small but complete system where an agent only ever *proposes*, and a human always approves before anything gets written.

## What we built

1. **Speech boundary** : a short voice note (in any of several languages) gets transcribed and translated via Sarvam AI, isolated behind a single module (`sarvam_stt.py`) so the rest of the system never deals with audio directly.
2. **LangGraph proposal graph** : a minimal `extract → validate → END` graph that turns the transcript into structured expense entries. It proposes; it never writes.
3. **Human approval boundary** : the participant reviews and edits the proposed entries in a React UI before anything is committed.
4. **Ledger tool** : only after approval does a `save_transactions` tool write to a local SQLite ledger.

Extraction runs on Groq via LiteLLM, with a deterministic fallback if no API key is configured, and Langfuse tracing wired in so participants could inspect input, output, latency, and token usage for each call : and compare traces against a small golden set.

## Slides

The full slide deck is [here](/iim-workshop-08-08-26/).

## Codebase

The workshop code (FastAPI agent/API layer + React frontend) is available as a standalone download: [voice-expense-agent.zip](/iim-workshop-08-08-26/voice-expense-agent.zip).
