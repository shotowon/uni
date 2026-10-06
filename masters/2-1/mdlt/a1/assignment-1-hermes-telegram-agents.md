# Assignment 1 — A Team of AI Agents in Telegram with Hermes Agent

## Overview

Build a small team of AI agents that work together inside a Telegram group, using Hermes Agent by Nous Research. Work alone or in pairs (up to 2 students).

## What to build

A Telegram group with at least **3 agents**, each running as its own Hermes Agent with its own Telegram bot:

| Agent | Job |
| --- | --- |
| Coordinator | Receives the request from a human, splits it into subtasks, sends them to the other agents, and replies with the final answer |
| Specialist 1 | Handles one kind of subtask (e.g. searching and summarising sources) |
| Specialist 2 | Handles a different kind of subtask (e.g. writing and running code) |

Pick any use case you like, for example a research helper, a study buddy, or a data-analysis assistant. The agents must hand work to each other by @mentioning one another in the group, and the whole flow must work end to end on at least one real request.

## Deliverables (50%)

| Deliverable | What to submit | Points |
| --- | --- | --- |
| Working system | Agents running in Telegram and completing a request end to end | 30 |
| Code repository | Each agent's config and `SOUL.md` (no API keys or bot tokens), plus a README with setup steps | 20 |

## Questions (50%)

Each team answers questions about its own system in a short defense (about 10 minutes). Every member must be able to answer. Expect questions like these:

1. Why did you split the work between these agents? What would change if a single agent did everything?
2. How does one agent know when to hand off work, and how does the coordinator know the task is finished?
3. What stops two bots from replying to each other forever?
4. Show a request where your system failed. What went wrong, and how would you fix it?
5. Which LLM does each agent use, and why? What would happen with a smaller model?
6. How do the prompt in `SOUL.md`, the skills and the tools change what an agent does?
7. What does each agent remember between conversations, and where is that stored?

| Criterion | Points |
| --- | --- |
| Correct and clear answers | 25 |
| Understanding of how the system works (not just what it does) | 15 |
| Honest analysis of failures and limits | 10 |

## Rules

- Deadline: Oct 5, 2026. Defenses happen in the following class.
- AI tools are allowed for building the system, but you must be able to explain every part of it yourself.
- Never commit API keys or bot tokens to the repository.
