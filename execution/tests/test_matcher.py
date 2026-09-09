"""Unit tests for transparent weighted qualification matcher."""

import unittest
from execution.scrapers.qualification_matcher import (
    evaluate_qualification_match,
    classify_role_category
)


class TestQualificationMatcher(unittest.TestCase):

    def test_core_skill_scoring_vs_secondary(self):
        # A job requiring core skills (Python, RAG, SQL) should score higher than one with just secondary tools (Git, Excel)
        score_core, skills_core, qualifies_core = evaluate_qualification_match(
            "AI Engineer Intern",
            "Must know Python, RAG pipelines, and SQL databases"
        )
        score_sec, skills_sec, qualifies_sec = evaluate_qualification_match(
            "Technology Intern",
            "Must know git, excel, and basic analytics"
        )

        self.assertTrue(qualifies_core)
        self.assertTrue(qualifies_sec)
        self.assertGreater(score_core, score_sec, "Core skills must score higher than generic tools")

    def test_prevent_redundant_substring_double_counting(self):
        # "data analytics" shouldn't double count "analytics" as two separate skills
        score, skills, _ = evaluate_qualification_match(
            "Data Analyst Intern",
            "Experience with data analytics and SQL queries"
        )
        self.assertIn("data analytics", skills)
        self.assertNotIn("analytics", skills, "'analytics' should not be double-counted when 'data analytics' matched")

    def test_role_category_precedence_ai_first(self):
        # Compound title with both AI and Data Analyst should prioritize AI/ML
        cat = classify_role_category("Data Scientist Intern - Generative AI")
        self.assertEqual(cat, "AI/ML & GenAI")


if __name__ == "__main__":
    unittest.main()
