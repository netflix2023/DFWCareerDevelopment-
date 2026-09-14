# JobSpy Ingestion Research & Architectural Analysis

> **Topic**: Evaluation of `JobSpy` (Python Multi-Board Scraper Library) vs. Direct ATS Ingestion  
> **Status**: Approved Architectural Research  
> **Author**: Senior Software Engineer | **Product Manager**: Neftali

---

## 1. What is JobSpy?

`JobSpy` is an open-source Python library designed to aggregate job postings across 4 major aggregator platforms simultaneously:
- **LinkedIn**
- **Indeed**
- **Glassdoor**
- **ZipRecruiter**

```python
# Standard JobSpy usage:
from jobspy import scrape_jobs

jobs = scrape_jobs(
    site_name=["indeed", "linkedin", "zip_recruiter", "glassdoor"],
    search_term="software engineer intern",
    location="Dallas, TX",
    results_wanted=25,
    hours_old=72,
    country_indeed='USA'
)
```

---

## 2. Senior Engineering Evaluation: Pros vs. Cons for Our DFW Engine

| Evaluation Criteria | JobSpy (Aggregator Scraper) | Direct ATS & Raw Feeds (Current Pipeline) |
|---|---|---|
| **Coverage** | Broad across smaller local businesses that don't have corporate ATS boards. | Focuses on high-tier tech employers (Capital One, Lockheed, AT&T, TI, Tech Startups). |
| **Speed to Posting** | ⚠️ **Slower (12–48 hrs lag)**: Indeed/LinkedIn aggregate jobs after companies post them. By this time, 100+ candidates have already applied. | 🚀 **Immediate (< 1–2 hrs)**: Catches corporate postings before mass aggregator syndication. |
| **IP Ban / Rate Limit Risk** | ⚠️ **High Risk**: Indeed and LinkedIn aggressively use Cloudflare bot-challenges and TLS fingerprinting. Running JobSpy frequently on a home or cloud IP causes HTTP 403 / 429 errors. | 🟢 **Zero / Low Risk**: Direct ATS public JSON endpoints (Greenhouse, Lever, Ashby) and GitHub raw feeds do not challenge with Cloudflare CAPTCHAs. |
| **Data Cleanliness** | ⚠️ Messy: Ingests recruiter tracking links, affiliate redirects (`indeed.com/rc/clk?...`), and garbage company strings (`↳ Company`). | 🟢 Clean: Returns canonical company ATS domains directly (`boards.greenhouse.io/...`, `myworkdayjobs.com/...`). |

---

## 3. Product Manager Decision & Architecture Rule

Per **Approved PM Decision #4** in [`AGENTS.md`](file:///g:/My%20Drive/AntigravityProjects/Career/AGENTS.md):
> **Indeed / JobSpy Rule**:
> - Our **Primary Pipeline** relies on direct ATS streams (Greenhouse, Lever, Ashby, Workday) and genuine raw university feeds.
> - `JobSpy` is preserved strictly as an **opt-in secondary fallback** (`--enable-jobspy`), used only on-demand when someone specifically wants broad aggregator coverage.
> - This keeps our primary daily engine 100% immune to Cloudflare bans, fast, and completely free of browser automation overhead.
