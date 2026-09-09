"""Unit tests for URL utilities, company normalization, and deterministic ID hashing."""

import unittest
from execution.scrapers.url_utils import (
    clean_canonical_url,
    detect_ats_source,
    resolve_company_name,
    extract_requisition_id,
    generate_job_id,
    sanitize_location
)


class TestUrlUtils(unittest.TestCase):

    def test_strip_tracking_params(self) -> None:
        url = "https://boards.greenhouse.io/company/jobs/12345?gh_src=linkedin&utm_medium=jobboard&utm_source=indeed"
        clean = clean_canonical_url(url)
        self.assertEqual(clean, "https://boards.greenhouse.io/company/jobs/12345")

    def test_resolve_company_name_from_subdomain(self) -> None:
        # Case 1: Raw arrow character
        boeing_url = "https://boeing.wd1.myworkdayjobs.com/EXTERNAL_CAREERS/job/Seattle-WA/Intern-Systems-Engineer_JR2026520976-1"
        self.assertEqual(resolve_company_name("\u21b3", boeing_url), "Boeing")
        self.assertEqual(resolve_company_name("↳", boeing_url), "Boeing")
        self.assertEqual(resolve_company_name("↳ Boeing", boeing_url), "Boeing")

        # Case 2: NXP Semiconductors
        nxp_url = "https://nxp.wd3.myworkdayjobs.com/careers/job/Austin-TX/Embedded-Software-Intern_R102938"
        self.assertEqual(resolve_company_name("↳", nxp_url), "NXP Semiconductors")

        # Case 3: Nationwide
        nw_url = "https://nationwide.wd1.myworkdayjobs.com/Nationwide/job/Columbus-OH/Data-Science-Intern_JR12345"
        self.assertEqual(resolve_company_name("", nw_url), "Nationwide")

        # Case 4: Valid explicit name preserved
        self.assertEqual(resolve_company_name("Copart", "https://copart.wd1.myworkdayjobs.com/..."), "Copart")
        self.assertEqual(resolve_company_name("The Boeing Company", boeing_url), "Boeing")

    def test_extract_requisition_id_and_deduplication(self) -> None:
        url1 = "https://boeing.wd1.myworkdayjobs.com/EXTERNAL_CAREERS/job/Seattle-WA/Intern-Systems-Engineer_JR2026520976-1"
        url2 = "https://boeing.wd1.myworkdayjobs.com/INTERN/job/Seattle-WA/Intern-Systems-Engineer_JR2026520976"

        req1 = extract_requisition_id(url1)
        req2 = extract_requisition_id(url2)

        self.assertEqual(req1, "JR2026520976")
        self.assertEqual(req2, "JR2026520976")

        # Generating job IDs for identical requisitions across internal boards MUST match!
        id1 = generate_job_id("The Boeing Company", "Intern - Systems Engineer", url1)
        id2 = generate_job_id("Boeing", "Intern - Systems Engineer", url2)
        self.assertEqual(id1, id2)

        # Generating job IDs without a req ID should match if company and title match, even with different URLs
        url_a = "https://startup.com/careers/ai-intern-2027?source=linkedin"
        url_b = "https://startup.com/jobs/ai-intern-2027?source=indeed"
        id_a = generate_job_id("TechCorp", "AI Engineer Intern", url_a)
        id_b = generate_job_id("TechCorp", "AI Engineer Intern", url_b)
        self.assertEqual(id_a, id_b)


    def test_sanitize_multi_location(self) -> None:
        messy_blob = "30 locationsRidley Park, PASeattle, WALong Beach, CAMesa, AZDallas, TX"
        sanitized = sanitize_location(messy_blob, is_dfw=True)
        self.assertEqual(sanitized, "Dallas, TX (Multi-Location)")

        clean_plano = "Plano, TX"
        self.assertEqual(sanitize_location(clean_plano, is_dfw=True), "Plano, TX")

    def test_detect_ats_sources(self) -> None:
        self.assertEqual(detect_ats_source("https://boards.greenhouse.io/test/jobs/1"), "greenhouse")
        self.assertEqual(detect_ats_source("https://jobs.lever.co/test/1"), "lever")
        self.assertEqual(detect_ats_source("https://jobs.ashbyhq.com/test/1"), "ashby")
        self.assertEqual(detect_ats_source("https://copart.wd1.myworkdayjobs.com/test"), "workday")
        self.assertEqual(detect_ats_source("https://careers.ti.com/job/123/?icims=1"), "icims")


if __name__ == "__main__":
    unittest.main()
