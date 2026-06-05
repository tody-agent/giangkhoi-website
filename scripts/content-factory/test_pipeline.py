#!/usr/bin/env python3
"""
Test Pipeline — TDD test suite for content factory.
Validates keyword matrix, blog generator, and quality gate.
"""

import os
import sys
import json
import tempfile
import unittest

# Add script directory to path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from keyword_matrix import get_keywords, get_keywords_by_tier, get_keywords_by_area, get_keywords_by_category
from generate_blog import generate_blog_post, generate_frontmatter, load_config
from quality_gate import parse_mdx, check_frontmatter, check_content, validate_all


class TestKeywordMatrix(unittest.TestCase):
    """Test keyword matrix completeness and consistency."""

    def setUp(self):
        self.keywords = get_keywords()

    def test_has_100_keywords(self):
        """Matrix should contain exactly 100 keywords."""
        self.assertEqual(len(self.keywords), 100, f"Expected 100 keywords, got {len(self.keywords)}")

    def test_unique_ids(self):
        """All keyword IDs should be unique."""
        ids = [k["id"] for k in self.keywords]
        self.assertEqual(len(ids), len(set(ids)), "Duplicate IDs found")

    def test_unique_slugs(self):
        """All slugs should be unique."""
        slugs = [k["slug"] for k in self.keywords]
        self.assertEqual(len(slugs), len(set(slugs)), "Duplicate slugs found")

    def test_unique_titles(self):
        """All titles should be unique."""
        titles = [k["title"] for k in self.keywords]
        self.assertEqual(len(titles), len(set(titles)), "Duplicate titles found")

    def test_required_fields(self):
        """Each keyword should have all required fields."""
        required = ["id", "slug", "title", "description", "category", "priority", "area", "tags", "keywords"]
        for kw in self.keywords:
            for field in required:
                self.assertIn(field, kw, f"Keyword {kw.get('id', '?')} missing field: {field}")

    def test_valid_categories(self):
        """All categories should be valid."""
        valid = {"cuu-ho", "dan-dung", "cong-nghiep", "huong-dan", "bang-gia", "kien-thuc", "khu-vuc"}
        for kw in self.keywords:
            self.assertIn(kw["category"], valid, f"Invalid category: {kw['category']} in {kw['slug']}")

    def test_valid_priorities(self):
        """All priorities should be valid."""
        valid = {"tier1", "tier2", "tier3", "tier4"}
        for kw in self.keywords:
            self.assertIn(kw["priority"], valid, f"Invalid priority: {kw['priority']} in {kw['slug']}")

    def test_tier_distribution(self):
        """Tiers should have balanced distribution."""
        tier1 = get_keywords_by_tier("tier1")
        tier2 = get_keywords_by_tier("tier2")
        tier3 = get_keywords_by_tier("tier3")
        tier4 = get_keywords_by_tier("tier4")
        self.assertEqual(len(tier1), 30, f"Tier1 should have 30, got {len(tier1)}")
        self.assertEqual(len(tier2), 30, f"Tier2 should have 30, got {len(tier2)}")
        self.assertEqual(len(tier3), 25, f"Tier3 should have 25, got {len(tier3)}")
        self.assertEqual(len(tier4), 15, f"Tier4 should have 15, got {len(tier4)}")

    def test_keywords_have_primary(self):
        """Each keyword should have a primary keyword."""
        for kw in self.keywords:
            self.assertIn("primary", kw["keywords"], f"Missing primary keyword in {kw['slug']}")
            self.assertTrue(kw["keywords"]["primary"].strip(), f"Empty primary keyword in {kw['slug']}")

    def test_description_length(self):
        """Descriptions should be under 160 characters."""
        for kw in self.keywords:
            self.assertLessEqual(len(kw["description"]), 165,
                                 f"Description too long ({len(kw['description'])} chars) in {kw['slug']}")

    def test_filter_by_area(self):
        """Should filter keywords by area correctly."""
        hy = get_keywords_by_area("Hưng Yên")
        self.assertTrue(len(hy) > 10, f"Expected >10 Hưng Yên keywords, got {len(hy)}")

    def test_filter_by_category(self):
        """Should filter keywords by category correctly."""
        cuu_ho = get_keywords_by_category("cuu-ho")
        self.assertTrue(len(cuu_ho) >= 5, f"Expected >=5 cuu-ho keywords, got {len(cuu_ho)}")


class TestBlogGenerator(unittest.TestCase):
    """Test blog post generation."""

    def setUp(self):
        self.config = load_config()
        self.keywords = get_keywords()
        self.sample_kw = self.keywords[0]  # First keyword

    def test_config_loads(self):
        """Config should load without errors."""
        self.assertIn("brand", self.config)
        self.assertIn("phone", self.config["brand"])

    def test_generate_frontmatter(self):
        """Frontmatter should contain required YAML fields."""
        fm = generate_frontmatter(self.sample_kw)
        self.assertIn("---", fm)
        self.assertIn("title:", fm)
        self.assertIn("description:", fm)
        self.assertIn("category:", fm)
        self.assertIn("faq:", fm)

    def test_generate_blog_post_not_empty(self):
        """Generated blog post should not be empty."""
        post = generate_blog_post(self.sample_kw, self.config)
        self.assertTrue(len(post) > 500, f"Post too short: {len(post)} chars")

    def test_generate_blog_post_has_cta(self):
        """Generated post should contain CTA."""
        post = generate_blog_post(self.sample_kw, self.config)
        self.assertIn("0971", post, "Post missing phone CTA")

    def test_generate_blog_post_has_internal_links(self):
        """Generated post should contain internal links."""
        post = generate_blog_post(self.sample_kw, self.config)
        self.assertIn("/vi/", post, "Post missing internal links")

    def test_generate_all_categories(self):
        """Should generate content for all category types."""
        categories_seen = set()
        # Sample every 10th keyword to cover all tiers/categories
        sampled = self.keywords[::10]
        for kw in sampled:
            post = generate_blog_post(kw, self.config)
            categories_seen.add(kw["category"])
            self.assertTrue(len(post) > 200, f"Post {kw['slug']} too short")

        self.assertTrue(len(categories_seen) >= 3, f"Should cover at least 3 categories, got {categories_seen}")

    def test_generate_post_parseable(self):
        """Generated post should be parseable as MDX."""
        post = generate_blog_post(self.sample_kw, self.config)
        parts = post.split("---", 2)
        self.assertEqual(len(parts), 3, "Post should have frontmatter delimiters")


class TestQualityGate(unittest.TestCase):
    """Test quality gate validation."""

    def test_valid_frontmatter_passes(self):
        """Valid frontmatter should pass checks."""
        fm = {
            "title": "Test Title",
            "description": "Test description under 160 chars",
            "date": "2026-06-06",
            "category": "cuu-ho",
            "priority": "tier1",
            "tags": ["test"],
            "area": ["Hưng Yên"],
            "keywords": {"primary": "test keyword", "secondary": [], "lsi": []},
            "faq": [
                {"question": "Q1?", "answer": "A1"},
                {"question": "Q2?", "answer": "A2"},
                {"question": "Q3?", "answer": "A3"},
            ],
            "author": "Test",
        }
        errors = check_frontmatter(fm, "test.mdx")
        self.assertEqual(len(errors), 0, f"Unexpected errors: {errors}")

    def test_missing_fields_detected(self):
        """Missing required fields should be detected."""
        fm = {"title": "Test"}
        errors = check_frontmatter(fm, "test.mdx")
        self.assertTrue(len(errors) > 0, "Should detect missing fields")

    def test_invalid_category_detected(self):
        """Invalid category should be detected."""
        fm = {
            "title": "Test",
            "description": "Test",
            "date": "2026-06-06",
            "category": "invalid-category",
            "priority": "tier1",
            "tags": [],
            "area": [],
            "keywords": {"primary": "test"},
            "faq": [{"question": "Q?", "answer": "A"}, {"question": "Q?", "answer": "A"}, {"question": "Q?", "answer": "A"}],
            "author": "Test",
        }
        errors = check_frontmatter(fm, "test.mdx")
        self.assertTrue(any("Invalid category" in e for e in errors))

    def test_content_with_cta_passes(self):
        """Content with CTA should pass content check."""
        content = """## Heading 1

Some content about xe cẩu. Gọi ngay 0971 491 174.

## Heading 2

More content with [link](/vi/dich-vu/cau-bon-nuoc) and [another](/vi/khu-vuc/my-hao).
Tel: tel:0971491174 for more info.
""" + " word" * 400
        errors = check_content(content, "test.mdx")
        self.assertEqual(len(errors), 0, f"Unexpected errors: {errors}")

    def test_short_content_fails(self):
        """Content under minimum word count should fail."""
        content = "Short content."
        errors = check_content(content, "test.mdx")
        self.assertTrue(any("Word count" in e for e in errors))


class TestIntegration(unittest.TestCase):
    """Integration test — generate and validate sample posts."""

    def test_generate_and_validate_sample(self):
        """Generate a sample post, save to temp dir, validate it."""
        config = load_config()
        keywords = get_keywords()

        with tempfile.TemporaryDirectory() as tmpdir:
            # Generate 5 sample posts
            for kw in keywords[:5]:
                content = generate_blog_post(kw, config)
                filepath = os.path.join(tmpdir, f"{kw['slug']}.mdx")
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(content)

            # Validate
            passed, total, errors = validate_all(tmpdir)
            self.assertEqual(total, 5, f"Expected 5 posts, got {total}")
            self.assertEqual(passed, 5, f"Expected 5 passed, got {passed}. Errors: {errors}")


if __name__ == "__main__":
    print("🧪 Running TDD Test Suite for Content Factory\n")
    unittest.main(verbosity=2)
