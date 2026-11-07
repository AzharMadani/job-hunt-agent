# Job Hunt Agent — Rules

## Search
- Source: Indeed connector, full-time only, US (country_code US)
- Location: anywhere in the US (onsite, hybrid, or remote)
- Recency: posted in the last 24 hours (widen to 72h only if fewer than 5 strong matches; say so)
- Target roles: see `profile/profile.md`
- Salary: no floor (report the range when listed)
- Exclude: staffing agencies / recruiting firms, contract-to-hire, roles requiring a security clearance
- Shortlist 5, then pick the top 3 by fit with the base resume

## Resume tailoring (ATS)
- Source of truth: `profile/base-resume.txt` (or the newest resume the candidate provides)
- Single column, standard headings (Summary, Skills, Experience, Education, Additional), no tables/graphics/icons, standard fonts
- Mirror the JD's exact keywords where the candidate genuinely has the skill
- Bullets action-verb-led, no bold lead-ins inside sentences
- NEVER invent employers, titles, dates, metrics, tools, or skills; only reorder, reword, and emphasize what is in the base resume
- Output: PDF named `<First>_<Last>_<Company>_<Role>.pdf`, 1 page preferred (2 max)

## Contacts (Apollo)
- 3 decision makers per role: hiring manager for the team, their skip-level (Director/VP/Head of Data/AI/Risk), and a technical/talent recruiter for that function
- Prefer verified work emails; skip anyone without an email rather than guessing
- Confirm Apollo credit use before revealing emails the first time in a session

## Cold email
- One personalized email per contact (3 per role, 9 total)
- Under 150 words; subject under 8 words
- Structure: specific hook about the company (recent news/product), why this role matters to the candidate, 2 proof points from the resume tied to the JD, soft ask (15-min chat), sign-off from the profile
- No flattery filler, no "I hope this email finds you well"

## Autonomy
- DRAFTS ONLY: create Gmail drafts with the tailored resume attached. Never send emails. Never submit applications.
- End each run with a summary table: role, company, location, pay, apply link, contacts drafted, draft links
