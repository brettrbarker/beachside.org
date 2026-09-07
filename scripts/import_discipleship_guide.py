#!/usr/bin/env python3

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse
import unicodedata


DAY_ORDER = ["monday", "tuesday", "wednesday", "thursday", "friday"]


def yaml_quote(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ")


def slugify(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    ascii_value = normalized.encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", ascii_value.lower()).strip("-")
    return slug or "discipleship-guide"


def build_output_slug(title: str, series: str | None = None) -> str:
    title_slug = slugify(title)
    if not series:
        return title_slug
    series_slug = slugify(series)
    if not series_slug:
        return title_slug
    return f"{series_slug}--{title_slug}"


def parse_date(value: Any) -> str:
    if not value:
        return datetime.now().strftime("%Y-%m-%dT09:00:00-05:00")
    if isinstance(value, str):
        value = value.strip()
        if not value:
            return datetime.now().strftime("%Y-%m-%dT09:00:00-05:00")
        if "T" in value or value.endswith("Z"):
            try:
                dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
                return dt.isoformat()
            except ValueError:
                pass
        try:
            dt = datetime.strptime(value, "%Y-%m-%d")
            return dt.strftime("%Y-%m-%dT09:00:00-05:00")
        except ValueError:
            pass
    return datetime.now().strftime("%Y-%m-%dT09:00:00-05:00")


def build_video_embed(url: str) -> str:
    if not url:
        return ""
    if "youtube.com/embed/" in url or "youtube-nocookie.com/embed/" in url:
        return url
    if "youtu.be/" in url:
        parsed = urlparse(url)
        video_id = parsed.path.strip("/").split("/")[-1]
        if video_id:
            return f"https://www.youtube.com/embed/{video_id}"
    parsed = urlparse(url)
    if "youtube.com" in parsed.netloc:
        video_id = parse_qs(parsed.query).get("v", [""])[0]
        if video_id:
            return f"https://www.youtube.com/embed/{video_id}"
    return ""


def render_questions(questions: list[dict[str, Any]]) -> list[str]:
    html_parts: list[str] = []
    for index, item in enumerate(questions or [], start=1):
        question = str(item.get("question", "")).strip()
        scripture = str(item.get("question_scripture", "")).strip()
        if not question:
            continue
        scripture_html = f'<div class="dg-q-scripture">{scripture}</div>' if scripture else ""
        html_parts.append(
            '    <li>\n'
            f'      <div class="dg-q-num">{index}</div>\n'
            f'      <div class="dg-q-body">{question}{scripture_html}</div>\n'
            '    </li>'
        )
    return html_parts


def render_devotions(devotions: dict[str, Any]) -> str:
    tab_buttons: list[str] = []
    panels: list[str] = []
    for index, day in enumerate(DAY_ORDER):
        entry = (devotions or {}).get(day, {}) if isinstance(devotions, dict) else {}
        scripture = str(entry.get("scripture", "")).strip()
        reflection = str(entry.get("reflection", "")).strip()
        if not scripture and not reflection:
            continue
        active = " active" if index == 0 else ""
        tab_buttons.append(
            f'    <button class="dg-devo-tab{active}" data-day="{day}">{day.title()}</button>'
        )
        panels.append(
            f'    <section class="dg-devo-panel{active}" id="devo-{day}">\n'
            f'      <a class="dg-devo-scripture-pill" href="https://www.bible.com/" target="_blank" rel="noopener">📖 {scripture or "Scripture reference"}</a>\n'
            f'      <div class="dg-prose">{reflection or "<p>Add reflection.</p>"}</div>\n'
            '    </section>'
        )
    if not tab_buttons:
        return ""
    return (
        '  <div class="dg-devo-tabs" role="tablist" aria-label="Daily devotions">\n'
        + "\n".join(tab_buttons)
        + '\n  </div>\n'
        + '  <div class="dg-devo-panels">\n'
        + "\n".join(panels)
        + '\n  </div>'
    )


def render_prayer_prompts(items: list[dict[str, Any]]) -> list[str]:
    lines: list[str] = []
    for item in items or []:
        prompt = str(item.get("prompt", "")).strip()
        if not prompt:
            continue
        lines.append(f'    <li><div class="dg-prayer-dot"></div><span>{prompt}</span></li>')
    return lines


def render_next_steps(items: list[dict[str, Any]]) -> list[str]:
    lines: list[str] = []
    for item in items or []:
        step = str(item.get("step", "")).strip()
        if not step:
            continue
        lines.append(f'    <li><div class="dg-step-chip">→</div><span>{step}</span></li>')
    return lines


def render_resources(items: list[dict[str, Any]]) -> list[str]:
    lines: list[str] = []
    for item in items or []:
        title = str(item.get("title", "")).strip()
        url = str(item.get("url", "")).strip()
        description = str(item.get("description", "")).strip()
        if not title:
            continue
        href = f' href="{url}" target="_blank" rel="noopener"' if url else ""
        lines.append(
            '  <div class="dg-resource">\n'
            '    <div class="dg-resource-bar"></div>\n'
            '    <div>\n'
            f'      <div class="dg-resource-name"><a{href}>{title}</a></div>\n'
            f'      <div class="dg-resource-desc">{description}</div>\n'
            '    </div>\n'
            '  </div>'
        )
    return lines


def render_doc(payload: dict[str, Any]) -> str:
    fields = payload.get("fields", {}) if isinstance(payload, dict) else {}
    title = str(payload.get("title") or fields.get("message_title") or "Untitled Guide").strip()
    guide_date = str(fields.get("guide_date") or payload.get("date") or "").strip()
    youtube_url = str(fields.get("youtube_link") or "").strip()
    main_idea = str(fields.get("main_idea") or "").strip()
    description = str(fields.get("description") or main_idea or title).strip()
    series = str(fields.get("series") or "").strip()
    speaker = str(fields.get("speaker") or "").strip()

    message_recap = str(fields.get("message_recap") or "").strip()
    discussion_questions = fields.get("discussion_questions") or []
    daily_devotions = fields.get("daily_devotions") or {}
    spiritual_practice = str(fields.get("spiritual_practice") or "").strip()
    prayer_prompts = fields.get("prayer_prompts") or []
    next_steps = fields.get("next_steps") or []
    resources = fields.get("resources") or []

    embed = build_video_embed(youtube_url)
    if embed:
        video_block = (
            '  <section class="dg-card dg-card--flush">\n'
            '    <div class="dg-video">\n'
            f'      <iframe src="{embed}" allowfullscreen allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"></iframe>\n'
            '    </div>\n'
            '  </section>'
        )
    else:
        video_block = ""

    front_matter_lines = [
        "---",
        f'title: "{yaml_quote(title)}"',
        f'date: {parse_date(guide_date)}',
        f'speaker: "{yaml_quote(speaker)}"',
    ]
    if series:
        front_matter_lines.append(f'series: "{yaml_quote(series)}"')
    front_matter_lines.extend([
        f'description: "{yaml_quote(description)}"',
        'draft: true',
        '---',
        '',
    ])

    discussion_items = render_questions(discussion_questions)
    discussion_block = (
        '  <section class="dg-card">\n'
        '    <h2 class="dg-label">Group Discussion Questions</h2>\n'
        '    <ol class="dg-q-list">\n'
        + ("\n".join(discussion_items) if discussion_items else '      <li><div class="dg-q-num">1</div><div class="dg-q-body">Add a discussion question.</div></li>') + '\n'
        '    </ol>\n'
        '  </section>'
    )

    devotion_html = render_devotions(daily_devotions)
    devotion_block = (
        '  <section class="dg-card dg-card--devo">\n'
        '    <h2 class="dg-label">Daily Devotions</h2>\n'
        f'{devotion_html}\n'
        '  </section>'
    ) if devotion_html else ""

    prayer_lines = render_prayer_prompts(prayer_prompts)
    prayer_block = (
        '  <section class="dg-card">\n'
        '    <h2 class="dg-label">Prayer Prompts</h2>\n'
        '    <ul class="dg-prayer-list">\n'
        + ("\n".join(prayer_lines) if prayer_lines else '      <li><div class="dg-prayer-dot"></div><span>Add a prayer prompt.</span></li>') + '\n'
        '    </ul>\n'
        '  </section>'
    ) if prayer_lines or True else ""

    next_steps_lines = render_next_steps(next_steps)
    next_steps_block = (
        '  <section class="dg-card--teal">\n'
        '    <h2 class="dg-label">Next Steps</h2>\n'
        '    <ul class="dg-steps-list">\n'
        + ("\n".join(next_steps_lines) if next_steps_lines else '      <li><div class="dg-step-chip">→</div><span>Add a concrete next step.</span></li>') + '\n'
        '    </ul>\n'
        '  </section>'
    ) if next_steps_lines or True else ""

    resource_lines = render_resources(resources)
    resources_block = (
        '  <section class="dg-card">\n'
        '    <h2 class="dg-label">Resources</h2>\n'
        + ("\n".join(resource_lines) if resource_lines else '    <div class="dg-resource"><div class="dg-resource-bar"></div><div><div class="dg-resource-name"><a href="https://example.org/">Resource name</a></div><div class="dg-resource-desc">Describe why this resource is helpful.</div></div></div>') + '\n'
        '  </section>'
    ) if resource_lines or True else ""

    spiritual_block = (
        '  <section class="dg-card">\n'
        '    <h2 class="dg-label">Spiritual Practice</h2>\n'
        f'    <div class="dg-practice-inner dg-prose">{spiritual_practice or "<p><strong>Practice:</strong> Add the weekly practice here.</p>"}</div>\n'
        '  </section>'
    ) if spiritual_practice or True else ""

    body = '\n'.join([
        '<div class="dg-wrap">',
        '',
        video_block,
        '',
        '  <section class="dg-card">',
        '    <h2 class="dg-label">Message Recap</h2>',
        '    <div class="dg-prose">',
        f'{message_recap or "<p>Add the message recap here.</p>"}',
        '    </div>',
        '  </section>',
        '',
        '  <aside class="dg-big-idea">',
        '    <div class="dg-big-idea-label">Main Idea</div>',
        f'    <blockquote>{main_idea or "Add the guide\'s main idea here."}</blockquote>',
        '  </aside>',
        '',
        discussion_block,
        '',
        devotion_block,
        '',
        spiritual_block,
        '',
        prayer_block,
        '',
        next_steps_block,
        '',
        resources_block,
        '',
        '</div>',
    ])

    return "\n".join(front_matter_lines) + "\n" + body + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Import a discipleship guide JSON payload into a Hugo markdown file.")
    parser.add_argument("--input", required=True, help="Path to the JSON file, or '-' to read from stdin.")
    parser.add_argument("--output-dir", default="content/discipleship-guide", help="Directory where the generated file should be written.")
    parser.add_argument("--force", action="store_true", help="Overwrite an existing file if one already exists.")
    parser.add_argument("--stdout", action="store_true", help="Print the generated file to stdout instead of writing it to disk.")
    args = parser.parse_args()

    if args.input == "-":
        payload = json.load(sys.stdin)
    else:
        input_path = Path(args.input)
        if not input_path.exists():
            print(f"Input file not found: {input_path}", file=sys.stderr)
            return 1
        with input_path.open("r", encoding="utf-8") as fh:
            payload = json.load(fh)

    rendered = render_doc(payload)
    title = str((payload.get("title") or payload.get("fields", {}).get("message_title") or "discipleship-guide")).strip()
    series = str((payload.get("series") or (payload.get("fields", {}) or {}).get("series") or "")).strip()
    slug = build_output_slug(title, series)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{slug}.md"

    if args.stdout:
        print(rendered)
        return 0

    if output_path.exists() and not args.force:
        print(f"File already exists: {output_path}. Use --force to overwrite it.", file=sys.stderr)
        return 1

    output_path.write_text(rendered, encoding="utf-8")
    print(f"Wrote {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
