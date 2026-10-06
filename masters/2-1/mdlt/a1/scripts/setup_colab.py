#!/usr/bin/env python3
"""Create three Hermes profiles without printing or committing secrets."""

from __future__ import annotations

import getpass
from pathlib import Path
import re
import shutil
import subprocess


ROOT = Path(__file__).resolve().parents[1]
PROFILES = ("coordinator", "researcher", "coder")


def ask(name: str, *, secret: bool = False, default: str = "") -> str:
    prompt = f"{name}" + (f" [{default}]" if default else "") + ": "
    value = (getpass.getpass(prompt) if secret else input(prompt)).strip()
    return value or default


def run(*args: str) -> None:
    subprocess.run(args, check=True)


def username(value: str) -> str:
    value = value.strip().lstrip("@")
    if not re.fullmatch(r"[A-Za-z0-9_]{5,32}", value):
        raise ValueError(f"Invalid Telegram username: {value!r}")
    return value


def main() -> None:
    if not shutil.which("hermes"):
        raise SystemExit("hermes is not on PATH. Run the official installer cell first.")

    human_id = ask("Your numeric Telegram user ID")
    if not re.fullmatch(r"[1-9][0-9]*", human_id):
        raise SystemExit("Telegram user ID must contain digits only.")
    group_id = ask("Telegram group ID (negative, usually -100...)")
    if not re.fullmatch(r"-[0-9]+", group_id):
        raise SystemExit("Group ID must be a negative integer.")

    names = {
        "coordinator": username(ask("Coordinator bot username (without @)")),
        "researcher": username(ask("Research bot username (without @)")),
        "coder": username(ask("Code bot username (without @)")),
    }
    tokens = {p: ask(f"{p} bot token", secret=True) for p in PROFILES}
    if len(set(tokens.values())) != 3 or any(":" not in token for token in tokens.values()):
        raise SystemExit("Supply three different BotFather tokens.")
    openrouter_key = ask("OpenRouter API key", secret=True)
    model = ask("OpenRouter model ID", default="nvidia/nemotron-3-ultra-550b-a55b:free")

    hermes_root = Path.home() / ".hermes" / "profiles"
    for profile in PROFILES:
        profile_dir = hermes_root / profile
        if not profile_dir.exists():
            run("hermes", "profile", "create", profile, "--description", {
                "coordinator": "Delegates study requests and synthesizes final answers.",
                "researcher": "Finds and summarizes credible sources.",
                "coder": "Writes, runs, and explains code and calculations.",
            }[profile])

        soul = (ROOT / "agents" / profile / "SOUL.md").read_text()
        soul = soul.replace("@COORDINATOR_BOT", f"@{names['coordinator']}")
        soul = soul.replace("@RESEARCH_BOT", f"@{names['researcher']}")
        soul = soul.replace("@CODE_BOT", f"@{names['coder']}")
        (profile_dir / "SOUL.md").write_text(soul)

        # Use Hermes' writer so values land in the correct config/.env files.
        prefix = ("hermes", "-p", profile, "config", "set")
        settings = {
            "model.provider": "openrouter",
            "model.default": model,
            "telegram.require_mention": "true",
            "telegram.exclusive_bot_mentions": "true",
            "telegram.bots_require_mention": "true",
            # Admit only bot-authored messages that explicitly mention this bot.
            "TELEGRAM_ALLOW_BOTS": "mentions",
            "TELEGRAM_BOT_TOKEN": tokens[profile],
            "TELEGRAM_ALLOWED_USERS": human_id,
            "TELEGRAM_GROUP_ALLOWED_CHATS": group_id,
            "OPENROUTER_API_KEY": openrouter_key,
        }
        for key, value in settings.items():
            run(*prefix, key, value)

    print("\nConfigured all profiles. Secrets are only under ~/.hermes/profiles/*/.env")
    print("Next: enable Bot-to-Bot Communication Mode in BotFather for all three bots,")
    print("add them to the group, then run: python scripts/start_agents.py")


if __name__ == "__main__":
    main()
