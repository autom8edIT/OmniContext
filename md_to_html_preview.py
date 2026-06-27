#!/usr/bin/env python3
"""
Convert the workshop analysis Markdown to a self-contained, nicely styled HTML
that looks like a clean full-screen Markdown preview (similar to VS Code / GitHub rendered view).

The resulting .html opens in its own browser window and looks polished and readable full-screen.
"""

import markdown
from markdown.extensions.tables import TableExtension
import os
from datetime import datetime

def md_to_html(md_path: str, html_path: str):
    with open(md_path, "r", encoding="utf-8") as f:
        md_text = f.read()

    # Convert Markdown to HTML with useful extensions
    html_body = markdown.markdown(
        md_text,
        extensions=[
            TableExtension(),
            "fenced_code",
            "sane_lists",
            "attr_list",
        ],
        output_format="html5",
    )

    # CSS that tries to match VS Code Markdown Preview as closely as possible (light theme)
    # More visual weight than plain white - better hierarchy, table, spacing
    css = """
:root {
  --font: "Segoe UI", -apple-system, BlinkMacSystemFont, "Helvetica Neue", Arial, sans-serif;
  --font-size: 14px;
  --text: #cccccc;           /* soft light gray text - low contrast */
  --bg: #1e1e1e;             /* VS Code dark editor background */
  --content-bg: #252526;     /* slightly lighter card */
  --link: #4fc1ff;           /* typical VS Code blue */
  --border: #3c3c3c;
  --heading: #e0e0e0;
  --table-header: #2d2d2d;
}

body {
  font-family: var(--font);
  font-size: var(--font-size);
  line-height: 1.65;
  color: var(--text);
  background: var(--bg);
  margin: 0;
  padding: 0;
}

/* Content "window" like VS Code dark preview pane - low brightness */
.markdown-body {
  max-width: 1100px;
  margin: 20px auto;
  padding: 30px 40px;
  background: var(--content-bg);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
  border: 1px solid var(--border);
  border-radius: 6px;
}

@media (max-width: 900px) {
  .markdown-body {
    margin: 10px;
    padding: 20px;
    box-shadow: none;
    border: none;
  }
}

h1, h2, h3, h4, h5, h6 {
  font-weight: 600;
  line-height: 1.25;
  color: var(--heading);
  margin-top: 1.6em;
  margin-bottom: 0.5em;
}

h1 {
  font-size: 1.9em;
  border-bottom: 1px solid var(--border);
  padding-bottom: 0.3em;
}

h2 {
  font-size: 1.45em;
  border-bottom: 1px solid var(--border);
  padding-bottom: 0.2em;
}

h3 { font-size: 1.2em; }

p, blockquote, ul, ol, dl, table, pre {
  margin-top: 0;
  margin-bottom: 14px;
}

ul, ol {
  padding-left: 1.8em;
}

li {
  margin-bottom: 0.2em;
}

blockquote {
  margin: 0 0 14px 0;
  padding: 0 1em;
  color: #a0a0a0;
  border-left: 0.25em solid #4a4a4a;
  background: #2a2a2a;
}

table {
  border-collapse: collapse;
  width: 100%;
  margin: 14px 0;
  font-size: 13.5px;
}

table th,
table td {
  border: 1px solid #d0d7de;
  padding: 6px 12px;
  text-align: left;
}

table th {
  font-weight: 600;
  background-color: var(--table-header);
}

table tr:nth-child(2n) {
  background-color: #2a2a2a;
}

code {
  font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
  background: #1f1f1f;
  padding: 2px 5px;
  border-radius: 3px;
  font-size: 0.92em;
}

pre {
  font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
  background: #1a1a1a;
  padding: 12px 14px;
  overflow: auto;
  font-size: 13px;
  line-height: 1.4;
  border-radius: 3px;
  border: 1px solid var(--border);
}

pre code {
  background: none;
  padding: 0;
  border-radius: 0;
}

strong {
  font-weight: 600;
  color: #e0e0e0;
}

a {
  color: var(--link);
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}

hr {
  border: none;
  border-top: 1px solid var(--border);
  margin: 18px 0;
}

/* Full screen friendly */
@media screen and (min-width: 1200px) {
  .markdown-body {
    max-width: 1280px;
    padding: 35px 50px;
    font-size: 15px;
  }
}


"""

    # Full HTML document
    html = f"""<!DOCTYPE html>
<html lang="sv">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Workshop: Sammanställda case + analys (Case 1–7 + Steg 4)</title>
  <style>
{css}
  </style>
</head>
<body>

<div class="markdown-body">

{html_body}

</div>

<footer style="max-width: 1280px; margin: 30px auto 40px; padding: 15px 40px; font-size: 12px; color: #666; text-align: center;">
  Genererad {datetime.now().strftime('%Y-%m-%d %H:%M')} • Öppna i webbläsare (F11 för fullskärm) • VS Code Markdown Preview-stil
</footer>

</body>
</html>"""

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Created nice preview HTML: {html_path}")
    print("Open it in your browser (double-click the .html) for a full-screen rendered preview look.")
    return html_path


if __name__ == "__main__":
    base = os.path.dirname(os.path.abspath(__file__)) or "."
    md_file = os.path.join(base, "workshop_8_dokument_analys_sammanslagen.md")
    html_file = os.path.join(base, "workshop_8_dokument_analys_sammanslagen.html")

    if not os.path.exists(md_file):
        print("ERROR: Markdown file not found.")
    else:
        md_to_html(md_file, html_file)