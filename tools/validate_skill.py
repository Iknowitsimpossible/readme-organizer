#!/usr/bin/env python3
"""Validate every skill under skills/ against the Agent Skills rules.

Usage:
    python3 tools/validate_skill.py [skills-dir]

Checks each skills/<name>/ folder for the mistakes Anthropic's skill guide
warns about:
  - SKILL.md exists with exactly that spelling
  - frontmatter is wrapped in --- delimiters
  - name is kebab-case, matches the folder, and avoids reserved words
  - description exists and is at most 1024 characters
  - no XML angle brackets anywhere in the frontmatter
  - no README.md inside the skill folder
  - every references/ or scripts/ path mentioned in SKILL.md exists
  - SKILL.md stays under 5,000 words

Exit code: 0 if every skill passes, 1 otherwise. Standard library only.
"""
import re
import sys
from pathlib import Path

KEBAB_CASE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
RESERVED_WORDS = ("claude", "anthropic")
MAX_DESCRIPTION = 1024
MAX_WORDS = 5000
BUNDLED_PATH = re.compile(r"\b((?:references|scripts|assets)/[\w./-]+\.\w+)")


def parse_frontmatter(text):
    """Return (frontmatter_text, fields) or (None, {}) if delimiters are missing.

    Only top-level `key: value` pairs are read, which is all these checks need.
    """
    if not text.startswith("---\n"):
        return None, {}
    end = text.find("\n---", 4)
    if end == -1:
        return None, {}
    block = text[4:end]
    fields = {}
    for line in block.splitlines():
        match = re.match(r"^([A-Za-z_-]+):\s*(.*)$", line)
        if match:
            fields[match.group(1)] = match.group(2).strip().strip("\"'")
    return block, fields


def validate(skill_dir):
    errors = []
    skill_file = skill_dir / "SKILL.md"
    names = [p.name for p in skill_dir.iterdir()]
    if "SKILL.md" not in names:
        wrong = [n for n in names if n.lower() == "skill.md"]
        hint = f" (found {wrong[0]}; the name is case-sensitive)" if wrong else ""
        return [f"missing SKILL.md{hint}"]

    text = skill_file.read_text()
    block, fields = parse_frontmatter(text)
    if block is None:
        return ["frontmatter must start and end with --- lines"]

    name = fields.get("name", "")
    if not name:
        errors.append("frontmatter has no name")
    else:
        if not KEBAB_CASE.match(name):
            errors.append(f"name '{name}' must be kebab-case (lowercase, digits, hyphens)")
        if name != skill_dir.name:
            errors.append(f"name '{name}' does not match folder '{skill_dir.name}'")
        if any(word in name for word in RESERVED_WORDS):
            errors.append(f"name '{name}' uses a reserved word ({', '.join(RESERVED_WORDS)})")

    description = fields.get("description", "")
    if not description:
        errors.append("frontmatter has no description")
    elif len(description) > MAX_DESCRIPTION:
        errors.append(f"description is {len(description)} characters (max {MAX_DESCRIPTION})")

    if "<" in block or ">" in block:
        errors.append("frontmatter contains < or >, which are not allowed")

    if (skill_dir / "README.md").exists():
        errors.append("README.md belongs at the repo root, not inside the skill folder")

    for path in sorted(set(BUNDLED_PATH.findall(text))):
        if not (skill_dir / path).exists():
            errors.append(f"SKILL.md mentions {path}, which does not exist")

    words = len(text.split())
    if words > MAX_WORDS:
        errors.append(f"SKILL.md is {words} words (keep it under {MAX_WORDS}; move detail to references/)")

    return errors


def main():
    skills_root = Path(sys.argv[1] if len(sys.argv) > 1 else "skills")
    skill_dirs = sorted(p for p in skills_root.iterdir() if p.is_dir()) if skills_root.is_dir() else []
    if not skill_dirs:
        print(f"ERROR: no skill folders found in {skills_root}")
        return 1

    failed = 0
    for skill_dir in skill_dirs:
        errors = validate(skill_dir)
        if errors:
            failed += 1
            for error in errors:
                print(f"ERROR {skill_dir.name}: {error}")
        else:
            print(f"OK    {skill_dir.name}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
