"""
Base Harvester Interface and Adapter Implementations.
Provides modular ingestion architecture decoupling feed formats (Markdown, Ashby API, Greenhouse API).
"""

from abc import ABC, abstractmethod
import urllib.request
import urllib.error
import time
import re
from typing import List, Dict, Any, Optional
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from execution.prototype.scrapers.url_utils import resolve_company_name


class BaseHarvester(ABC):
    """Abstract base class for all job feed ingestors."""

    @abstractmethod
    def harvest(self) -> List[Dict[str, Any]]:
        """Harvests and returns standardized raw job records."""
        pass


class MarkdownFeedHarvester(BaseHarvester):
    """
    Ingests community GitHub Markdown tables (e.g. SimplifyJobs repositories).
    Features exponential backoff retry and robust parent entity tracking.
    """

    def __init__(self, feed_urls: List[str], max_retries: int = 3, retry_delay: float = 2.0):
        self.feed_urls = feed_urls
        self.max_retries = max_retries
        self.retry_delay = retry_delay

    def _fetch_url_with_retry(self, url: str) -> Optional[str]:
        """Fetches URL contents with exponential backoff retry protection."""
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) CareerSurgeEngine/1.0"}
        delay = self.retry_delay

        for attempt in range(1, self.max_retries + 1):
            try:
                req = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(req, timeout=15) as response:
                    return response.read().decode("utf-8")
            except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as e:
                print(f"[-] [Attempt {attempt}/{self.max_retries}] Failed fetching {url}: {e}")
                if attempt < self.max_retries:
                    time.sleep(delay)
                    delay *= 2  # Exponential backoff
                else:
                    print(f"[!] Exhausted retries for {url}. Skipping stream.")
                    return None
            except Exception as e:
                print(f"[!] Unexpected error fetching {url}: {e}")
                return None
        return None

    def harvest(self) -> List[Dict[str, Any]]:
        """Harvests and parses all configured markdown feed streams."""
        all_items: List[Dict[str, Any]] = []

        for feed_url in self.feed_urls:
            print(f"[*] Harvesting stream: {feed_url}")
            content = self._fetch_url_with_retry(feed_url)
            if not content:
                continue

            trs = re.findall(r"<tr>(.*?)</tr>", content, re.DOTALL)
            last_company = ""
            feed_items_count = 0

            for tr in trs[1:]:
                tds = re.findall(r"<td>(.*?)</td>", tr, re.DOTALL)
                if len(tds) < 5:
                    continue

                # 1. Extract raw company text
                comp_text = re.sub(r"<[^>]+>", "", tds[0]).strip()
                comp_match = re.search(r">([^<]+)</a>", tds[0]) or re.search(r"<strong>([^<]+)</strong>", tds[0])
                extracted_company = comp_match.group(1).strip() if comp_match else comp_text

                # 2. Extract first application link
                apply_match = re.search(r'href="([^"]+)"', tds[3])
                apply_url = apply_match.group(1).strip() if apply_match else ""
                if not apply_url:
                    continue

                # 3. Determine company name with inheritance and non-alphanumeric fallback
                if "↳" in comp_text or not comp_text or comp_text == "↳":
                    company = last_company
                else:
                    company = extracted_company

                # Safety check: if company is empty or starts with punctuation (↳), resolve from domain
                if not company or not company[0].isalnum():
                    company = resolve_company_name(comp_text, apply_url)

                # Only update last_company if we have a valid alphanumeric enterprise name
                if company and company[0].isalnum():
                    last_company = company

                # 4. Extract title, location, age
                title = re.sub(r"<[^>]+>", "", tds[1]).strip()
                loc = re.sub(r"<[^>]+>", "", tds[2]).strip()

                age_str = re.sub(r"<[^>]+>", "", tds[4]).strip()
                age_days: Optional[int] = None
                age_num = re.search(r"(\d+)", age_str)
                if age_num:
                    age_days = int(age_num.group(1))

                all_items.append({
                    "company": company,
                    "title": title,
                    "location": loc,
                    "raw_url": apply_url,
                    "age_days": age_days,
                    "description": f"{title} at {company} in {loc}"
                })
                feed_items_count += 1

            print(f"[+] Successfully parsed {feed_items_count} entries from stream.")

        return all_items


class AshbyApiHarvester(BaseHarvester):
    """Adapter for querying direct Ashby GraphQL endpoints (Future Sprint)."""
    def harvest(self) -> List[Dict[str, Any]]:
        return []


class GreenhouseApiHarvester(BaseHarvester):
    """Adapter for querying direct Greenhouse public JSON endpoints (Future Sprint)."""
    def harvest(self) -> List[Dict[str, Any]]:
        return []
