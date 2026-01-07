#!/usr/bin/env python3
"""Build script for BSRG website. Generates index.html from template and topics.json."""

import json
from pathlib import Path

SESSION_DETAIL = """
<details{open_attr}>
  <summary>
    <span class="summary-date">{date_formatted}</span>
    <strong>{title}</strong>
  </summary>
  <p>{description}</p>{note}
  {link_groups}
</details>
""".strip()


def generate_link_groups_html(link_groups: list[dict]) -> str:
    """Generate HTML for link groups."""
    groups_html = []
    for group in link_groups:
        links_html = "\n".join(
            f'      <li><a href="{link["url"]}">{link["text"]}</a></li>'
            for link in group["links"]
        )
        group_html = f"""  <div class="link-group">
    <h4>{group["title"]}</h4>
    <ul>
{links_html}
    </ul>
  </div>"""
        groups_html.append(group_html)
    return "\n\n".join(groups_html)


def generate_topic_html(topic: dict) -> str:
    """Generate HTML for a single topic."""
    open_attr = " open" if topic.get("current") else ""
    date = topic.get("date", "")

    link_groups = topic.get("linkGroups", [])
    link_groups_html = generate_link_groups_html(link_groups)

    note = topic.get("note")
    note_html = f"\n  <p><em>Note: {note}</em></p>" if note else ""

    return SESSION_DETAIL.format(
        open_attr=open_attr,
        date_formatted=date,
        title=topic["title"],
        description=topic["description"],
        note=note_html,
        link_groups=link_groups_html,
    )


def build():
    """Main build function."""
    root = Path(__file__).parent

    # Load data
    with open(root / "topics.json") as f:
        topics = json.load(f)

    with open(root / "template.html") as f:
        template = f.read()

    # Generate topics HTML with <hr> separators (skip hidden topics)
    topics_html_parts = []
    for topic in topics:
        if topic.get("hidden"):
            continue
        topics_html_parts.append("<hr>")
        topics_html_parts.append(generate_topic_html(topic))
    topics_html_parts.append("<hr>")

    topics_html = "\n\n".join(topics_html_parts)

    # Replace placeholder and write output
    output = template.replace("<!-- TOPICS -->", topics_html)

    with open(root / "index.html", "w") as f:
        f.write(output)

    print(f"Built index.html with {len(topics)} topics")


if __name__ == "__main__":
    build()
