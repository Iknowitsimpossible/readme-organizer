# README suggestions for penalty-night

Real output from running readme-organizer on [penalty-night](https://github.com/Iknowitsimpossible/penalty-night), saved here as an example. (In a real project this is a working file you delete after applying the suggestions.)

**Classified as:** game (browser game: three.js + Vite, deployed to GitHub Pages).

## Verdict

A strong README already: a clear one-line hook, the play link at the top, and a controls table that matches the code. The main gaps are no visual, and local setup that skips the steps a newcomer needs (cloning, Node version).

## Issues (most important first)

### 1. No screenshot or GIF

**What:** No image is tracked in the repo, and the README has none.
**Why it matters:** For a game, a visual is what makes a visitor click "Play it here". It is the single biggest improvement available.
**Fix:** Record a short clip of a penalty (macOS: Cmd+Shift+5 → record selected portion), convert it to a GIF or take a screenshot, save it as `docs/gameplay.gif`, then add this right under the opening paragraph:

```markdown
![A penalty being taken under the floodlights](docs/gameplay.gif)
```

### 2. Local setup skips cloning and the Node requirement

**What:** "Run it yourself" starts at `npm install`. It doesn't say to clone the repo, and doesn't mention that `package.json` requires Node `^22.12.0 || ^24.0.0 || >=26.0.0` (`engines`).
**Why it matters:** Someone with Node 18 or 20 installed hits a confusing error. A newcomer may not know they need to clone first.
**Fix:** Replace the "Run it yourself" section with:

````markdown
## Run it yourself

Requires [Node.js](https://nodejs.org) 22.12 or newer.

```bash
git clone https://github.com/Iknowitsimpossible/penalty-night.git
cd penalty-night
npm install
npm run dev
```

Then open the address it prints. `npm test` runs the unit tests.
````

### 3. No license

**What:** The repo is public, but it has no `LICENSE` file.
**Why it matters:** Without a license, the code is "all rights reserved" by default: people can look at it but have no right to reuse it. That's fine if it's what you want, but it should be a deliberate choice.
**Fix:** Either add a `LICENSE` (MIT is the usual choice for a portfolio project) and end the README with:

```markdown
## License

[MIT](LICENSE)
```

or leave it out on purpose.

### 4. (Optional) Deploy status badge

**What:** `.github/workflows/pages.yml` builds, tests, and deploys on every push to `main`, but nothing shows that.
**Why it matters:** A green badge tells visitors the live game is current and the tests pass. Low priority.
**Fix:** Add under the title:

```markdown
[![Deploy](https://github.com/Iknowitsimpossible/penalty-night/actions/workflows/pages.yml/badge.svg)](https://github.com/Iknowitsimpossible/penalty-night/actions/workflows/pages.yml)
```

## Keep

- **The opening paragraph and the "Play it here" link.** They say what the game is and let people play in one click, which matters more than local setup for a browser game.
- **The Controls table.** Checked against `src/input/keyboard.js` and `src/game.js`: arrows, Space, Z / X, A / D, P / Esc all match.
- **The keeper tip** about the gold dive bar and the hint zone (matches the `keeperHints` setting in `src/ui/settings.js`).
- **The short length.** Your last commit trimmed it to the essentials on purpose. These suggestions add about 10 lines.
- **Section names.** "Run it yourself" and "Controls" fit a game better than generic "Installation" / "Usage" headings, and they cover the same ground.
