#!/usr/bin/env python3
"""memeforge — CLI meme template finder, captioner, and random generator.

Zero dependencies. Pure Python stdlib. MIT License.
"""
from __future__ import annotations

import argparse
import json
import random
import sys
from typing import Dict, List, Tuple

# ── Meme Template Database (~50 popular templates) ──────────────────────────

TEMPLATES: Dict[str, Dict] = {
    "drake": {
        "name": "Drake Hotline Bling",
        "keywords": ["drake", "hotline", "bling", "no", "yes", "reject", "approve"],
        "zones": {"top": "top-left (reject)", "bottom": "bottom-right (approve)"},
        "default_top": "Using top panel",
        "default_bottom": "Using bottom panel",
        "ascii": r"""
   ╭──────────────╮      ╭──────────────╮
   │  🙅 TOP TEXT │      │  👉 BOTTOM   │
   │              │      │     TEXT     │
   ╰──────────────╯      ╰──────────────╯
        (╯°□°）╯              ¯\_(ツ)_/¯
""",
    },
    "distracted-boyfriend": {
        "name": "Distracted Boyfriend",
        "keywords": ["distracted", "boyfriend", "girlfriend", "looking", "other", "woman"],
        "zones": {"top": "boyfriend (distracted by)", "bottom": "girlfriend (ignored)"},
        "default_top": "The new thing",
        "default_bottom": "The old thing",
        "ascii": r"""
    👨 (looking)        👩 (ignored)
     ╲   ❤️?   ╱
      👩‍🦰 (new thing)
""",
    },
    "two-buttons": {
        "name": "Two Buttons",
        "keywords": ["buttons", "sweating", "choice", "two", "difficult"],
        "zones": {"top": "left button", "bottom": "right button"},
        "default_top": "Obvious choice",
        "default_bottom": "Also obvious choice",
        "ascii": r"""
         😰  (sweating)
    ┌─────────┐    ┌─────────┐
    │ TOP     │    │ BOTTOM  │
    └─────────┘    └─────────┘
""",
    },
    "change-my-mind": {
        "name": "Change My Mind",
        "keywords": ["change", "mind", "crowder", "table", "sign"],
        "zones": {"top": "sign text"},
        "default_top": "Unpopular opinion",
        "default_bottom": "",
        "ascii": r"""
    🤔 Change My Mind
    ┌─────────────────┐
    │ TOP TEXT        │
    └─────────────────┘
         ☕️
""",
    },
    "one-does-not-simply": {
        "name": "One Does Not Simply",
        "keywords": ["boromir", "simply", "lotr", "does not"],
        "zones": {"top": "One does not simply...", "bottom": ""},
        "default_top": "One does not simply",
        "default_bottom": "walk into Mordor",
        "ascii": r"""
         🧔 (Boromir)
    ┌───────────────────────┐
    │ One does not simply   │
    │     TOP TEXT          │
    └───────────────────────┘
""",
    },
    "this-is-fine": {
        "name": "This Is Fine",
        "keywords": ["fine", "fire", "dog", "burning", "ok"],
        "zones": {"top": "thought bubble"},
        "default_top": "This is fine.",
        "default_bottom": "",
        "ascii": r"""
          🔥  🔥
       ┌──🐶──┐
       │ TOP  │
       └──────┘
       🔥  ☕️  🔥
""",
    },
    "surprised-pikachu": {
        "name": "Surprised Pikachu",
        "keywords": ["pikachu", "surprised", "shocked", "pokemon"],
        "zones": {"top": "what happened", "bottom": "reaction"},
        "default_top": "When you get caught",
        "default_bottom": "⚡😮⚡",
        "ascii": r"""
       ⚡😮⚡
      (Pikachu)
    ┌───────────┐
    │ TOP TEXT  │
    └───────────┘
""",
    },
    "roll-safe": {
        "name": "Roll Safe",
        "keywords": ["roll", "safe", "think", "smart", "temple"],
        "zones": {"top": "smart thought"},
        "default_top": "Can't get bugs if you don't write code",
        "default_bottom": "",
        "ascii": r"""
         🤔💭
    👉  ┌─────────────┐
        │   TOP TEXT  │
        └─────────────┘
""",
    },
    "expanding-brain": {
        "name": "Expanding Brain",
        "keywords": ["brain", "expanding", "galaxy", "levels", "bigger"],
        "zones": {"top": "small brain", "bottom": "galaxy brain"},
        "default_top": "Normal idea",
        "default_bottom": "Genius idea",
        "ascii": r"""
    🧠  →  🧠💡  →  🧠✨  →  🌌
    ┌──────────┐  ┌──────────┐
    │ TOP TEXT │  │ BOTTOM   │
    └──────────┘  └──────────┘
""",
    },
    "doge": {
        "name": "Doge",
        "keywords": ["doge", "shiba", "much", "wow", "comic sans"],
        "zones": {"top": "top left", "bottom": "bottom right"},
        "default_top": "such tool",
        "default_bottom": "much CLI",
        "ascii": r"""
        🐕 much wow
    ┌─────────┐  ┌─────────┐
    │  TOP    │  │ BOTTOM  │
    └─────────┘  └─────────┘
""",
    },
    "gru-plan": {
        "name": "Gru's Plan",
        "keywords": ["gru", "plan", "minions", "despicable"],
        "zones": {"top": "panel 1", "bottom": "panel 4"},
        "default_top": "I have a plan",
        "default_bottom": "I have no plan",
        "ascii": r"""
    ┌──────────┐   ┌──────────┐
    │ 1. TOP   │ → │ 4. BOTTOM│
    └──────────┘   └──────────┘
        🕵️  Gru
""",
    },
    "winnie-the-pooh": {
        "name": "Winnie the Pooh",
        "keywords": ["pooh", "winnie", "fancy", "tuxedo", "normal"],
        "zones": {"top": "normal pooh", "bottom": "fancy pooh"},
        "default_top": "Normal thing",
        "default_bottom": "Fancy thing",
        "ascii": r"""
       🧸 Normal        🎩 Fancy
    ┌──────────┐    ┌──────────┐
    │ TOP TEXT │    │ BOTTOM   │
    └──────────┘    └──────────┘
""",
    },
    "monkey-puppet": {
        "name": "Monkey Puppet",
        "keywords": ["monkey", "puppet", "side-eye", "nervous"],
        "zones": {"top": "saying one thing", "bottom": "really doing another"},
        "default_top": "I'll start the diet tomorrow",
        "default_bottom": "orders pizza now",
        "ascii": r"""
       🙈 (nervous look)
    ┌─────────────────────┐
    │ TOP TEXT            │
    │   👀                │
    │      BOTTOM TEXT    │
    └─────────────────────┘
""",
    },
    "galaxy-brain": {
        "name": "Galaxy Brain",
        "keywords": ["galaxy", "brain", "levels", "ascending"],
        "zones": {"top": "lowest level", "bottom": "highest level"},
        "default_top": "Small brain",
        "default_bottom": "Galaxy brain",
        "ascii": r"""
    🧠 → 💡 → ✨ → 🌌 → 🌠
      TOP             BOTTOM
""",
    },
    "woman-yelling-at-cat": {
        "name": "Woman Yelling at Cat",
        "keywords": ["yelling", "cat", "arguing", "housewives"],
        "zones": {"top": "woman (angry)", "bottom": "cat (confused)"},
        "default_top": "ME: THE DEADLINE IS TOMORROW",
        "default_bottom": "The bug: 🐱 meow?",
        "ascii": r"""
    😡 👩 YELLING:        🐱 Confused cat:
    ┌──────────────┐    ┌──────────────┐
    │ TOP TEXT     │    │ BOTTOM TEXT  │
    └──────────────┘    └──────────────┘
""",
    },
    "evil-kermit": {
        "name": "Evil Kermit",
        "keywords": ["kermit", "evil", "hood", "inner", "me"],
        "zones": {"top": "good kermit", "bottom": "evil hooded kermit"},
        "default_top": "Write unit tests",
        "default_bottom": "Push to production",
        "ascii": r"""
       🐸 Me:             🐸👿 Evil Me:
    ┌──────────────┐  ┌──────────────┐
    │ TOP TEXT     │  │ BOTTOM TEXT  │
    └──────────────┘  └──────────────┘
""",
    },
    "harold-hide-pain": {
        "name": "Harold Hide the Pain",
        "keywords": ["harold", "hide", "pain", "smile", "suffering"],
        "zones": {"top": "what you say", "bottom": "what you feel"},
        "default_top": "Everything is great!",
        "default_bottom": "😬 (dying inside)",
        "ascii": r"""
       😬 (pained smile)
    ┌────────────────────┐
    │ TOP TEXT           │
    │    (BOTTOM TEXT)   │
    └────────────────────┘
""",
    },
    "bernie-sanders-mittens": {
        "name": "Bernie Sanders Mittens",
        "keywords": ["bernie", "sanders", "mittens", "inauguration", "chair"],
        "zones": {"top": "Bernie asks...", "bottom": ""},
        "default_top": "I am once again asking",
        "default_bottom": "for your code review",
        "ascii": r"""
    👴🧥🧤 (sitting in chair)
    ┌──────────────────────────┐
    │ I am once again asking   │
    │      TOP TEXT            │
    └──────────────────────────┘
""",
    },
    "disaster-girl": {
        "name": "Disaster Girl",
        "keywords": ["disaster", "girl", "fire", "smirk", "chaos"],
        "zones": {"top": "the disaster", "bottom": "the smirk"},
        "default_top": "Production is on fire",
        "default_bottom": "😏 It was my commit",
        "ascii": r"""
       😏 (smirk)
       👧
    ┌──────────────┐
    │ TOP TEXT     │
    │ 🔥🔥🔥       │
    └──────────────┘
""",
    },
    "think-about-it": {
        "name": "Think About It",
        "keywords": ["think", "about", "eddie", "murphy", "tap"],
        "zones": {"top": "brain tap thought"},
        "default_top": "Can't have bugs in production",
        "default_bottom": "if you never deploy",
        "ascii": r"""
    👉🧠 (tapping temple)
    ┌─────────────────────┐
    │ TOP TEXT            │
    └─────────────────────┘
""",
    },
    "always-has-been": {
        "name": "Always Has Been",
        "keywords": ["always", "has", "been", "astronaut", "space", "gun"],
        "zones": {"top": "astronaut 1", "bottom": "astronaut 2 (gun)"},
        "default_top": "Wait, it's all tech debt?",
        "default_bottom": "Always has been. 🔫",
        "ascii": r"""
       🧑‍🚀           🧑‍🚀🔫
    ┌──────────┐  ┌──────────┐
    │ TOP TEXT │  │ BOTTOM   │
    └──────────┘  └──────────┘
""",
    },
    "bike-fall": {
        "name": "Bike Fall",
        "keywords": ["bike", "fall", "stick", "blame"],
        "zones": {"top": "puts stick in own wheel", "bottom": "blames someone"},
        "default_top": "I wrote the bug",
        "default_bottom": "Why would QA do this?",
        "ascii": r"""
    🚲💥 (falling)
    ┌──────────┐  ┌──────────┐
    │ TOP TEXT │→ │ BOTTOM   │
    └──────────┘  └──────────┘
""",
    },
    "left-exit-12": {
        "name": "Left Exit 12 Off Ramp",
        "keywords": ["exit", "ramp", "car", "off", "highway", "swerve"],
        "zones": {"top": "straight road", "bottom": "exit ramp (better)"},
        "default_top": "The safe approach",
        "default_bottom": "The radical alternative",
        "ascii": r"""
    ──── TOP ────
         ↘️ BOTTOM
    🚗💨
""",
    },
    "futurama-fry": {
        "name": "Futurama Fry",
        "keywords": ["futurama", "fry", "suspicious", "squint"],
        "zones": {"top": "Can't tell if...", "bottom": "Or..."},
        "default_top": "Can't tell if bug or feature",
        "default_bottom": "or both",
        "ascii": r"""
       🤨 (Fry squinting)
    ┌──────────────────────┐
    │ TOP TEXT             │
    │      BOTTOM TEXT     │
    └──────────────────────┘
""",
    },
    "first-world-problems": {
        "name": "First World Problems",
        "keywords": ["first", "world", "problems", "crying", "rich"],
        "zones": {"top": "first world complaint"},
        "default_top": "My CI takes 2 whole minutes",
        "default_bottom": "",
        "ascii": r"""
       😭 (crying)
    ┌────────────────────────┐
    │ First World Problems:  │
    │      TOP TEXT          │
    └────────────────────────┘
""",
    },
    "unsettled-tom": {
        "name": "Unsettled Tom",
        "keywords": ["unsettled", "tom", "jerry", "worried", "mouse"],
        "zones": {"top": "what causes unease"},
        "default_top": "When the junior dev says 'It works on my machine'",
        "default_bottom": "",
        "ascii": r"""
    🐭😰 (Unsettled Tom)
    ┌───────────────────┐
    │ TOP TEXT          │
    └───────────────────┘
""",
    },
    "spongebob-mocking": {
        "name": "SpongeBob Mocking",
        "keywords": ["spongebob", "mocking", "chicken", "alternating"],
        "zones": {"top": "mOcKiNg tExT"},
        "default_top": "yOu WoUlDn'T jUsT pUsH tO mAiN",
        "default_bottom": "",
        "ascii": r"""
    🧽🐔 (mocking SpongeBob)
    ┌───────────────────────┐
    │ TOP TEXT              │
    └───────────────────────┘
""",
    },
    "trump-wrong": {
        "name": "Trump Wrong",
        "keywords": ["trump", "wrong", "fake", "news"],
        "zones": {"top": "statement", "bottom": "WRONG"},
        "default_top": "AI will replace all developers in 2025",
        "default_bottom": "WRONG ❌",
        "ascii": r"""
    ┌───────────────────┐
    │ TOP TEXT          │
    │ ❌ WRONG          │
    └───────────────────┘
""",
    },
    "anakin-padme": {
        "name": "Anakin & Padme",
        "keywords": ["anakin", "padme", "for", "right", "star wars"],
        "zones": {"top": "Padme asks", "bottom": "Anakin responds"},
        "default_top": "You did write tests, right?",
        "default_bottom": "...",
        "ascii": r"""
    👩‍🦱 Padme:             👦 Anakin:
    ┌──────────────┐    ┌──────────────┐
    │ TOP TEXT     │    │ BOTTOM TEXT  │
    └──────────────┘    └──────────────┘
""",
    },
    "waiting-skeleton": {
        "name": "Waiting Skeleton",
        "keywords": ["waiting", "skeleton", "bench", "long", "time"],
        "zones": {"top": "waiting for..."},
        "default_top": "Waiting for code review",
        "default_bottom": "",
        "ascii": r"""
       💀☠️ (on bench)
    ┌────────────────────┐
    │ Waiting for:       │
    │    TOP TEXT        │
    └────────────────────┘
""",
    },
    "is-this-a-pigeon": {
        "name": "Is This a Pigeon?",
        "keywords": ["pigeon", "butterfly", "meme", "is this"],
        "zones": {"top": "points at thing", "bottom": "Is this a pigeon?"},
        "default_top": "Me: points at untested code",
        "default_bottom": "Is this production-ready?",
        "ascii": r"""
    🦋 (butterfly?)
     🧑                  🕊️
    ┌──────────────┐
    │ TOP TEXT     │
    └──────────────┘
    Is this a BOTTOM TEXT?
""",
    },
    "mike-wazowski-face-swap": {
        "name": "Mike Wazowski Face Swap",
        "keywords": ["mike", "wazowski", "sulley", "face", "swap", "monster"],
        "zones": {"top": "Sulley with Mike's face", "bottom": "Mike (horrified)"},
        "default_top": "When someone messes with your code",
        "default_bottom": "😱",
        "ascii": r"""
    👹 Sulley face       👁️😱 Mike
    ┌──────────────┐  ┌──────────────┐
    │ TOP TEXT     │  │ BOTTOM TEXT  │
    └──────────────┘  └──────────────┘
""",
    },
    "spider-man-pointing": {
        "name": "Spider-Man Pointing",
        "keywords": ["spider", "man", "pointing", "identical", "same"],
        "zones": {"top": "spider-man 1", "bottom": "spider-man 2"},
        "default_top": "Two microservices",
        "default_bottom": "that do the same thing",
        "ascii": r"""
    🕷️👉         👈🕷️
    ┌─────────┐ ┌─────────┐
    │ TOP     │ │ BOTTOM  │
    └─────────┘ └─────────┘
""",
    },
    "computer-fist": {
        "name": "Computer Fist",
        "keywords": ["computer", "fist", "punch", "rage", "desk"],
        "zones": {"top": "what caused the rage"},
        "default_top": "git merge main --no-ff",
        "default_bottom": "",
        "ascii": r"""
    👊💥🖥️
    ┌───────────────────┐
    │ TOP TEXT          │
    └───────────────────┘
""",
    },
    "homer-bush": {
        "name": "Homer Backs Into Bushes",
        "keywords": ["homer", "bush", "back", "disappear", "simpsons"],
        "zones": {"top": "thing to disappear from"},
        "default_top": "When someone asks about the prod outage",
        "default_bottom": "",
        "ascii": r"""
    🏃‍♂️🌿🌿🌿
    ┌────────────────────┐
    │ TOP TEXT           │
    └────────────────────┘
""",
    },
    "batman-slapping-robin": {
        "name": "Batman Slapping Robin",
        "keywords": ["batman", "robin", "slap", "argument", "wrong"],
        "zones": {"top": "slap reason"},
        "default_top": "NO! You don't push on Friday!",
        "default_bottom": "",
        "ascii": r"""
    🦇👋😵 (slap)
    ┌──────────────────────┐
    │ TOP TEXT             │
    └──────────────────────┘
""",
    },
    "the-rock-driving": {
        "name": "The Rock Driving",
        "keywords": ["rock", "driving", "look", "stare"],
        "zones": {"top": "what he sees", "bottom": "his reaction"},
        "default_top": "The prod logs at 3 AM",
        "default_bottom": "😐",
        "ascii": r"""
    🚗💨   👨 (driving)
    ┌──────────────┐
    │ TOP TEXT     │
    │   BOTTOM     │
    └──────────────┘
""",
    },
    "confused-nick-young": {
        "name": "Confused Nick Young",
        "keywords": ["nick", "young", "confused", "question", "marks"],
        "zones": {"top": "confusing thing"},
        "default_top": "When the build fails but the error is in node_modules",
        "default_bottom": "",
        "ascii": r"""
    🤨❓❓❓ (Nick Young)
    ┌────────────────────┐
    │ TOP TEXT           │
    └────────────────────┘
""",
    },
    "modern-problems": {
        "name": "Modern Problems Require Modern Solutions",
        "keywords": ["modern", "problems", "solutions", "tap", "temple"],
        "zones": {"top": "the problem", "bottom": "the solution"},
        "default_top": "CI is slow",
        "default_bottom": "Remove all tests",
        "ascii": r"""
    🤔                    💡
    ┌──────────────┐  ┌──────────────┐
    │ TOP TEXT     │→ │ BOTTOM TEXT  │
    └──────────────┘  └──────────────┘
""",
    },
    "phil-collins": {
        "name": "Phil Collins Drumming",
        "keywords": ["phil", "collins", "drum", "intense", "music"],
        "zones": {"top": "drum intensity"},
        "default_top": "Deploying to production on Friday at 4:59 PM",
        "default_bottom": "",
        "ascii": r"""
    🥁🥁🥁 (Phil Collins)
    ┌─────────────────────────┐
    │ TOP TEXT                │
    └─────────────────────────┘
""",
    },
    "blinking-guy": {
        "name": "Blinking Guy",
        "keywords": ["blinking", "guy", "white", "confused", "surprised"],
        "zones": {"top": "what he just heard"},
        "default_top": "Wait, you don't use version control?",
        "default_bottom": "",
        "ascii": r"""
    👦😳 (blinking intensely)
    ┌───────────────────────┐
    │ TOP TEXT              │
    └───────────────────────┘
""",
    },
    "elmo-fire": {
        "name": "Elmo Fire",
        "keywords": ["elmo", "fire", "burn", "chaos", "sesame"],
        "zones": {"top": "what's burning"},
        "default_top": "The production database",
        "default_bottom": "🔥🔥🔥",
        "ascii": r"""
    🔥🔥🔥
    👹 (Elmo)
    ┌─────────────────┐
    │ TOP TEXT        │
    └─────────────────┘
""",
    },
    "pickle-rick": {
        "name": "Pickle Rick",
        "keywords": ["pickle", "rick", "rick and morty", "scientist"],
        "zones": {"top": "Pickle Rick!"},
        "default_top": "I turned myself into a CLI tool, Morty!",
        "default_bottom": "I'm Pickle Rick! 🥒",
        "ascii": r"""
    🥒😎 (Pickle Rick)
    ┌──────────────────────┐
    │ TOP TEXT             │
    │    BOTTOM TEXT       │
    └──────────────────────┘
""",
    },
    "dog-in-burning-house": {
        "name": "Dog in Burning House",
        "keywords": ["dog", "burning", "house", "fire", "cup"],
        "zones": {"top": "what's happening"},
        "default_top": "Production is on fire",
        "default_bottom": "",
        "ascii": r"""
    🏠🔥🔥🔥
    🐕☕️ This is fine.
    ┌──────────────────┐
    │ TOP TEXT         │
    └──────────────────┘
""",
    },
    "banana-dance": {
        "name": "Banana Dance",
        "keywords": ["banana", "dance", "peanut", "butter", "jelly"],
        "zones": {"top": "dance caption"},
        "default_top": "It's Friday and the deploy succeeded",
        "default_bottom": "🍌🕺🍌",
        "ascii": r"""
    🍌  🕺  🍌
    ┌───────────────────┐
    │ TOP TEXT          │
    └───────────────────┘
       BOTTOM TEXT
""",
    },
    "guy-looking-back": {
        "name": "Guy Looking Back",
        "keywords": ["looking", "back", "girlfriend", "other", "girl"],
        "zones": {"top": "what he looks at", "bottom": "what he ignores"},
        "default_top": "New shiny framework",
        "default_bottom": "My current tech stack",
        "ascii": r"""
    👨 (looking) → 👩 (ignored)
    ┌──────────┐    ┌──────────┐
    │ TOP TEXT │    │ BOTTOM   │
    └──────────┘    └──────────┘
""",
    },
    "shaq-hot-sauce": {
        "name": "Shaq Hot Sauce",
        "keywords": ["shaq", "hot", "sauce", "spicy", "wing"],
        "zones": {"top": "Shaq suffering"},
        "default_top": "When they ask for one more feature before launch",
        "default_bottom": "",
        "ascii": r"""
    🏀😰🔥 (Shaq sweating)
    ┌──────────────────────┐
    │ TOP TEXT             │
    └──────────────────────┘
""",
    },
    "shut-up-and-take-my-money": {
        "name": "Shut Up and Take My Money",
        "keywords": ["shut", "up", "money", "fry", "take", "throw"],
        "zones": {"top": "what you want"},
        "default_top": "A CI pipeline that actually works",
        "default_bottom": "💸💸💸",
        "ascii": r"""
    🧑💸💸💸
    ┌──────────────────────────┐
    │ Shut up and take my...   │
    │     TOP TEXT             │
    └──────────────────────────┘
""",
    },
    "i-dont-always": {
        "name": "I Don't Always... But When I Do",
        "keywords": ["always", "when", "most", "interesting", "man"],
        "zones": {"top": "I don't always X", "bottom": "But when I do, Y"},
        "default_top": "I don't always write bugs",
        "default_bottom": "But when I do, they're in production",
        "ascii": r"""
    🧔🍺 (Most Interesting Man)
    ┌─────────────────────────┐
    │ TOP TEXT                │
    │      BOTTOM TEXT        │
    └─────────────────────────┘
""",
    },
    "epic-handshake": {
        "name": "Epic Handshake",
        "keywords": ["handshake", "epic", "agreement", "muscular", "two"],
        "zones": {"top": "thing 1", "bottom": "thing 2", "middle": "agreement"},
        "default_top": "Developers",
        "default_bottom": "QA Engineers",
        "middle": "Blaming each other",
        "ascii": r"""
    💪 TOP 🤝 BOTTOM 💪
    ┌─────────────────┐
    │    AGREEMENT    │
    └─────────────────┘
""",
    },
}


# ── CLI ────────────────────────────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--format", choices=["text", "json"], default="text",
                        help="Output format (default: text)")

    p = argparse.ArgumentParser(
        prog="memeforge",
        description="CLI meme template finder, captioner, and random generator. Zero deps.",
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    # template
    tmpl = sub.add_parser("template", parents=[common],
                          help="Find meme templates by keyword")
    tmpl.add_argument("keyword", nargs="?", help="Keyword to search for")
    tmpl.add_argument("--list", action="store_true",
                      help="List all available templates")
    tmpl.set_defaults(func=cmd_template)

    # caption
    cap = sub.add_parser("caption", parents=[common],
                         help="Generate meme text layout")
    cap.add_argument("template", help="Template name or keyword")
    cap.add_argument("top_text", help="Top text for the meme")
    cap.add_argument("bottom_text", nargs="?", default="",
                     help="Bottom text for the meme (optional)")
    cap.set_defaults(func=cmd_caption)

    # random
    rnd = sub.add_parser("random", parents=[common],
                         help="Generate a random meme combination")
    rnd.set_defaults(func=cmd_random, keyword=None, top_text=None, bottom_text=None)

    return p


def _find_template(keyword: str) -> Tuple[str, Dict] | None:
    """Find a template by exact slug or keyword match."""
    kw_lower = keyword.lower().strip()
    if kw_lower in TEMPLATES:
        return kw_lower, TEMPLATES[kw_lower]
    for slug, data in TEMPLATES.items():
        if kw_lower in slug:
            return slug, data
        if any(kw_lower in k for k in data.get("keywords", [])):
            return slug, data
    return None


def _as_text(slug: str, data: Dict, top: str, bottom: str) -> str:
    lines = [
        f"{'═' * 60}",
        f"  Template: {data['name']}  (slug: {slug})",
        f"{'═' * 60}",
        f"  Top Text:    {top or '(none)'}",
        f"  Bottom Text: {bottom or '(none)'}",
        "",
        data.get("ascii", "  [no ASCII art available]"),
        f"{'═' * 60}",
    ]
    return "\n".join(lines)


def _as_json(slug: str, data: Dict, top: str, bottom: str) -> str:
    return json.dumps({
        "template": slug,
        "name": data["name"],
        "top_text": top,
        "bottom_text": bottom,
        "zones": data.get("zones", {}),
        "format": "meme",
    }, indent=2)


def cmd_template(args: argparse.Namespace) -> int:
    if args.list:
        if args.format == "json":
            print(json.dumps({
                "templates": list(TEMPLATES.keys()),
                "count": len(TEMPLATES),
            }, indent=2))
        else:
            print(f"Available templates ({len(TEMPLATES)}):\n")
            for slug, data in sorted(TEMPLATES.items()):
                print(f"  {slug:<30} {data['name']}")
        return 0

    if not args.keyword:
        print("Error: keyword is required when not using --list", file=sys.stderr)
        return 1

    result = _find_template(args.keyword)
    if result is None:
        if args.format == "json":
            print(json.dumps({"error": f"No template matching '{args.keyword}'"}))
        else:
            print(f"No template matching '{args.keyword}'. Use --list to see all.", file=sys.stderr)
        return 1

    slug, data = result
    if args.format == "json":
        print(json.dumps({
            "template": slug,
            "name": data["name"],
            "keywords": data["keywords"],
            "zones": data["zones"],
            "default_top": data.get("default_top", ""),
            "default_bottom": data.get("default_bottom", ""),
        }, indent=2))
    else:
        print(f"\n  Template: {data['name']} ({slug})")
        print(f"  Keywords: {', '.join(data['keywords'])}")
        print(f"  Zones: {json.dumps(data['zones'])}")
        print(f"  Default top:    {data.get('default_top', '')}")
        print(f"  Default bottom: {data.get('default_bottom', '')}")
        print(data["ascii"])
    return 0


def cmd_caption(args: argparse.Namespace) -> int:
    result = _find_template(args.template)
    if result is None:
        if args.format == "json":
            print(json.dumps({"error": f"No template matching '{args.template}'"}))
        else:
            print(f"No template matching '{args.template}'", file=sys.stderr)
        return 1

    slug, data = result
    top = args.top_text
    bottom = args.bottom_text

    if args.format == "json":
        print(_as_json(slug, data, top, bottom))
    else:
        print(_as_text(slug, data, top, bottom))
    return 0


def cmd_random(args: argparse.Namespace) -> int:
    slug = random.choice(list(TEMPLATES.keys()))
    data = TEMPLATES[slug]
    top = data.get("default_top", "TOP TEXT")
    bottom = data.get("default_bottom", "BOTTOM TEXT")

    if args.format == "json":
        print(json.dumps({
            "template": slug,
            "name": data["name"],
            "top_text": top,
            "bottom_text": bottom,
            "format": "meme",
        }, indent=2))
    else:
        print(_as_text(slug, data, top, bottom))
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
