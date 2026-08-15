# T&C Danger Highlighter

Most people just click "accept" on privacy policies without reading them — nobody has time to parse paragraph after paragraph of deliberately dense legal language. This tool reads the policy for you and flags the clauses that actually matter.

## What it does

The tool scans a website's privacy policy or terms of service against a curated database of known dangerous clauses, then reports:

- **What was found** — the category of concern (e.g. Unilateral Changes, Mandatory Arbitration, AI Training on Your Data)
- **How severe it is** — High / Medium / Low danger rating
- **What it actually means** — a plain-English explanation, no legal jargon
- **An overall danger score** — a single 0–10 rating summarizing the policy's risk

## How it works

1. The tool reads the full text of a privacy policy or terms of service document.
2. The text is split into sentences and scanned using a sliding window, so related clauses spread across sentence boundaries can still be detected.
3. Each window is checked against a database of known dangerous clause patterns, using keyword co-occurrence — if enough of a clause's defining keywords appear close together, it's flagged as a likely match. This is more realistic than exact-phrase matching, since different companies rarely use identical wording for similar clauses.
4. Matches are deduplicated, then combined into an overall danger score, capped at 10.

## Data sources

The clause database draws from two sources:
- **[ToS;DR](https://tosdr.org)** — a community-maintained database of terms-of-service analysis
- **Independent research** — clauses manually sourced from platforms not well covered by ToS;DR, with a focus on major Indian consumer apps (Paytm, Myntra, Swiggy, PhonePe, Flipkart, and others)

## Tech stack

- **Language:** Python 3.11+
- **Matching:** Python's built-in `re` module, combined with a custom keyword co-occurrence system
- **Database:** Plain Python dictionary (`patterns.py`) — no external database required
- **Planned:** Flask web interface, Chrome extension, `nltk` for improved sentence tokenization and fuzzy matching

## Roadmap

- [ ] Expand self-researched clause coverage, especially for underrepresented Indian platforms
- [ ] Dynamic file input (choose which policy to scan, rather than a hardcoded path)
- [ ] Flask-based web interface
- [ ] Chrome extension that scans the page you're currently viewing
- [ ] Fuzzier matching with `nltk` to catch reworded (not just keyword-matching) clauses

## Status

This is an active work-in-progress portfolio project. The core scanning pipeline (read → match → score → report) is functional; matching accuracy is still being tuned.

## License

This project is licensed under the MIT License.
