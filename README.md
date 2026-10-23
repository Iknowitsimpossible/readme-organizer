# readme-organizer

[![CI](https://github.com/Iknowitsimpossible/readme-organizer/actions/workflows/ci.yml/badge.svg)](https://github.com/Iknowitsimpossible/readme-organizer/actions/workflows/ci.yml)

An agent skill that turns a finished project into one a stranger can understand, install, and run, by writing its README or reviewing the one you have. It works with any coding agent that supports [Agent Skills](https://agentskills.io), including Claude Code and Codex.

## What it does

Point it at a finished repo and it will:

- **Identify the project type** (web app, library, CLI tool, game, data/ML, or coursework) and use a README template made for that type. A game gets controls and a play link; a library gets an import example.
- **Cover the three things readers need:** what the project does, how to install it, and how to use it.
- **Check every command against your code.** A bundled checker flags `npm run` scripts that don't exist, links to missing files, and clone URLs that point to the wrong repo. Anything it can't confirm is left as a `TODO` instead of being guessed.
- **Suggest, never overwrite.** If you already have a README, it writes `README-SUGGESTIONS.md` with ranked, ready-to-paste fixes, notes what to keep, and applies only the changes you approve.

### Before and after

<!-- check-readme: off -->
From a real run on [penalty-night](https://github.com/Iknowitsimpossible/penalty-night), a browser game. The original setup section:

````markdown
## Run it yourself

```bash
npm install
npm run dev
```
````

The skill noticed that `package.json` requires Node 22.12+ and that a newcomer wouldn't know to clone first. It suggested:

````markdown
## Run it yourself

Requires [Node.js](https://nodejs.org) 22.12 or newer.

```bash
git clone https://github.com/Iknowitsimpossible/penalty-night.git
cd penalty-night
npm install
npm run dev
```
````
<!-- check-readme: on -->

It also flagged the missing gameplay GIF and license, and said to keep the controls table (after checking it against the key-handling code) and the README's deliberately short length. Full output: [examples/penalty-night-suggestions.md](examples/penalty-night-suggestions.md).

## Installation

You need git, a coding agent that can run shell commands in your project, and optionally Python 3 for the checker.

First, clone this repo somewhere permanent:

```bash
git clone https://github.com/Iknowitsimpossible/readme-organizer.git ~/code/readme-organizer
```

Then link the skill folder to where your agent looks for skills. Using a link instead of a copy means `git pull` updates the skill.

**Claude Code**

```bash
mkdir -p ~/.claude/skills
ln -s ~/code/readme-organizer/skills/readme-organizer ~/.claude/skills/readme-organizer
```

**Codex**

```bash
mkdir -p ~/.agents/skills
ln -s ~/code/readme-organizer/skills/readme-organizer ~/.agents/skills/readme-organizer
```

Restart Codex afterward so it picks up the new skill.

**Other agents with Agent Skills support:** link or copy `skills/readme-organizer` into the folder your agent reads skills from.

**Agents without skills support** (for example Cursor or Copilot): they can't load it automatically, but they can follow it. Ask: *"Follow the instructions in ~/code/readme-organizer/skills/readme-organizer/SKILL.md to review my README."*

To install for a single project only, put the folder in that project's `.claude/skills/` (Claude Code) or `.agents/skills/` (Codex).

This skill isn't meant for chat-only apps such as the Claude or ChatGPT web apps. Its first step runs `git status` on your project, so it needs an agent with access to your local repo.

## Usage

Commit and push your project first. The skill checks for this before it starts. Then, inside the project, ask your agent:

```text
Review my README
```

or *"Write a README for this project"*. You can also call it by name: `/readme-organizer` in Claude Code, `$readme-organizer` in Codex.

What happens:

1. Checks that the project is committed and pushed.
2. Reads manifests, entry points, scripts, and deploy configs.
3. Tells you the project type it detected and why.
4. Writes `README.md`, or `README-SUGGESTIONS.md` if a README already exists.
5. Runs the checker, fixes anything it flags, and lists the `TODO` markers left for you (screenshots, deploy URLs, and so on).

You can also run the checker on any README yourself:

```bash
python3 ~/code/readme-organizer/skills/readme-organizer/scripts/check_readme.py path/to/project
```

## Development

Run the same checks as CI from the repo root:

```bash
python3 tools/validate_skill.py
python3 -m unittest discover tests
```

`validate_skill.py` checks the skill's structure and frontmatter (kebab-case name, description length, no angle brackets, no README inside the skill folder, bundled files exist). The unit tests cover the README checker. Manual triggering and functional tests are in [tests/test-cases.md](tests/test-cases.md).

```text
skills/readme-organizer/        # the skill itself (this folder is what you install)
├── SKILL.md                    # workflow, examples, troubleshooting
├── references/                 # writing rules + one template per project type
└── scripts/check_readme.py     # verifies commands and links against the repo
tools/validate_skill.py         # validates skill structure and frontmatter
tests/                          # checker unit tests + manual test cases
examples/                       # real output from test runs
```

The writing guidance draws on [banesullivan/README](https://github.com/banesullivan/README). The skill's structure follows Anthropic's [guide to building skills](https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf).

## License

[MIT](LICENSE)
