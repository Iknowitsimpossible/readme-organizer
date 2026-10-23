"""Tests for skills/readme-organizer/scripts/check_readme.py.

Each test builds a tiny git repo in a temp folder, writes a README, runs the
checker as a subprocess, and checks its exit code and output.

Run from the repo root:
    python3 -m unittest discover tests
"""
import json
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

CHECKER = Path(__file__).resolve().parent.parent / "skills" / "readme-organizer" / "scripts" / "check_readme.py"
ORIGIN = "https://github.com/example/demo.git"


class CheckerTestCase(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self._tmp.name)
        self.git("init", "-q")
        self.git("remote", "add", "origin", ORIGIN)

    def tearDown(self):
        self._tmp.cleanup()

    def git(self, *args):
        subprocess.run(["git", "-C", str(self.repo), *args], check=True, capture_output=True)

    def add_file(self, path, content=""):
        """Write a file and track it with git."""
        file = self.repo / path
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text(content)
        self.git("add", path)

    def add_package_json(self, scripts):
        self.add_file("package.json", json.dumps({"name": "demo", "scripts": scripts}))

    def write_readme(self, text, path="README.md"):
        file = self.repo / path
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text(textwrap.dedent(text))

    def run_checker(self, *extra_args):
        result = subprocess.run(
            [sys.executable, str(CHECKER), str(self.repo), *extra_args],
            capture_output=True, text=True,
        )
        return result.returncode, result.stdout


class TestPackageScripts(CheckerTestCase):
    def test_existing_scripts_pass(self):
        self.add_package_json({"dev": "vite", "test": "vitest run", "start": "node ."})
        self.write_readme("""
            ```bash
            npm install
            npm run dev
            npm test
            npm start
            ```
        """)
        code, out = self.run_checker()
        self.assertEqual(code, 0, out)

    def test_missing_npm_script_is_an_error(self):
        self.add_package_json({"dev": "vite"})
        self.write_readme("""
            ```bash
            npm start
            ```
        """)
        code, out = self.run_checker()
        self.assertEqual(code, 1)
        self.assertIn('no "start" script', out)

    def test_missing_yarn_and_pnpm_scripts_are_errors(self):
        self.add_package_json({"dev": "vite"})
        self.write_readme("""
            ```bash
            yarn build
            pnpm run lint
            ```
        """)
        code, out = self.run_checker()
        self.assertEqual(code, 1)
        self.assertIn('no "build" script', out)
        self.assertIn('no "lint" script', out)

    def test_npm_run_without_package_json_is_an_error(self):
        self.write_readme("""
            ```bash
            npm run dev
            ```
        """)
        code, out = self.run_checker()
        self.assertEqual(code, 1)
        self.assertIn("no package.json", out)

    def test_leading_dollar_prompt_is_ignored(self):
        self.add_package_json({"dev": "vite"})
        self.write_readme("""
            ```bash
            $ npm run dev
            ```
        """)
        code, out = self.run_checker()
        self.assertEqual(code, 0, out)


class TestMakeAndEntryFiles(CheckerTestCase):
    def test_make_target_found(self):
        self.add_file("Makefile", "build:\n\techo hi\n")
        self.write_readme("""
            ```bash
            make build
            ```
        """)
        code, out = self.run_checker()
        self.assertEqual(code, 0, out)

    def test_missing_make_target_is_an_error(self):
        self.add_file("Makefile", "build:\n\techo hi\n")
        self.write_readme("""
            ```bash
            make deploy
            ```
        """)
        code, out = self.run_checker()
        self.assertEqual(code, 1)
        self.assertIn('no "deploy" target', out)

    def test_tracked_python_file_passes_and_untracked_fails(self):
        self.add_file("main.py", "print('hi')\n")
        self.write_readme("""
            ```bash
            python main.py
            python3 other.py
            ```
        """)
        code, out = self.run_checker()
        self.assertEqual(code, 1)
        self.assertNotIn("main.py is not", out)
        self.assertIn("other.py is not a tracked file", out)


class TestLinks(CheckerTestCase):
    def test_tracked_file_and_folder_links_pass(self):
        self.add_file("LICENSE", "MIT")
        self.add_file("docs/guide.md", "# Guide")
        self.write_readme("""
            See [LICENSE](LICENSE), [the docs](docs/) and [the guide](docs/guide.md#setup).
        """)
        code, out = self.run_checker()
        self.assertEqual(code, 0, out)

    def test_missing_image_is_an_error(self):
        self.write_readme("""
            ![Gameplay](docs/gameplay.gif)
            <img src="docs/logo.png" alt="logo">
        """)
        code, out = self.run_checker()
        self.assertEqual(code, 1)
        self.assertIn("docs/gameplay.gif", out)
        self.assertIn("docs/logo.png", out)

    def test_untracked_file_on_disk_is_still_an_error(self):
        (self.repo / "notes.md").write_text("not committed")
        self.write_readme("[notes](notes.md)\n")
        code, out = self.run_checker()
        self.assertEqual(code, 1)
        self.assertIn("notes.md", out)

    def test_external_links_and_anchors_are_skipped(self):
        self.write_readme("""
            [site](https://example.com) [mail](mailto:a@b.c) [top](#readme)
        """)
        code, out = self.run_checker()
        self.assertEqual(code, 0, out)

    def test_links_resolve_relative_to_a_readme_in_a_subfolder(self):
        self.add_file("LICENSE", "MIT")
        self.write_readme("[license](../LICENSE)\n", path="docs/README.md")
        code, out = self.run_checker("docs/README.md")
        self.assertEqual(code, 0, out)

    def test_links_inside_code_blocks_are_not_checked(self):
        # Suggestion files show proposed Markdown inside fences; images there may not exist yet.
        self.write_readme("""
            ```markdown
            ![Gameplay](docs/gameplay.gif)
            ```
        """)
        code, out = self.run_checker()
        self.assertEqual(code, 0, out)


class TestCloneUrl(CheckerTestCase):
    def test_matching_clone_url_passes_in_https_and_ssh_forms(self):
        self.write_readme("""
            ```bash
            git clone https://github.com/example/demo
            git clone git@github.com:example/demo.git
            ```
        """)
        code, out = self.run_checker()
        self.assertEqual(code, 0, out)

    def test_wrong_clone_url_is_an_error(self):
        self.write_readme("""
            ```bash
            git clone https://github.com/someone/else.git
            ```
        """)
        code, out = self.run_checker()
        self.assertEqual(code, 1)
        self.assertIn("does not match origin", out)


class TestReportingAndErrors(CheckerTestCase):
    def test_todo_markers_are_listed_but_not_errors(self):
        self.write_readme("""
            # Demo
            <!-- TODO: add screenshot -->
            TODO: write usage
            Leave a `TODO` marker when unsure.
        """)
        code, out = self.run_checker()
        self.assertEqual(code, 0, out)
        self.assertIn("2 TODO line(s)", out)

    def test_check_off_section_is_skipped(self):
        self.write_readme("""
            <!-- check-readme: off -->
            ```bash
            npm run dev
            git clone https://github.com/someone/else.git
            ```
            ![quoted](docs/missing.png)
            <!-- check-readme: on -->
            ```bash
            npm start
            ```
        """)
        code, out = self.run_checker()
        self.assertEqual(code, 1)
        self.assertIn("npm start", out)
        self.assertNotIn("npm run dev", out)
        self.assertNotIn("someone/else", out)
        self.assertNotIn("missing.png", out)

    def test_paths_outside_the_repo_are_skipped(self):
        self.write_readme("""
            ```bash
            python3 ~/tools/check.py .
            node /usr/local/lib/cli.js
            ```
        """)
        code, out = self.run_checker()
        self.assertEqual(code, 0, out)

    def test_commands_in_prose_are_not_checked(self):
        self.write_readme("Run `npm start` once the server is ready.\n")
        code, out = self.run_checker()
        self.assertEqual(code, 0, out)

    def test_missing_readme_fails(self):
        code, out = self.run_checker()
        self.assertEqual(code, 1)
        self.assertIn("does not exist", out)

    def test_not_a_git_repo_fails(self):
        with tempfile.TemporaryDirectory() as plain:
            Path(plain, "README.md").write_text("# Hi\n")
            result = subprocess.run([sys.executable, str(CHECKER), plain], capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn("not a git repository", result.stdout)


if __name__ == "__main__":
    unittest.main()
