---
title: "Building a No-Code Supplier Follow-up Assistant"
date: 2026-09-13
slug: iim-mumbai-no-code-supplier-agent-workshop
tags:
  - Agents
  - Activepieces
  - No-Code
---

This follow-up workshop for IIM Mumbai's Blended MBA participants builds a practical AI workflow without requiring participants to write code.

The use case is a supplier risk and follow-up assistant. A participant submits the order context, AI classifies the delivery risk and drafts a supplier message, and a person reviews the exact text before the workflow can send it.

## What participants build

1. A web form that captures the supplier, order and delivery context.
2. A classifier with three permitted results: Routine, AtRisk and Critical.
3. A factual supplier follow-up draft whose tone reflects the risk.
4. A Gmail approval request that pauses the workflow.
5. An approval branch that sends the message or stops without acting.

The workshop also tests two failures that matter in daily work: an exact-label classification error and a fluent draft that changes *promised* into *confirmed*.

## Slides

The interactive workshop deck is [available here](/iim-workshop-activepieces/).

You can also [download the PowerPoint](/iim-workshop-activepieces/supplier-risk-follow-up-activepieces-workshop.pptx).
