# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

Source for the NCSU GIS/MEA582 "Geospatial Modeling and Analysis" course website
(https://ncsu-geoforall-lab.github.io/geospatial-modeling-course). Content is
hand-written HTML fragments that a shell/Python pipeline assembles into a static
site. There is no framework, package manager, or test suite; the build is
`build.sh` plus small Python helper scripts in the repo root.

## Build

```bash
./build.sh              # builds main site into build/
cd lectures && ./build.sh   # builds reveal.js lecture slides into build/lectures/
```

Open `build/index.html` to preview. The build does not reliably detect changes;
delete the stale file in `build/` (or the whole directory) and rebuild if edits
do not show up. Never edit anything in `build/`: every generated file carries a
"This is a generated file" comment.

Publishing is automatic: pushing to `main` triggers the GitHub Actions workflow
(`.github/workflows/gh-pages.yml`), which runs both build scripts and force-pushes
`build/` to the `gh-pages` branch.

## How the build pipeline works

- Source pages are HTML body fragments (no `<html>`/`<head>`). `build.sh` wraps
  each with `head.html` and `foot.html` and pipes it through `edit.py`, which
  rewrites `<em class="module">toolname</em>` into a link to that tool's GRASS
  manual page. Use that markup whenever mentioning a GRASS tool.
- Pages in subdirectories (`grass/`, `arcgis/`, `arcpro/`, `topics/`,
  `resources/`, `project_titles/`) get `head.html`/`foot.html` passed through
  `increase-link-depth.py` so relative links resolve one level down.
- Two index pages are generated, not written: `build/grass/index.html` (order
  taken from links in `assignments.html`) and `build/topics/index.html` (order
  taken from `schedule.html`). `extract-links.py` collects the links,
  `generate-index.py` pulls headings from each target page. Subtopic entries
  come from elements with `class="subtopic"` in topic pages.
- Command examples in assignments live in `<pre><code>` blocks. These are
  machine-readable: `doc2tests.py` converts them into runnable shell scripts.

## Content layout

- `grass/`, `arcgis/`, `arcpro/`: parallel assignment instructions per software.
  The GRASS versions are the primary, actively maintained ones.
- `grass/notebooks/`: Jupyter notebook versions of assignments ("Track 2"),
  with Binder config (`requirements.txt`, `apt.txt`, `postBuild`). Topic pages
  in `topics/` link Track 1 (HTML instructions here) and Track 2 (notebooks in
  the separate GIS582-assignments repo).
- `topics/`: per-topic pages linked from `schedule.html`; these drive the
  topics index.
- `lectures/`: self-contained reveal.js slide deck sources with their own
  `build.sh` and `build-slides.py`.
- `grass/data/`: text files (recode rules, color rules, site coordinates)
  downloaded by students during assignments.

## Maintenance workflows (from README)

- Per-semester updates: everything that must change each term is tagged with
  the string `term-changes` (as an HTML class). Find all of them with
  `grep -IrnE term-changes --exclude=README.md --exclude-dir={build,.git}`.
- GRASS version bumps: manual URLs embed the version as `grassXY`. Use
  `./replace_string.sh grassXY grassXZ` then grep for leftovers, including
  bare `X.Y` version mentions. Note `edit.py` also hardcodes a `grassXY`
  manual URL for module links.
- Testing GRASS assignments: `doc2tests.py < grass/<page>.html > test.sh`, then
  run it with `grass ~/grassdata/nc_spm_08_grass7/<test_mapset>/ --exec ./test.sh`
  against the nc_spm_08_grass7 sample dataset (full recipe in README).
- Link checking: `./check-links.sh build/<page>.html` (requires linkchecker).

## Conventions

- Write "GRASS", never "GRASS GIS".
- Content license is CC BY-SA 4.0; copyright years live in README and
  `foot.html` and are updated together each calendar year.
