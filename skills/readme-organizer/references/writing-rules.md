# Writing rules

These apply to every project type. Templates add type-specific rules on top.

## Accuracy

- Every command, flag, URL, version, and feature must trace to a fact gathered in Step 2. If something can't be confirmed, write `<!-- TODO: ... -->`.
- State minimum requirements only when the repo specifies them (`engines`, `requires-python`, `rust-version`, `.nvmrc`). Otherwise report a configured CI/runtime version as such; say “Tested with” only when a successful run provides evidence.
- Translate version ranges into plain language: `^22.12.0 || ^24.0.0 || >=26.0.0` becomes "Node.js 22.x (22.12+), 24.x, or 26+". Preserve excluded major versions and upper bounds; never flatten a disjoint range into a single minimum.
- Show real output only if you actually ran the command. Otherwise describe it.

## Structure

- Cover purpose, first successful use, and setup. Order around the primary reader: a browser game leads with Play and Controls; a library leads with installation and a minimal useful example. Templates are starting points, not mandatory headings.
- The title is the project's name. Directly under it, add one sentence saying what it is and who it's for.
- If the project is deployed or published, put the link (live demo, package page) right under that sentence. For many visitors that is the main way to use it.
- Badges only when they report something real: an existing CI workflow, a published package version, a license file.
- Optional sections, only with real content: *Configuration*, *Project structure*, *Development* / *Contributing*, *Acknowledgments*, *License*.
- Keep build-from-source and contributor setup out of *Installation*. Put them under *Development*.
- Headings may fit the project ("Run it yourself", "Controls", "How to play") as long as readers can find purpose, usage, and setup easily.

## Style

- Be concise. Cut any sentence that doesn't help a reader decide, install, or use.
- Write for a newcomer: spell out `git clone` and `cd`, and link to where runtimes can be installed (e.g. nodejs.org).
- Put every command in a fenced code block with a language tag (`bash`, `python`, `js`, ...). Use one command per line, without a leading `$`.
- Lead with outcomes, not implementation. "Take penalties with a swipe, then dive to save theirs" beats "Uses three.js and a physics module".
- No emojis.
- Use relative links for repo files (`[LICENSE](LICENSE)`) and absolute links for everything else.
- Visual projects (web apps, games, UIs) need a screenshot or GIF. Use a tracked image if one exists. Otherwise add `<!-- TODO: add screenshot at docs/screenshot.png -->` and tell the user how to make one (macOS: Cmd+Shift+5). Never link an image that doesn't exist.

## Visual composition

- Build a compact opening: title, one-sentence purpose, primary action link, and one useful visual for a visual project. Keep secondary links subordinate.
- Omit “What it does” when it repeats the opening. Add features only when they help readers choose or understand the project; do not fill a three-bullet quota.
- Use consistent heading depth and blank lines. Keep setup commands together so readers can reach a first success without jumping between sections.
- Use tables for mappings such as controls or configuration, not paragraphs or long commands. Avoid decorative separators and badge collections.
- Preserve an existing visual identity. For a small project, prefer a short, composed page; link to deeper documentation when needed.
- Inspect the rendered Markdown when a preview is available: check the opening hierarchy, image placement, table readability, and code fences. If only source was inspected, say so.
