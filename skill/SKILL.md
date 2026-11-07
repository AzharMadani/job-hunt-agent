---
name: job-hunt-agent
description: "Run a job hunt pipeline: find fresh US roles on Indeed, tailor ATS resumes, find hiring contacts in Apollo, and create personalized Gmail cold-email drafts (never sent)."
---

# Job Hunt Agent

End-to-end pipeline: Indeed search -> shortlist 5 -> pick top 3 -> one sub-agent per role (research, ATS resume, Apollo contacts, cold emails, Gmail drafts) -> summary.

## Inputs
- Candidate profile: `profile/profile.md` (name, contact line, sign-off, target queries, fit signals, proof points). Copy `examples/profile.example.md` to start.
- Base resume: `profile/base-resume.txt` (use a newer resume if the candidate provides one).
- Rules: `config/rules.md`. Read it at the start of every run; it overrides defaults below.
- Per-role agent brief: `config/agent-brief.md`.
- Optional overrides in the request (e.g. "only fintech", "last 3 days", "5 roles").

## Hard rules
- DRAFTS ONLY. Never send an email. Never submit a job application.
- Never invent employers, titles, dates, metrics, tools, or skills in the resume or emails. Only reorder, reword, and emphasize what the base resume says.
- Never guess an email address. No verified/likely email from Apollo = skip that contact and pick the next one.
- Exclude staffing agencies, recruiting firms, contract/contract-to-hire, and clearance-required roles.
- Respect a posting that asks candidates not to email resumes: draft without the attachment and point to the portal.

## Step 1 - Search (Indeed)
1. Load the Indeed connector tools (`search_jobs`, `get_job_details`, `get_company_data`).
2. Run one search per target query from the profile (country_code US, job_type fulltime), location "United States" plus "remote" (and the candidate's home city).
3. Keep only postings from the last 24 hours. If fewer than 5 strong matches, widen to 72 hours and say so.
4. Pull job details for candidates. Score fit 1-10 against the base resume using the profile's fit signals. Penalize roles needing 8+ years in a specialty the candidate lacks, or PhD-required research roles.
5. Show a table of the top 5: #, role (linked to apply URL), company, location, pay (if listed), posted, fit score, one-line why. Pick the top 3 by fit and continue unless redirected.

## Step 2 - Apollo setup (once per run)
- Call `apollo_users_api_profile` with include_credit_usage and include_waterfall_capability once.
- Before the first email reveal of the run, state the expected credit use (about 9 enrichments) and confirm.
- Note: People Search and People Enrichment need a paid Apollo plan. If Apollo returns a plan-limit block, stop the contact step and report it; the rest of the pipeline still runs.

## Step 3 - One sub-agent per role (run the 3 in parallel)
Spawn 3 general-purpose agents, one per role. Give each the full JD text, apply link, and paths to `config/agent-brief.md`, `config/rules.md`, `profile/profile.md` and `profile/base-resume.txt`. The brief covers:
a. Research (5-bullet brief with dated, sourced news and outreach hooks)
b. ATS resume (keyword map with gaps, tailored PDF + DOCX via `scripts/build_resume.py`, visual check)
c. Decision makers in Apollo (hiring manager, skip-level, recruiter; enrich by id; skip anyone without an email)
d. Cold emails (one per contact, under 150 words, subject under 8 words)
e. Gmail drafts (attachment = tailored PDF via `sha256:<hash>:<absolute path>`)

## Step 4 - Wrap up
- Send the 3 tailored PDFs to the candidate.
- Final summary table: role, company, location, pay, apply link, 3 contacts (name, title), Gmail draft links, notable keyword gaps.
- List anything that failed (no email found, no pay listed, posting older than 24h) in one short line each.
- Remind the candidate that the drafts are unsent and the applications are theirs to submit.
