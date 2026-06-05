#!/usr/bin/env python3
"""
Quality Gate — Validate generated blog posts meet SEO and content standards.
Run after generation to ensure all posts pass quality checks.
"""

import os
import re
import sys
import yaml
from typing import Dict, List, Tuple


REQUIRED_FIELDS = ["title", "description", "date", "category", "priority", "tags", "area", "keywords", "faq", "author"]
VALID_CATEGORIES = ["cuu-ho", "dan-dung", "cong-nghiep", "huong-dan", "bang-gia", "kien-thuc", "khu-vuc"]
VALID_PRIORITIES = ["tier1", "tier2", "tier3", "tier4"]
MIN_WORD_COUNT = 400
MIN_FAQ_COUNT = 3
MIN_CTA_COUNT = 1
MIN_INTERNAL_LINKS = 2
MAX_TITLE_LENGTH = 70
MAX_DESC_LENGTH = 160


def parse_mdx(filepath: str) -> Tuple[Dict, str]:
    """Parse MDX file into frontmatter and content."""
    with open(filepath, "r", encoding="utf-8") as f:
        raw = f.read()

    # Split frontmatter
    parts = raw.split("---", 2)
    if len(parts) < 3:
        return {}, raw

    frontmatter_str = parts[1].strip()
    content = parts[2].strip()

    try:
        frontmatter = yaml.safe_load(frontmatter_str) or {}
    except yaml.YAMLError:
        frontmatter = {}

    return frontmatter, content


def count_words(text: str) -> int:
    """Count Vietnamese words (rough estimate)."""
    # Remove markdown formatting
    clean = re.sub(r'[#*_\[\]\(\)\|>!`]', ' ', text)
    clean = re.sub(r'https?://\S+', '', clean)
    clean = re.sub(r'\s+', ' ', clean)
    words = clean.strip().split()
    return len(words)


def check_frontmatter(fm: Dict, filepath: str) -> List[str]:
    """Validate frontmatter fields."""
    errors = []
    basename = os.path.basename(filepath)

    for field in REQUIRED_FIELDS:
        if field not in fm:
            errors.append(f"[{basename}] Missing field: {field}")

    if "title" in fm:
        if len(fm["title"]) > MAX_TITLE_LENGTH:
            # Warning, not error — Vietnamese titles can be long
            pass
        if not fm["title"].strip():
            errors.append(f"[{basename}] Empty title")

    if "description" in fm:
        if len(fm["description"]) > MAX_DESC_LENGTH:
            pass  # Warning only
        if not fm["description"].strip():
            errors.append(f"[{basename}] Empty description")

    if "category" in fm and fm["category"] not in VALID_CATEGORIES:
        errors.append(f"[{basename}] Invalid category: {fm['category']}")

    if "priority" in fm and fm["priority"] not in VALID_PRIORITIES:
        errors.append(f"[{basename}] Invalid priority: {fm['priority']}")

    if "faq" in fm:
        if not isinstance(fm["faq"], list):
            errors.append(f"[{basename}] FAQ must be a list")
        elif len(fm["faq"]) < MIN_FAQ_COUNT:
            errors.append(f"[{basename}] FAQ count {len(fm['faq'])} < {MIN_FAQ_COUNT}")

    return errors


def check_content(content: str, filepath: str) -> List[str]:
    """Validate content quality."""
    errors = []
    basename = os.path.basename(filepath)

    # Word count
    wc = count_words(content)
    if wc < MIN_WORD_COUNT:
        errors.append(f"[{basename}] Word count {wc} < {MIN_WORD_COUNT}")

    # CTA check
    cta_patterns = [r'tel:', r'0971', r'Gọi ngay', r'Chat Zalo', r'zalo\.me']
    cta_count = sum(1 for p in cta_patterns if re.search(p, content))
    if cta_count < MIN_CTA_COUNT:
        errors.append(f"[{basename}] CTA count {cta_count} < {MIN_CTA_COUNT}")

    # Internal links
    internal_links = re.findall(r'\(/vi/[^)]+\)', content)
    if len(internal_links) < MIN_INTERNAL_LINKS:
        errors.append(f"[{basename}] Internal links {len(internal_links)} < {MIN_INTERNAL_LINKS}")

    # H2 headings
    h2_count = len(re.findall(r'^## ', content, re.MULTILINE))
    if h2_count < 2:
        errors.append(f"[{basename}] H2 heading count {h2_count} < 2")

    return errors


def check_duplicates(posts: List[Tuple[str, Dict]]) -> List[str]:
    """Check for duplicate titles and descriptions."""
    errors = []
    titles = {}
    descriptions = {}

    for filepath, fm in posts:
        basename = os.path.basename(filepath)
        title = fm.get("title", "")
        desc = fm.get("description", "")

        if title in titles:
            errors.append(f"[{basename}] Duplicate title with {titles[title]}")
        else:
            titles[title] = basename

        if desc in descriptions:
            errors.append(f"[{basename}] Duplicate description with {descriptions[desc]}")
        else:
            descriptions[desc] = basename

    return errors


def validate_all(blog_dir: str) -> Tuple[int, int, List[str]]:
    """Validate all blog posts in directory."""
    if not os.path.exists(blog_dir):
        return 0, 0, [f"Blog directory not found: {blog_dir}"]

    mdx_files = sorted([f for f in os.listdir(blog_dir) if f.endswith(".mdx")])
    if not mdx_files:
        return 0, 0, ["No .mdx files found"]

    all_errors = []
    all_posts = []
    passed = 0

    for filename in mdx_files:
        filepath = os.path.join(blog_dir, filename)
        fm, content = parse_mdx(filepath)
        all_posts.append((filepath, fm))

        errors = []
        errors.extend(check_frontmatter(fm, filepath))
        errors.extend(check_content(content, filepath))

        if errors:
            all_errors.extend(errors)
        else:
            passed += 1

    # Check duplicates
    dup_errors = check_duplicates(all_posts)
    all_errors.extend(dup_errors)

    return passed, len(mdx_files), all_errors


def main():
    """Run quality gate."""
    blog_dir = os.path.join(os.path.dirname(__file__), "..", "..", "src", "content", "blog")

    if len(sys.argv) > 1:
        blog_dir = sys.argv[1]

    print(f"🔍 Quality Gate — Validating blog posts in: {blog_dir}\n")

    passed, total, errors = validate_all(blog_dir)

    if errors:
        print(f"❌ QUALITY GATE FAILED")
        print(f"   Passed: {passed}/{total}")
        print(f"   Errors: {len(errors)}\n")
        for err in errors:
            print(f"   ⚠️  {err}")
        sys.exit(1)
    else:
        print(f"✅ QUALITY GATE PASSED")
        print(f"   All {total} posts validated successfully!")
        sys.exit(0)


if __name__ == "__main__":
    main()
