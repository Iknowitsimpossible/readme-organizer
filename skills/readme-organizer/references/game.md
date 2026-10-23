# Template: Game

A visitor wants to know: what does it look like, how do I launch it, and how do I play?

## Skeleton

For a deployed browser game, lead with play and controls. For a desktop game, put the verified launch instructions before controls. Use only existing assets and verified links.

````markdown
# Game Name

One sentence: the genre and the hook.

[Play the game](verified-play-url)

![Describe the actual gameplay image](existing-image-path)

## How to play

The goal and win/lose conditions in 2–4 sentences.

| Input | Action |
|---|---|
| Verified key or gesture | Action from the input code |

## Run locally

Verified runtime requirements, followed by one complete command block:

```bash
# Clone, enter the project, install dependencies, and launch.
# Replace these comments with commands verified against the repository.
```

## Credits

Sources for third-party assets, when recorded in the repository.
````

## Type-specific notes

- **Visuals matter most.** A representative GIF or screenshot near the top helps visitors understand the game. Prioritize broken launch instructions before visual polish. If none exists, leave a TODO and tell the user how to make one (macOS: Cmd+Shift+5 to record the screen).
- **Controls:** extract them from the key-handling code (`pygame.K_*`, `onKeyPress`, `Input.GetKey`, etc.). Don't guess.
- **Deployed browser games** (Phaser, three.js, plain JS canvas on GitHub Pages, itch.io, etc.): the play link is the main Usage. Put it right under the opening sentence. Local setup becomes a short secondary section, e.g. "Run it yourself", for people who want to read or change the code. Find the URL in the Pages workflow, the repo homepage, a CNAME file, or the existing README.
- **Touch and keyboard:** if the game supports both, use a table with one column per input method, not two separate lists.
- **Credits:** list third-party assets found in `assets/` with their sources or licenses if the repo records them. If you can't find a source, flag it to the user, since unlicensed assets matter when publishing.
