# readme-organizer

[![CI](https://github.com/Iknowitsimpossible/readme-organizer/actions/workflows/ci.yml/badge.svg)](https://github.com/Iknowitsimpossible/readme-organizer/actions/workflows/ci.yml)

An agent skill that turns a finished project into one a stranger can understand, install, and run, by writing its README or reviewing the one you have. It works with any coding agent that supports [Agent Skills](https://agentskills.io), including Claude Code and Codex.

## What it does

Point it at a finished repo and it will:

- **Identify the project type** (web app, library, CLI tool, game, data/ML, or coursework) and use a README template made for that type. A game gets controls and a play link; a library gets an import example.
- **Cover the three things readers need:** what the project does, how to install it, and how to use it.
- **Check every command against your code.** A bundled checker flags `npm run` scripts that don't exist, links to missing files, and clone URLs that point to the wrong repo. Anything it can't confirm is left as a `TODO` instead of being guessed.
- **Suggest, never overwrite.** If you already have a README, it writes `README-SUGGESTIONS.md` with ranked, ready-to-paste fixes, notes what to keep, and applies only the changes you approve.

## Installation

**Requirements:** git, and a coding agent that can run shell commands in your local repo. Python 3 is optional, for the checker. Chat-only apps such as the Claude or ChatGPT web apps can't use it, because they can't see your repo.

1. Clone this repo somewhere permanent:

   ```bash
   git clone https://github.com/Iknowitsimpossible/readme-organizer.git ~/code/readme-organizer
   ```

2. Link the skill into your agent's skills folder. A link instead of a copy means `git pull` updates the skill. For Claude Code:

   ```bash
   mkdir -p ~/.claude/skills
   ln -s ~/code/readme-organizer/skills/readme-organizer ~/.claude/skills/readme-organizer
   ```

   For another agent, use the same two commands with its folder:

   | Agent | All projects | One project | Call it by name |
   |---|---|---|---|
   | Claude Code | `~/.claude/skills/` | `.claude/skills/` | `/readme-organizer` |
   | Codex (restart after installing) | `~/.agents/skills/` | `.agents/skills/` | `$readme-organizer` |
   | Other Agent Skills agents | see your agent's docs | | |

Agents without skills support (for example Cursor or Copilot) can still follow it. Ask: *"Follow the instructions in ~/code/readme-organizer/skills/readme-organizer/SKILL.md to review my README."*

## Usage

Commit and push your project first. The skill checks this before it starts. Then, inside the project, ask your agent:

```text
Review my README
```

or *"Write a README for this project"*. The skill then:

1. Checks that the project is committed and pushed.
2. Reads manifests, entry points, scripts, and deploy configs.
3. Tells you the project type it detected and why.
4. Writes `README.md`, or `README-SUGGESTIONS.md` if a README already exists.
5. Runs the checker, fixes anything it flags, and lists the `TODO` markers left for you (screenshots, deploy URLs, and so on).

### Run the checker by itself

The checker works without an agent, on any README:

```bash
python3 ~/code/readme-organizer/skills/readme-organizer/scripts/check_readme.py path/to/project
```

### Example output

<!-- check-readme: off -->
From a real run on [penalty-night](https://github.com/Iknowitsimpossible/penalty-night), a browser game. The skill noticed that `package.json` requires Node 22.12+ and that newcomers wouldn't know to clone first:

````diff
 ## Run it yourself

+Requires [Node.js](https://nodejs.org) 22.12 or newer.
+
 ```bash
+git clone https://github.com/Iknowitsimpossible/penalty-night.git
+cd penalty-night
 npm install
 npm run dev
 ```
````
<!-- check-readme: on -->

It also flagged the missing gameplay GIF and license, and said to keep the controls table and the deliberately short length. Full output: [examples/penalty-night-suggestions.md](examples/penalty-night-suggestions.md).

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

## Acknowledgments

The writing guidance draws on [banesullivan/README](https://github.com/banesullivan/README). The skill's structure follows Anthropic's [guide to building skills](https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf).

## License

[MIT](LICENSE)
