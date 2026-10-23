# readme-organizer

A Claude Code skill that writes or reviews the README of a finished project, adapting the structure to the kind of project it is.

## What it does

Point it at a finished repo and it will:

- **Identify the project type** (web app, library, CLI tool, game, data/ML, or coursework) from manifests, entry points, and file layout.
- **Write a README with three core sections** (what it does, how to install it, how to use it), using a template tailored to that type.
- **Only use commands it can verify.** Every install and run command is traced to `package.json` scripts, a Makefile, a manifest, or source code. Anything it can't confirm is left as a `TODO` instead of being guessed.
- **Suggest instead of overwrite.** If a README already exists, it writes `README-SUGGESTIONS.md` with ranked issues and ready-to-paste fixes, and applies only the ones you approve.

The writing guidance draws on [banesullivan/README](https://github.com/banesullivan/README).

## Installation

Requires [Claude Code](https://claude.com/claude-code).

Install it as a personal skill, available in every project:

```bash
git clone https://github.com/Iknowitsimpossible/readme-organizer.git ~/.claude/skills/readme-organizer
```

Or install it for a single project:

```bash
git clone https://github.com/Iknowitsimpossible/readme-organizer.git .claude/skills/readme-organizer
```

## Usage

Commit and push your project first. The skill checks for this and warns you about uncommitted or unpushed work. Then, inside the project in Claude Code, run:

```text
/readme-organizer
```

Or just ask: *"Write a README for this project"* or *"Review my README"*.

What happens:

1. Checks the repo is committed and pushed.
2. Reads manifests, entry points, scripts, and config examples.
3. Tells you the project type it detected and why.
4. Writes `README.md`, or `README-SUGGESTIONS.md` if a README already exists.
5. Lists any `TODO` markers you need to fill in (deploy URL, screenshots, and so on).

## How it's organized

```text
readme-organizer/
├── SKILL.md              # workflow, classification rules, writing rules
└── references/           # one template per project type, loaded on demand
    ├── web-app.md
    ├── library.md
    ├── cli-tool.md
    ├── game.md
    ├── data-ml.md
    └── coursework.md
```

Only the template for the detected type is loaded, which keeps the skill's context small.

## License

[MIT](LICENSE)
