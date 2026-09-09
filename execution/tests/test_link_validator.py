"""Unit tests for live link validator with mock and concurrent checks."""

import unittest
from unittest.mock import patch, MagicMock
from execution.scrapers.link_validator import check_url_liveness, validate_job_links_concurrently
from execution.scrapers.models import JobPosting


class TestLinkValidator(unittest.TestCase):

    @patch("urllib.request.urlopen")
    def test_active_link_returns_true(self, mock_urlopen: MagicMock) -> None:
        mock_response = MagicMock()
        mock_response.getcode.return_value = 200
        mock_response.read.return_value = b"<html><head><title>Job Details</title></head><body>Apply Now</body></html>"
        mock_urlopen.return_value.__enter__.return_value = mock_response

        is_alive, reason = check_url_liveness("https://boards.greenhouse.io/test/jobs/123", timeout=2)
        self.assertTrue(is_alive)
        self.assertEqual(reason, "200 OK")

    @patch("urllib.request.urlopen")
    def test_closed_job_keyword_flagged(self, mock_urlopen: MagicMock) -> None:
        mock_response = MagicMock()
        mock_response.getcode.return_value = 200
        mock_response.read.return_value = b"<html><body>This job posting is no longer accepting applications.</body></html>"
        mock_urlopen.return_value.__enter__.return_value = mock_response

        is_alive, reason = check_url_liveness("https://jobs.lever.co/test/123", timeout=2)
        self.assertFalse(is_alive)
        self.assertIn("Position closed", reason)

    @patch("urllib.request.urlopen")
    def test_concurrent_filtering(self, mock_urlopen: MagicMock) -> None:
        mock_response = MagicMock()
        mock_response.getcode.return_value = 200
        mock_response.read.return_value = b"<html><body>Active Role</body></html>"
        mock_urlopen.return_value.__enter__.return_value = mock_response

        job = JobPosting(
            job_id="test1",
            company="TestCo",
            title="AI Intern",
            ats_source="greenhouse",
            apply_url="https://boards.greenhouse.io/test/jobs/1",
            location="Dallas, TX",
            match_score=0.9
        )

        valid_jobs, dead_jobs = validate_job_links_concurrently([job], max_workers=2, timeout=2)
        self.assertEqual(len(valid_jobs), 1)
        self.assertEqual(len(dead_jobs), 0)


if __name__ == "__main__":
    unittest.main()
