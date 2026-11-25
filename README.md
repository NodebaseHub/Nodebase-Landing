# Nodebase-Landing

Public site for nodebasehub.com. Cloudflare serves `production/v2.2/` and deploys when `main` changes.

## Folders
- `production/v2.2/` - the web root. Only files the browser needs go here. Anything else here is public.
- `content/curators.json` - the single source of truth for the curator cards on Cafe Hoppers (EN + ZH).
- `tools/` - build and check scripts (not served).
- `docs/` - working notes and context briefs (not served).

## Workflow
1. Claude works on a branch, never on `main`.
2. Curator or pick changes go in `content/curators.json`, then `python3 tools/build_curators.py` rebuilds both Cafe Hoppers pages. Don't hand-edit between the `SSOT:CURATORS` markers.
3. `python3 tools/release_check.py` must say GO before a merge.
4. JT reviews, pushes and merges in GitHub Desktop.

## Content rules
- Curator quotes stay in English on both pages; labels translate to Hong Kong Traditional Chinese.
- A pick shows "Quote coming soon" until the curator's quote is in the JSON.
