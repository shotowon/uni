# Hermes Telegram Study Team

This repository implements **Assignment 1 — A Team of AI Agents in Telegram with Hermes Agent**. Three independent Hermes profiles run as Telegram bots in one group, visibly delegate a real request with `@mentions`, return specialist results, and produce one final answer.

## Team design

| Agent | Responsibility | Handoff behavior |
| --- | --- | --- |
| Coordinator | Receives the human request, creates task IDs, delegates, and synthesizes the answer | Sends `[TASK <id>]`; accepts matching `[RESULT <id>]` messages |
| Researcher | Finds and summarizes credible sources | Returns one sourced result to the coordinator |
| Coder | Handles code, calculations, benchmarks, and data analysis | Returns one tested result to the coordinator |

Each agent has its own configuration, `SOUL.md`, Telegram token, conversation state, and gateway. Profiles communicate only through messages visible in the Telegram group.

## Repository layout

```text
agents/
  coordinator/{config.yaml,SOUL.md,.env.example}
  researcher/{config.yaml,SOUL.md,.env.example}
  coder/{config.yaml,SOUL.md,.env.example}
scripts/
  setup_colab.py      # creates/configures all three profiles
  start_agents.py     # starts all three Telegram gateways
COLAB.md              # Google Colab walkthrough
assignment-1-hermes-telegram-agents.md
```

Never commit a real `.env`, API key, or BotFather token. The examples contain placeholders only.

## 1. Create and configure the Telegram bots

Open the official `@BotFather` and repeat these steps for the coordinator, researcher, and coder:

1. Send `/newbot`, then provide a display name and unique username ending in `bot`.
2. Save the token BotFather returns. Each profile needs a different token.
3. Open `/mybots`, select the bot, and open **Bot Settings**.
4. Enable **Bot-to-Bot Communication** (also shown as **Bot-to-Bot Communication Mode**). This lets Telegram deliver messages written by other bots.
5. Under **Group Privacy**, choose **Turn off** so the bot can receive the group messages used by the handoff protocol.
6. Repeat for all three bots.

Create one Telegram group and add all three bots. If privacy was changed after adding a bot, remove it and add it again. Making bots group administrators is a fallback for group-message visibility, but does not replace Bot-to-Bot Communication mode.

Also collect:

- your numeric Telegram user ID (for example, from `@userinfobot`);
- the negative group chat ID, commonly beginning with `-100` (from a Telegram ID bot or Bot API update).

## 2. Install Hermes Agent

```bash
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
hermes --version
```

For Google Colab, follow [COLAB.md](COLAB.md). Colab is convenient for a defense demo, but bots stop when its runtime disconnects; use a persistent machine or VPS for continuous operation.

## 3. Configure the profiles

### Recommended setup

```bash
python scripts/setup_colab.py
```

Despite its name, this script also works on a normal Linux/macOS installation. It prompts for the IDs, three usernames, three hidden bot tokens, one hidden OpenRouter key, and a model ID. It creates profiles under `~/.hermes/profiles/`, installs each `SOUL.md`, replaces username placeholders, and writes secrets through Hermes.

### Manual setup

```bash
hermes profile create coordinator --description "Delegates requests and synthesizes answers"
hermes profile create researcher --description "Finds and summarizes credible sources"
hermes profile create coder --description "Handles code, calculations, and data analysis"

cp agents/coordinator/.env.example ~/.hermes/profiles/coordinator/.env
cp agents/researcher/.env.example ~/.hermes/profiles/researcher/.env
cp agents/coder/.env.example ~/.hermes/profiles/coder/.env
```

For each profile:

1. Replace all `CHANGE_ME...` values in its private `.env`.
2. Copy its `config.yaml` and `SOUL.md` into the corresponding profile directory.
3. In the copied soul files, replace `@COORDINATOR_BOT`, `@RESEARCH_BOT`, and `@CODE_BOT` with real usernames.
4. Keep `TELEGRAM_ALLOW_BOTS=mentions` for every profile. Specialists must receive coordinator tasks, and the coordinator must receive specialist results; `mentions` admits only bot messages that explicitly address the receiving bot.
5. Leave `TELEGRAM_HOME_CHANNEL_THREAD_ID` empty unless the group uses a particular forum topic. Hermes may populate the optional home-channel values itself.

The environment examples mirror the variable sets in the current local profiles without copying any real values.

## 4. Validate and run

```bash
hermes profile list
hermes -p coordinator doctor
hermes -p researcher doctor
hermes -p coder doctor
python scripts/start_agents.py
```

The last command keeps all gateways in the foreground and writes `coordinator.log`, `researcher.log`, and `coder.log`. Keep it running during the demo; `Ctrl+C` stops all gateways.

## 5. Demonstrate the assignment flow

Mention only the coordinator:

```text
@your_coordinator_bot Compare insertion sort and merge sort. Ask the researcher
for trustworthy complexity facts and the coder to benchmark both on random lists
of 1,000 and 10,000 integers. Recommend one for nearly sorted data.
```

Expected visible sequence:

```text
Human       -> Coordinator: request
Coordinator -> Researcher:  [TASK T-....-R]
Coordinator -> Coder:       [TASK T-....-C]
Researcher  -> Coordinator: [RESULT T-....-R]
Coder       -> Coordinator: [RESULT T-....-C]
Coordinator -> Human: final synthesis without a bot mention
```

Send `/new@bot_username` for all three bots before repeating a clean demonstration.

## Why bot loops stop

- Group traffic requires a direct mention and exclusive bot-mention routing.
- Specialists accept only `[TASK <id>]` addressed to their exact username.
- Each specialist returns exactly one `[RESULT <same-id>]` and cannot delegate.
- The coordinator accepts only results for IDs it created and never delegates from a result.
- Final answers contain no bot username.
- Collaboration depth is limited to one delegation and one result.

## Troubleshooting

- **No bot responds:** check its token, OpenRouter key, allowed user/group IDs, and log.
- **Human messages work but handoffs do not:** enable Bot-to-Bot Communication for every bot and confirm `TELEGRAM_ALLOW_BOTS=mentions` for all profiles.
- **A bot cannot see group messages:** turn Group Privacy off, remove and re-add it, or promote it to group admin.
- **All bots answer together:** verify the three strict mention variables are `true` and mention only the intended bot.
- **A gateway exits immediately:** ensure each profile has a different token, then inspect its log.
- **Prompt changes do not appear:** rerun setup or copy the updated `SOUL.md`, then start a new Telegram session.
- **Colab stops:** reconnect, rerun setup if storage reset, and restart the gateways.

## Defense guide

1. **Why multiple agents?** Narrow roles make delegation visible and results auditable. One agent is simpler and cheaper but cannot demonstrate handoffs and mixes research, execution, and synthesis.
2. **How is completion detected?** The coordinator records its suffixed task IDs and waits for one matching result from every selected specialist.
3. **What prevents infinite replies?** Mention gating, typed envelopes, known IDs, one-response specialist rules, and the one-hop protocol.
4. **Failure example:** without Bot-to-Bot Communication, the coordinator receives the human request but specialists never receive assignments. Other limits include protocol mistakes, weak sources, rate limits, and Colab shutdowns.
5. **Which model?** The configs select an OpenRouter model; the setup script allows a different model ID. Smaller/free models cost less but may omit IDs or ignore role boundaries.
6. **Prompts, skills, and tools:** `SOUL.md` defines role and protocol; skills provide procedures; tools supply capabilities such as browsing or code execution. Prompts cannot grant missing tools.
7. **Memory:** profiles keep separate sessions/state under `~/.hermes/profiles/<name>/`. They share no private memory; Telegram messages are their collaboration record.

## References

- [Assignment specification](assignment-1-hermes-telegram-agents.md)
- [Hermes Agent repository](https://github.com/NousResearch/hermes-agent)
- [Hermes Telegram guide](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/messaging/telegram.md)
- [Hermes profiles guide](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/profiles.md)
- [Telegram bot-to-bot communication](https://core.telegram.org/api/bots/bot-to-bot)
