# Job Hunt Agent

A Claude Code skill that runs a job search end to end:

1. **Search** Indeed for fresh full-time US roles (last 24h, widening to 72h if needed) and score fit against your resume.
2. **Shortlist** the top 5, then pick the top 3.
3. **Per role, in parallel:** research the company, tailor an ATS-friendly 1-page resume (PDF + DOCX), find the hiring manager, skip-level and recruiter in Apollo, and write a personalized cold email for each.
4. **Draft** the emails in Gmail with the tailored resume attached. Nothing is ever sent and no application is ever submitted.

## Layout

```
skill/SKILL.md               The Claude Code skill (pipeline steps and hard rules)
config/rules.md              Search, resume, contact and email rules
config/agent-brief.md        Instructions handed to each per-role sub-agent
scripts/build_resume.py      content.json -> PDF + DOCX + page1.png
examples/profile.example.md  Template for your profile (name, contact, queries, proof points)
examples/content.example.json  Resume content schema
profile/                     Your profile and base resume (gitignored)
resumes/ emails/ work/       Generated output (gitignored)
```

## Setup

1. Install the skill: copy `skill/` to `~/.claude/skills/job-hunt-agent/` (or add it through your Claude skills settings).
2. Create your profile:
   ```bash
   cp examples/profile.example.md profile/profile.md
   ```
   Then put your plain-text resume in `profile/base-resume.txt`.
3. Install the resume builder's dependencies:
   ```bash
   python3 -m venv .venv && .venv/bin/pip install python-docx reportlab pymupdf
   ```
4. Connect these in Claude: **Indeed** (job search), **Apollo** (contacts; People Search and Enrichment need a paid plan), and **Gmail** (drafts).

## Run

In Claude Code, from this folder: `Run my job hunt` (optionally: "only fintech", "last 3 days", "5 roles").

Build a resume by hand:

```bash
.venv/bin/python scripts/build_resume.py examples/content.example.json /tmp/test.pdf /tmp/test.docx
```

## Guardrails

- Drafts only: never sends email, never submits applications.
- Never invents employers, titles, dates, metrics, tools or skills; only reorders and rewords the base resume.
- Never guesses email addresses; contacts without a verified email are skipped.
- Excludes staffing agencies, contract-to-hire and clearance-required roles.
- Respects postings that ask not to receive resumes by email.
