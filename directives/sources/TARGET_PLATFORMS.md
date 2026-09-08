# Target Job Ingestion Platforms & Source Taxonomy

> **Status**: Candidate Evaluation Matrix (Neftali to review and toggle active sources)  
> **Philosophy**: Favor high-speed, direct ATS endpoints with zero browser bloat, supplemented by fresh date-sorted feeds.

---

## Tier 1: Direct ATS Public JSON APIs (Highest Priority & Speed)
*Why*: Directly queries company careers backend. 0% bot challenge, instantaneous, returns full structured JD text without HTML noise.

| Platform | Endpoint / Pattern | Rate Limits & Auth | Speed to Role | Default Status |
| :--- | :--- | :--- | :--- | :--- |
| **Greenhouse** | `GET https://boards-api.greenhouse.io/v1/boards/{company}/jobs?content=true` | None (Public JSON) | Immediate | **Recommended Active** |
| **Lever** | `GET https://api.lever.co/v0/postings/{company}?mode=json` | None (Public JSON) | Immediate | **Recommended Active** |
| **Ashby** | `POST https://api.ashbyhq.com/posting-api/job-board/{company}` | None (Public JSON) | Immediate | **Recommended Active** |
| **Workday** | `POST https://{company}.wd1.myworkdayjobs.com/wday/cxs/{company}/{board}/jobs` | Light pagination | Immediate | Candidate / Under Review |

---

## Tier 2: Date-Sorted Aggregators & Guest Endpoints
*Why*: High volume of listings across smaller and mid-sized employers.

| Platform | Endpoint / Access Pattern | Tactical Filter / Query | Risk / Guard | Default Status |
| :--- | :--- | :--- | :--- | :--- |
| **LinkedIn Guest** | `GET https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search` | `f_TPR=r86400` (Past 24h) + under 100 applicants | 429 Bot Guard / Jitter | **Candidate / Fast-Track** |
| **Indeed** | RSS Feed / Search URL | Sort by **Date** (`sort=date`), remote=`United States` | Cloudflare bot protection | Candidate / Secondary |
| **Google Jobs** | SerpAPI / Scraper | `after:YYYY-MM-DD` | Rate limits / Quota cost | Optional |

---

## Tier 3: Niche Tech, Startup & Early-Career Ecosystems
*Why*: Less noise, higher response rate for early career and internship seekers.

| Platform | Domain | Focus Areas | Feasibility | Default Status |
| :--- | :--- | :--- | :--- | :--- |
| **Y Combinator (Work at a Startup)** | `workatastartup.com` | High-growth YC tech startups, SWE/AI roles | Clean JSON payloads | Candidate / Strong |
| **Simplify.jobs** | `simplify.jobs` | Early career, 1-click apply, GitHub repo backer | API requires inspection | Candidate |
| **Wellfound (formerly AngelList)** | `wellfound.com` | Early-stage startups, equity roles | Strict Cloudflare guard | Candidate / Defer |
| **Handshake** | `joinhandshake.com` | University/college campus verified roles | Requires student auth session | Candidate / Phase 2 |

---

## Tier 4: Community-Curated GitHub Repositories (Golden Lists)
*Why*: Maintained by community in real-time with verified links to fresh SWE/Data internships and new grad roles.

| Repository | Source URL | Content Format | Extraction Strategy | Default Status |
| :--- | :--- | :--- | :--- | :--- |
| **SimplifyJobs / Summer 2025 Internships** | `SimplifyJobs/Summer2025-Internships` | Markdown Table | GitHub raw README parser | **Recommended Active** |
| **SimplifyJobs / New Grad Positions** | `SimplifyJobs/New-Grad-Positions` | Markdown Table | GitHub raw README parser | **Recommended Active** |
| **Pitt-CSC / Tech Internships** | Community repository mirrors | Markdown / JSON | Git raw fetch | Candidate |
