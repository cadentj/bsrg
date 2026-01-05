#!/usr/bin/env python3
"""Build script for BSRG website. Generates index.html from template and topics.json."""

import json
from datetime import datetime
from pathlib import Path


def format_date(date_str: str) -> str:
    """Convert 2025-01-11 to Jan 2025."""
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    return dt.strftime("%b %Y")


SESSION_DETAIL = """
<details{open_attr}>
  <summary>
    <span class="summary-date">{date_formatted}</span>
    <strong>{title}</strong>
  </summary>
  <p>{description}</p>
  <ul>
    {links}
  </ul>
</details>
""".strip()


def generate_topic_html(topic: dict) -> str:
    """Generate HTML for a single topic."""
    open_attr = " open" if topic.get("current") else ""
    date_formatted = format_date(topic["date"])

    links_html = "\n".join(
        f'      <li><a href="{link["url"]}">{link["text"]}</a></li>'
        for link in topic["links"]
    )

    return SESSION_DETAIL.format(
        open_attr=open_attr,
        date_formatted=date_formatted,
        title=topic["title"],
        description=topic["description"],
        links=links_html,
    )


def build():
    """Main build function."""
    root = Path(__file__).parent

    # Load data
    with open(root / "topics.json") as f:
        topics = json.load(f)

    with open(root / "template.html") as f:
        template = f.read()

    # Generate topics HTML with <hr> separators
    topics_html_parts = []
    for topic in topics:
        topics_html_parts.append("<hr>")
        topics_html_parts.append(generate_topic_html(topic))

    topics_html = "\n\n".join(topics_html_parts)

    # Replace placeholder and write output
    output = template.replace("<!-- TOPICS -->", topics_html)

    with open(root / "index.html", "w") as f:
        f.write(output)

    print(f"Built index.html with {len(topics)} topics")


if __name__ == "__main__":
    build()
