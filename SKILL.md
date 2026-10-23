---
name: readme-organizer
description: Write or review the README of a finished project. Reads the repo, identifies what kind of project it is (web app, library, CLI tool, game, coursework, data/ML), and produces a README with three core sections — what it does, how to install it, how to use it. If a README already exists, it suggests changes instead of overwriting. Use when the user asks to write, organize, refresh, or review a README for a project that is done or nearly done. Do not use for projects still in early development.
---

# README Organizer

Produce a README that answers, in order: **What does this project do? How do I install it? How do I use it?**

The README is often the only thing a visitor reads. It should let them decide in under a minute whether the project is useful to them and get it running in a few more.

## Workflow

Work through these phases in order. Do not start writing until phases 1–3 are done.

### Phase 1 — Check the project is ready

This skill is meant for finished projects. Before anything else, run:

```bash
git status --short
git log --oneline -5
git status -sb | head -1        # shows "ahead N" if commits are unpushed
```

- **Uncommitted changes or unpushed commits:** tell the user and ask whether to continue. The README should describe what is actually pushed.
- **Not a git repo, or only a handful of commits with obvious TODOs/stubs in the code:** say the project looks unfinished and ask before continuing.
- Otherwise, continue without asking.

### Phase 2 — Gather facts

Read only what you need. Start with `git ls-files` to see what is tracked (this skips build output and dependencies), then read:

1. **Manifests:** `package.json`, `pyproject.toml`, `setup.py`, `requirements.txt`, `Cargo.toml`, `go.mod`, `pom.xml`, `build.gradle`, `CMakeLists.txt`, `Makefile`, `Dockerfile`, `environment.yml`.
2. **Entry points:** `main.*`, `app.*`, `index.*`, `src/`, `bin/`, the `"bin"` / `"main"` / `[project.scripts]` fields in manifests.
3. **Runnable commands:** `scripts` in `package.json`, Makefile targets, `[project.scripts]`, CI workflow steps in `.github/workflows/`.
4. **Config the user must supply:** `.env.example`, `config.example.*`, any code reading `process.env` / `os.environ`.
5. **Context:** the existing `README*`, `LICENSE`, `git remote get-url origin`, deployment configs (`vercel.json`, `netlify.toml`, GitHub Pages), screenshots or `assets/` images.

Keep a running list of **facts with their sources** (for example "dev server: `npm run dev` — package.json scripts.dev"). Every command in the final README must come from this list.

### Phase 3 — Classify the project

Choose **one** primary type using the signals below, then read the matching template in `references/`. Read only that one template.

| Type | Strong signals | Template |
|---|---|---|
| Web app / website | React/Vue/Svelte/Next/Vite/Flask/Django/Express in deps; `index.html`; deploy config | `references/web-app.md` |
| Library / package | Published-package metadata (`name` + `version` + `exports`/`main`, or `[project]` with no app entry point); code meant to be imported | `references/library.md` |
| CLI tool | `"bin"` field, `[project.scripts]`, `argparse`/`click`/`commander`/`clap`, a `main` that reads `argv` | `references/cli-tool.md` |
| Game | pygame/Unity/Godot/Phaser/cmu_graphics, a game loop, sprite or level assets | `references/game.md` |
| Data / ML | Mostly `.ipynb`, `data/` folder, pandas/sklearn/torch, model weights, results plots | `references/data-ml.md` |
| Coursework | Course codes or `hw`/`lab`/`project` in names (e.g. `hw7_andrewid`), handout PDFs, autograder files, starter code | `references/coursework.md` |

If two types fit (a game that is also coursework, a web app with a CLI), pick the one that describes **how a visitor uses it** and borrow sections from the other. If nothing fits, use the closest template and say so. If you really cannot tell, ask the user one short question.

Tell the user the type you chose and the main reason in one line, e.g. *"Classified as a web app: Vite + React with a Vercel deploy config."*

### Phase 4 — Write or suggest

**No README exists (or it is empty or default boilerplate):** write `README.md` following the template and the rules below. Show the user the result and list any `TODO` markers you left.

**A README already exists:** do **not** overwrite it. Write `README-SUGGESTIONS.md` in the repo root containing:

1. **Verdict:** one or two sentences on the README's overall state.
2. **Issues**, most important first. Each issue has:
   - what is wrong or missing (e.g. "Install says `npm start`, but package.json has no `start` script"),
   - why it matters to a reader,
   - the exact replacement text, ready to paste.
3. **Keep:** what is already good and should stay.

Then summarize the top three suggestions in chat and ask whether to apply them. Apply only what the user approves, editing the existing README in place and keeping the author's own voice and custom sections.

`README-SUGGESTIONS.md` is a working file. Remind the user to delete it, or not commit it, once they are done.

## Writing rules

These apply to every template.

**Accuracy**
- Never invent a command, flag, URL, version number, or feature. Each must trace back to a fact from Phase 2.
- If something is needed but cannot be confirmed (a deploy URL, a required API key's name), write `<!-- TODO: ... -->` and tell the user.
- State minimum requirements (language/runtime version, OS limits) only when the repo specifies them (`engines`, `requires-python`, `rust-version`, CI matrix). Otherwise write what the project was built with, e.g. "Tested with Python 3.12".

**Structure**
- Core order: title → one-line description → **What it does** → **Installation** → **Usage**. Optional sections come after Usage.
- The title is the project's name. Directly under it, add one sentence saying what the project is and who it is for.
- Add badges only when they report something real (a CI workflow that exists, a published package version, a license file). No decorative badges.
- Optional sections, only when there is real content: *Configuration*, *Project structure*, *Development* / *Contributing*, *Acknowledgments*, *License*.
- Keep build-from-source and contributor setup out of *Installation*. Put them under *Development*, so ordinary users are not slowed down.

**Style**
- Be concise. If a sentence does not help a reader decide, install, or use, cut it.
- Write for a newcomer: spell out steps such as `git clone` and `cd` instead of assuming them.
- Put every command or code snippet in a fenced code block with a language tag (`bash`, `python`, `js`, …).
- No emojis in headings or body text.
- Use relative links for files in the repo (`[LICENSE](LICENSE)`), absolute links for everything else.
- For visual projects (web apps, games, UIs), include a screenshot or GIF. Use an existing image if the repo has one. Otherwise add `<!-- TODO: add screenshot at docs/screenshot.png -->`. Never link an image that doesn't exist.

## Final check

Before showing the result, re-read it and confirm that:

- [ ] each command appears in a manifest, script, Makefile, or source file you read;
- [ ] each file or image link points to a tracked file (`git ls-files`);
- [ ] the three core sections are present and in order;
- [ ] a stranger could go from `git clone` to a working project using only the README;
- [ ] all `TODO` markers are listed for the user.
