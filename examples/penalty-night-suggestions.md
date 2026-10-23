# README review · penalty-night

The README already has a clear hook, a play link, and useful controls. Complete the local setup first; a gameplay image would make the opening more inviting once one is available.

This revised report uses the repository facts recorded in the original review. It is a presentation example, not a fresh validation of penalty-night.

## Proposed changes

| ID | Change | Priority | Status |
|---|---|---|---|
| R1 | Complete “Run it yourself” | Important | Ready to apply |
| R2 | Show a gameplay image below the play link | Important | Needs asset |
| R3 | Document the author's licensing choice | Optional | Needs decision |
| R4 | Add a deployment status badge | Optional | Ready to apply |

## Ready to apply

### R1 · Complete local setup

**Location:** Replace “Run it yourself,” from its heading to just before the next heading.

Newcomers need the clone steps and supported Node versions before installing. The original review recorded `engines.node` as `^22.12.0 || ^24.0.0 || >=26.0.0` and confirmed the `dev` and `test` scripts in `package.json`.

**Replacement:**

````markdown
## Run it yourself

Requires [Node.js](https://nodejs.org): 22.x (22.12+), 24.x, or 26+.

```bash
git clone https://github.com/Iknowitsimpossible/penalty-night.git
cd penalty-night
npm install
npm run dev
```

Open the local address printed in the terminal.

To run the unit tests:

```bash
npm test
```
````

### R4 · Add deployment status

**Location:** Insert directly below the project title, before the opening paragraph.

The original review identified `.github/workflows/pages.yml` as the deployment workflow. This badge links to its status; it does not independently prove the live deployment is current.

**Insert:**

```markdown
[![Deploy](https://github.com/Iknowitsimpossible/penalty-night/actions/workflows/pages.yml/badge.svg)](https://github.com/Iknowitsimpossible/penalty-night/actions/workflows/pages.yml)
```

## Needs your input

### R2 · Supply one gameplay image

**Next action:** Capture a representative penalty scene and save it in the repository, for example as `docs/gameplay.png`. A still image is sufficient; animation is optional.

**Placement:** Immediately below the existing play link, before the next section. Keep the opening paragraph and play link together.

Apply this snippet only after that file exists and is tracked:

```markdown
![A penalty being taken under the floodlights](docs/gameplay.png)
```

Adjust the alt text to describe the actual image. This item is not part of the ready-to-apply candidate.

### R3 · Decide whether to add a license

**Next action:** Choose the reuse terms you want, or deliberately leave licensing unchanged. The original review found no `LICENSE` file; this report does not select a license for you.

Once a license is chosen and the file exists, add a short License section linking to it. Until then, there is no ready README edit for this item.

## Keep

- The opening hook and prominent “Play it here” link.
- The controls table and keeper tip, which the original review checked against the game code.
- The short length and project-specific headings, including “Run it yourself.”

## Validation and next step

This example has not been rerun against the current game repository. In a live review, assemble R1 and R4 into a temporary copy of the README, check it relative to the original README location, and report the actual results. R2 and R3 remain pending.

Select changes by ID, for example: “Apply R1.”
