# readme-organizer

A Claude Code skill that turns a finished project into one a stranger can understand, install, and run, by writing its README or reviewing the one you have.

## What it does

Point it at a finished repo and it will:

- **Identify the project type** (web app, library, CLI tool, game, data/ML, or coursework) and use a README template made for that type. A game gets controls and a play link; a library gets an import example.
- **Cover the three things readers need:** what the project does, how to install it, and how to use it.
- **Check every command against your code.** A bundled checker flags `npm run` scripts that don't exist, links to missing files, and clone URLs that point to the wrong repo. Anything it can't confirm is left as a `TODO` instead of being guessed.
- **Suggest, never overwrite.** If you already have a README, it writes `README-SUGGESTIONS.md` with ranked, ready-to-paste fixes, notes what to keep, and applies only the changes you approve.

The writing guidance draws on [banesullivan/README](https://github.com/banesullivan/README). The skill's structure follows Anthropic's [guide to building skills](https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf).

## Installation

Requires [Claude Code](https://claude.com/claude-code), git, and Python 3.

Clone the repo, then link the skill folder into your personal skills directory:

```bash
git clone https://github.com/Iknowitsimpossible/readme-organizer.git
mkdir -p ~/.claude/skills
ln -s "$PWD/readme-organizer/skills/readme-organizer" ~/.claude/skills/readme-organizer
```

Using a link instead of a copy means `git pull` updates the skill. To install it for a single project only, copy `skills/readme-organizer` into that project's `.claude/skills/` folder.

## Usage

Commit and push your project first. The skill checks for this before it starts. Then, inside the project in Claude Code, run:

```text
/readme-organizer
```

Or just ask: *"Write a README for this project"* or *"Review my README"*.

What happens:

1. Checks that the project is committed and pushed.
2. Reads manifests, entry points, scripts, and deploy configs.
3. Tells you the project type it detected and why.
4. Writes `README.md`, or `README-SUGGESTIONS.md` if a README already exists.
5. Runs the checker, fixes anything it flags, and lists the `TODO` markers left for you (screenshots, deploy URLs, and so on).

You can also run the checker on any README yourself:

```bash
python3 skills/readme-organizer/scripts/check_readme.py path/to/project
```

## Repository layout

```text
skills/readme-organizer/        # the skill itself (this folder is what you install)
├── SKILL.md                    # workflow, examples, troubleshooting
├── references/
│   ├── writing-rules.md        # rules shared by every project type
│   └── web-app.md, library.md, cli-tool.md, game.md, data-ml.md, coursework.md
└── scripts/
    └── check_readme.py         # verifies commands and links against the repo
tests/test-cases.md             # triggering, functional, and checker test cases
```

Only the template for the detected project type is loaded, which keeps the skill's context small.

## License

[MIT](LICENSE)
