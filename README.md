# memeforge
![CI](https://github.com/realMNohgee/Meme_Forge/actions/workflows/ci.yml/badge.svg) ![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg) ![License](https://img.shields.io/badge/license-MIT-blue.svg)

CLI meme template finder, captioner, and random generator.

Zero dependencies. Pure Python stdlib.

🧰 **[Tool on Hermtica Marketplace](https://hermtica.com/marketplace)**

## One Tool, Many Domains

| Domain | Use Case |
|--------|----------|
| **Developer Tools** | Generate meme-based release notes, commit messages, error messages |
| **Content Creation** | Quick social media meme text layout generation |
| **CI/CD** | Fun build failure notifications in meme format |
| **Chatbots/Agents** | Structured meme output for conversational agents |
| **Education** | Meme-based learning reinforcement |

## Agentic AI Framing

memeforge is a utility tool in the agentic-AI ecosystem — it provides structured, machine-readable meme generation that agents can use to add personality and humor to their outputs. With `--format json`, other tools and agents can consume meme data programmatically.

## Install

```bash
# Just download and run — zero deps
curl -O https://raw.githubusercontent.com/realMNohgee/Meme_Forge/main/memeforge.py
chmod +x memeforge.py
./memeforge.py template drake
```

## Usage

```bash
# Find a meme template by keyword
./memeforge.py template drake
./memeforge.py template --list

# Generate a meme with text
./memeforge.py caption drake "Using Python" "Still using Python"

# Random meme
./memeforge.py random

# JSON output
./memeforge.py random --format json
./memeforge.py template drake --format json
```

## Subcommands

- `template <keyword>` — Find meme templates by keyword. Use `--list` to see all available templates.
- `caption <template> <top_text> [bottom_text]` — Generate meme text layout with ASCII art.
- `random` — Generate a random meme combination.

## License

MIT — see [LICENSE](LICENSE)
