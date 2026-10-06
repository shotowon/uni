# Run the team in Google Colab

Colab already provides Linux. Hermes' official installer manages its Python environment with Astral `uv`, so you do not need to manually `pip install` the project.

## Cell 1 — install Hermes (includes `uv`)

```bash
!curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
import os
os.environ["PATH"] = f'{os.path.expanduser("~")}/.local/bin:' + os.environ["PATH"]
!hermes --version
```

If `hermes` is installed somewhere else, the installer prints the path; add that directory to `PATH` in the Python line.

## Cell 2 — obtain this repository

Push this folder to a private or public Git repository **without secrets**, then:

```python
REPO_URL = "https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git"
```

```bash
!git clone "$REPO_URL" /content/hermes-team
%cd /content/hermes-team
```

Alternatively, upload a zip in Colab's Files panel, unzip it under `/content/hermes-team`, and `%cd` there.

## Cell 3 — create profiles and enter secrets

```bash
!python scripts/setup_colab.py
```

The script prompts for:

- your numeric Telegram user ID;
- the group ID;
- three bot usernames and tokens;
- one OpenRouter key;
- an OpenRouter model ID (press Enter for the default).

The token/key prompts are hidden. Do not put secrets directly in a notebook because saved notebooks commonly leak them.

## Cell 4 — validate profiles

```bash
!hermes profile list
!hermes -p coordinator doctor
!hermes -p researcher doctor
!hermes -p coder doctor
```

Warnings about optional tools are acceptable; provider or Telegram credential errors are not.

## Cell 5 — start all bots

```bash
!python scripts/start_agents.py
```

Keep this cell running during the demo. Stop it with the square stop button or `Ctrl+C`.

If something fails, open another cell and inspect logs without displaying `.env` files:

```bash
!tail -n 80 coordinator.log
!tail -n 80 researcher.log
!tail -n 80 coder.log
```

