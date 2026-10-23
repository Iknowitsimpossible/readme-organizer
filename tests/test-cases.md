# Test cases

Run these by hand in a coding agent that supports skills (Claude Code, Codex, ...) after changing the skill. Run the triggering tests in both if you can, since each agent decides from the description on its own. They follow the three test areas in Anthropic's skill-building guide: triggering, functional, and checker.

## 1. Triggering

Start a fresh session inside a finished project and send each prompt. Record whether `readme-organizer` loads.

**Should trigger**

- "Write a README for this project"
- "Review my README"
- "Can you clean up the readme before I put this on my portfolio?"
- "My project is done, make it presentable on GitHub"
- "Document how to install and run this"

**Should NOT trigger**

- "Add docstrings to utils.py"
- "Write a CHANGELOG for v2"
- "Generate API reference docs for this library"
- "Fix the failing test in tests/ball.test.js"
- "Write a README for this skill" (while editing a skill's own repo)

Target: at least 4 of 5 in each list.

## 2. Functional

| Case | Setup | Expected |
|---|---|---|
| Existing README, finished game | `penalty-night` | Classified as **game**; writes `README-SUGGESTIONS.md`; README unchanged; suggestions include a screenshot, clone and Node 22.12 steps, and a license; keeps the controls table and short length; no suggestion to rename "Run it yourself" |
| Untracked tool folder only | Repo with only `.claude/` untracked | Step 1 continues without asking |
| Unpushed commit | Commit something without pushing | Step 1 stops and asks |
| No README | Remove README on a scratch branch | Writes `README.md` with what / install / use in order; every TODO is listed |
| Coursework repo | e.g. `hw7_*` | Warns about academic integrity before writing |
| Same request, 3 runs | Repeat case 1 | Same type and the same top three suggestions each time |

## 3. Checker

```bash
python3 skills/readme-organizer/scripts/check_readme.py ~/code/penalty-night
```

Expected: `0 error(s)`. Then plant errors in a scratch copy of a README (an `npm start` with no start script, a link to `docs/missing.png`, a wrong clone URL) and confirm each one is reported.

## 4. Automated

CI runs these on every push (see `.github/workflows/ci.yml`). To run them locally:

```bash
python3 tools/validate_skill.py
python3 -m unittest discover tests
```
