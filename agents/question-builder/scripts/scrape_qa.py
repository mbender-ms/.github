#!/usr/bin/env python3
"""
Scrape Microsoft Q&A questions for any Azure service tag,
group similar questions by fuzzy matching, and compare against
an optional canonical question set.

Usage:
  python scrape_qa.py --tag azure-application-gateway --tag-id 148
  python scrape_qa.py --tag azure-firewall --tag-id 197 --output-dir ./output
  python scrape_qa.py --tag azure-load-balancer --tag-id 185 --canonical canonical.csv
  python scrape_qa.py --tag azure-virtual-network --tag-id 75 --smoke-test

Outputs (prefixed with the tag slug):
  {tag}_qa_raw.csv              Ungrouped question dump (checkpoint)
  {tag}_qa_questions.csv        Grouped with canonical overlap flags
  {tag}_qa_overlap.csv          Only canonical overlaps (if canonical CSV provided)
  {tag}_qa_unique_questions.csv Unique groups not in canonical set, by frequency
"""

import argparse
import csv
import os
import re
import sys
import time
from collections import defaultdict
from datetime import datetime
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from thefuzz import fuzz

PAGE_DELAY = 1.5
RETRY_LIMIT = 3
RETRY_BACKOFF = 2.0

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}

QUESTION_URL_RE = re.compile(r"/en-us/answers/questions/(\d+)/")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Scrape Microsoft Q&A questions for an Azure service tag."
    )
    parser.add_argument(
        "--tag", required=True, help="Q&A tag slug, e.g. 'azure-application-gateway'"
    )
    parser.add_argument(
        "--tag-id", required=True, type=int, help="Numeric tag ID from the Q&A URL, e.g. 148"
    )
    parser.add_argument(
        "--output-dir", default=".", help="Directory for output CSVs (default: current directory)"
    )
    parser.add_argument(
        "--canonical",
        help="Path to a canonical CSV for overlap comparison. Must have a 'Canonical question' column.",
    )
    parser.add_argument(
        "--group-threshold", type=int, default=75,
        help="Fuzzy similarity % to group similar questions (default: 75)",
    )
    parser.add_argument(
        "--canonical-threshold", type=int, default=65,
        help="Fuzzy similarity % to match canonical questions (default: 65)",
    )
    parser.add_argument(
        "--min-rows", type=int, default=100,
        help="Minimum expected rows — abort if fewer scraped (default: 100)",
    )
    parser.add_argument(
        "--fetch-summaries", action="store_true",
        help="Fetch each unique question's Q&A page to extract the real question body for the summary column.",
    )
    parser.add_argument(
        "--smoke-test", action="store_true", help="Only fetch page 1 and validate extraction, then exit"
    )
    return parser.parse_args()


def build_base_url(tag_id: int, tag_slug: str) -> str:
    return f"https://learn.microsoft.com/en-us/answers/tags/{tag_id}/{tag_slug}"


def fetch_page(url: str) -> requests.Response | None:
    for attempt in range(1, RETRY_LIMIT + 1):
        try:
            resp = requests.get(url, headers=HEADERS, timeout=30)
            if resp.status_code == 200:
                return resp
            if resp.status_code == 429 or resp.status_code >= 500:
                wait = RETRY_BACKOFF ** attempt
                print(
                    f"  HTTP {resp.status_code} on {url} — retrying in {wait:.0f}s "
                    f"(attempt {attempt}/{RETRY_LIMIT})"
                )
                time.sleep(wait)
                continue
            print(f"  HTTP {resp.status_code} on {url} — skipping")
            return None
        except requests.RequestException as exc:
            wait = RETRY_BACKOFF ** attempt
            print(
                f"  Request error: {exc} — retrying in {wait:.0f}s "
                f"(attempt {attempt}/{RETRY_LIMIT})"
            )
            time.sleep(wait)
    print(f"  Failed after {RETRY_LIMIT} attempts: {url}")
    return None


def extract_questions(soup: BeautifulSoup) -> list[dict]:
    questions = []
    for link in soup.find_all("a", href=QUESTION_URL_RE):
        href = link.get("href", "")
        title = link.get_text(strip=True)
        if not title or not href:
            continue

        match = QUESTION_URL_RE.search(href)
        if not match:
            continue

        question_id = match.group(1)
        full_url = urljoin("https://learn.microsoft.com", href)

        answer_count = 0
        date_asked = ""
        container = link.find_parent(["div", "li", "article", "section"])
        if container:
            text = container.get_text(" ", strip=True)
            answer_match = re.search(r"(\d+)\s+answers?", text)
            if answer_match:
                answer_count = int(answer_match.group(1))
            date_match = re.search(r"asked\s+(\w+\s+\d{1,2},\s+\d{4})", text)
            if date_match:
                date_asked = date_match.group(1)

        questions.append(
            {
                "question_id": question_id,
                "title": title,
                "url": full_url,
                "answer_count": answer_count,
                "date_asked": date_asked,
            }
        )
    return questions


def deduplicate(questions: list[dict]) -> tuple[list[dict], int]:
    seen_urls: set[str] = set()
    deduped: list[dict] = []
    for question in questions:
        if question["url"] not in seen_urls:
            seen_urls.add(question["url"])
            deduped.append(question)
    return deduped, len(questions) - len(deduped)


def detect_total_pages(base_url: str) -> int:
    resp = fetch_page(base_url)
    if resp is None:
        return 1

    soup = BeautifulSoup(resp.text, "html.parser")
    max_page = 1
    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"]
        match = re.search(r"[?&]page=(\d+)", href)
        if match:
            page_num = int(match.group(1))
            if page_num > max_page:
                max_page = page_num

    for el in soup.find_all(string=re.compile(r"^\d+$")):
        parent = el.find_parent("a")
        if parent and parent.get("href") and "page=" in parent.get("href", ""):
            try:
                num = int(el.strip())
                if num > max_page:
                    max_page = num
            except ValueError:
                pass

    return max_page


def normalize_title(title: str, tag_slug: str) -> str:
    text = title.lower().strip()
    tag_words = tag_slug.replace("-", " ")
    prefixes = [tag_words]
    if tag_words.startswith("azure "):
        prefixes.append(tag_words[6:])
    prefixes.append("azure")

    for prefix in prefixes:
        if text.startswith(prefix):
            text = text[len(prefix):].lstrip(" -:–—")
    return text.strip()


def smoke_test(base_url: str, tag_slug: str) -> list[dict]:
    print("\n=== Smoke Test (page 1 only) ===")
    url = f"{base_url}?page=1"
    resp = fetch_page(url)
    if resp is None:
        print("Smoke test failed: Could not fetch page 1")
        sys.exit(1)

    soup = BeautifulSoup(resp.text, "html.parser")
    questions = extract_questions(soup)

    if len(questions) == 0:
        print("Smoke test failed: No questions extracted from page 1")
        sys.exit(1)

    for question in questions[:3]:
        if not question["title"] or "/answers/questions/" not in question["url"]:
            print("Smoke test failed: bad extracted question data")
            sys.exit(1)

    print(f"Smoke test passed for {tag_slug} — {len(questions)} questions from page 1")
    return questions


def scrape_all_pages(base_url: str, total_pages: int, page1_questions: list[dict]) -> list[dict]:
    print(f"\n=== Scraping pages 2-{total_pages} ===")
    all_questions = list(page1_questions)

    for page_num in range(2, total_pages + 1):
        url = f"{base_url}?page={page_num}"
        resp = fetch_page(url)
        if resp is None:
            print(f"  Skipped page {page_num}")
            continue

        soup = BeautifulSoup(resp.text, "html.parser")
        all_questions.extend(extract_questions(soup))

        if page_num % 10 == 0 or page_num == total_pages:
            print(f"  Page {page_num}/{total_pages} — {len(all_questions)} questions so far")

        time.sleep(PAGE_DELAY)

    return all_questions


def verify_scraped_data(questions: list[dict], min_rows: int) -> list[dict]:
    print("\n=== Post-Scrape Verification ===")
    questions, dup_count = deduplicate(questions)
    print(f"  Duplicates removed: {dup_count}")

    empty_title = sum(1 for q in questions if not q["title"])
    empty_url = sum(1 for q in questions if not q["url"])
    questions = [q for q in questions if q["title"] or q["url"]]
    print(f"  Rows with empty title: {empty_title}")
    print(f"  Rows with empty URL: {empty_url}")

    if len(questions) < min_rows:
        print(f"Verification failed: only {len(questions)} questions (minimum: {min_rows})")
        sys.exit(1)

    dates_parsed = 0
    dates_bad = 0
    for question in questions:
        if question["date_asked"]:
            try:
                dt = datetime.strptime(question["date_asked"], "%b %d, %Y")
                dates_parsed += 1
                if dt.year < 2020 or dt.year > 2027:
                    dates_bad += 1
            except ValueError:
                dates_bad += 1

    if dates_parsed:
        print(f"  Dates parsed: {dates_parsed}, out of range/invalid: {dates_bad}")

    print(f"  Final clean count: {len(questions)}")
    return questions


def write_raw_csv(questions: list[dict], path: str) -> None:
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f, fieldnames=["question_id", "title", "url", "answer_count", "date_asked"]
        )
        writer.writeheader()
        writer.writerows(questions)


def write_questions_csv(questions: list[dict], path: str) -> None:
    fieldnames = [
        "group_id", "question_title", "url", "answer_count", "date_asked",
        "group_representative", "group_count",
        "canonical_overlap", "canonical_question_matched", "similarity_score",
    ]
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for question in questions:
            writer.writerow(
                {
                    "group_id": question["group_id"],
                    "question_title": question["title"],
                    "url": question["url"],
                    "answer_count": question["answer_count"],
                    "date_asked": question["date_asked"],
                    "group_representative": question["group_representative"],
                    "group_count": question["group_count"],
                    "canonical_overlap": question.get("canonical_overlap", ""),
                    "canonical_question_matched": question.get("canonical_question_matched", ""),
                    "similarity_score": question.get("similarity_score", 0),
                }
            )


def write_overlap_csv(overlap_rows: list[dict], path: str) -> None:
    fieldnames = [
        "group_representative", "group_count",
        "canonical_question", "canonical_conversation_count", "similarity_score",
    ]
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(overlap_rows)


def fetch_question_summary(url: str) -> str:
    resp = fetch_page(url)
    if resp is None:
        return ""
    soup = BeautifulSoup(resp.text, "html.parser")
    meta = soup.find("meta", attrs={"name": "description"})
    if meta and meta.get("content"):
        desc = meta["content"].strip()
        if desc.endswith("\u2026"):
            desc = desc[:-1].rstrip() + "..."
        return desc
    return ""


def summarize_as_question(title: str) -> str:
    text = title.strip()
    if not text:
        return text

    question_starters = (
        "how", "what", "why", "when", "where", "which", "who",
        "is ", "are ", "can ", "could ", "do ", "does ", "did ",
        "will ", "would ", "should ", "has ", "have ", "am ",
    )
    lower = text.lower()
    if lower.startswith(question_starters):
        return text.rstrip(".!? ") + "?"
    if text.endswith("?"):
        return text

    error_signals = (
        "error", "fail", "issue", "problem", "not working", "doesn't work",
        "unable", "cannot", "timeout", "refused", "denied", "bad gateway",
        "500", "502", "503", "504", "404", "403", "401",
    )
    if any(signal in lower for signal in error_signals):
        return f"How do I resolve: {text.rstrip('.!? ')}?"
    if len(text.split()) < 8 and not any(c in text for c in "?!."):
        return f"What is {text.rstrip('.!? ')}?"
    return f"How do I {text[0].lower()}{text[1:].rstrip('.!? ')}?"


def write_unique_csv(questions: list[dict], path: str, fetch_summaries: bool = False) -> None:
    seen_groups: dict[int, dict] = {}
    for question in questions:
        group_id = question["group_id"]
        if group_id in seen_groups or question.get("canonical_overlap") == "YES":
            continue
        seen_groups[group_id] = {
            "group_id": group_id,
            "question": question["group_representative"],
            "question_summary": "",
            "group_count": question["group_count"],
            "sample_url": question["url"],
        }

    unique_rows = sorted(seen_groups.values(), key=lambda row: row["group_count"], reverse=True)

    if fetch_summaries:
        for row in unique_rows:
            desc = fetch_question_summary(row["sample_url"])
            row["question_summary"] = desc or summarize_as_question(row["question"])
            time.sleep(PAGE_DELAY)
    else:
        for row in unique_rows:
            row["question_summary"] = summarize_as_question(row["question"])

    fieldnames = ["group_id", "question", "question_summary", "group_count", "sample_url"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(unique_rows)


def group_questions(questions: list[dict], tag_slug: str, threshold: int) -> list[dict]:
    group_id_map: dict[int, int] = {}
    group_reps: dict[int, str] = {}
    group_members: dict[int, list[int]] = defaultdict(list)
    next_group = 1

    normalized = [normalize_title(question["title"], tag_slug) for question in questions]

    for i in range(len(questions)):
        if i in group_id_map:
            continue

        group_id = next_group
        next_group += 1
        group_id_map[i] = group_id
        group_members[group_id].append(i)
        group_reps[group_id] = questions[i]["title"]

        for j in range(i + 1, len(questions)):
            if j in group_id_map:
                continue
            score = fuzz.token_sort_ratio(normalized[i], normalized[j])
            if score >= threshold:
                group_id_map[j] = group_id
                group_members[group_id].append(j)

    for group_id, indices in group_members.items():
        titles = [questions[idx]["title"] for idx in indices]
        group_reps[group_id] = min(titles, key=len)

    for i, question in enumerate(questions):
        group_id = group_id_map[i]
        question["group_id"] = group_id
        question["group_representative"] = group_reps[group_id]
        question["group_count"] = len(group_members[group_id])

    return questions


def load_canonical(path: str) -> list[dict]:
    with open(path, "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def match_canonical(questions: list[dict], canonical: list[dict], tag_slug: str, threshold: int) -> list[dict]:
    group_reps: dict[int, dict] = {}
    for question in questions:
        group_id = question["group_id"]
        if group_id not in group_reps:
            group_reps[group_id] = question

    canonical_titles = [(row["Canonical question"], row) for row in canonical]
    overlap_rows = []

    for group_id, rep_q in group_reps.items():
        best_score = 0
        best_canonical = None
        norm_rep = normalize_title(rep_q["group_representative"], tag_slug)

        for can_title, can_row in canonical_titles:
            norm_can = normalize_title(can_title, tag_slug)
            score = fuzz.token_sort_ratio(norm_rep, norm_can)
            if score > best_score:
                best_score = score
                best_canonical = can_row

        if best_score >= threshold and best_canonical:
            for question in questions:
                if question["group_id"] == group_id:
                    question["canonical_overlap"] = "YES"
                    question["canonical_question_matched"] = best_canonical["Canonical question"]
                    question["similarity_score"] = best_score

            overlap_rows.append(
                {
                    "group_representative": rep_q["group_representative"],
                    "group_count": rep_q["group_count"],
                    "canonical_question": best_canonical["Canonical question"],
                    "canonical_conversation_count": best_canonical.get("Conversation count", ""),
                    "similarity_score": best_score,
                }
            )
        else:
            for question in questions:
                if question["group_id"] == group_id:
                    question["canonical_overlap"] = ""
                    question["canonical_question_matched"] = ""
                    question["similarity_score"] = 0

    return overlap_rows


def main() -> None:
    args = parse_args()

    base_url = build_base_url(args.tag_id, args.tag)
    os.makedirs(args.output_dir, exist_ok=True)

    start = time.time()
    page1_questions = smoke_test(base_url, args.tag)
    if args.smoke_test:
        return

    total_pages = detect_total_pages(base_url)
    all_questions = scrape_all_pages(base_url, total_pages, page1_questions)
    all_questions = verify_scraped_data(all_questions, args.min_rows)

    raw_path = os.path.join(args.output_dir, f"{args.tag}_qa_raw.csv")
    write_raw_csv(all_questions, raw_path)

    all_questions = group_questions(all_questions, args.tag, args.group_threshold)

    overlap_rows = []
    if args.canonical:
        canonical = load_canonical(args.canonical)
        overlap_rows = match_canonical(all_questions, canonical, args.tag, args.canonical_threshold)

    questions_path = os.path.join(args.output_dir, f"{args.tag}_qa_questions.csv")
    write_questions_csv(all_questions, questions_path)

    if args.canonical and overlap_rows:
        overlap_path = os.path.join(args.output_dir, f"{args.tag}_qa_overlap.csv")
        write_overlap_csv(overlap_rows, overlap_path)

    unique_path = os.path.join(args.output_dir, f"{args.tag}_qa_unique_questions.csv")
    write_unique_csv(all_questions, unique_path, fetch_summaries=args.fetch_summaries)

    elapsed = time.time() - start
    print(f"Done in {elapsed:.0f}s")
    print(f"Raw dump: {raw_path}")
    print(f"Grouped questions: {questions_path}")
    if args.canonical:
        print(f"Canonical overlap: {os.path.join(args.output_dir, f'{args.tag}_qa_overlap.csv')}")
    print(f"Unique questions: {unique_path}")


if __name__ == "__main__":
    main()