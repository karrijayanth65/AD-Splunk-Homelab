"""Offline documentation checks; no Windows or Splunk execution is performed."""
from pathlib import Path
from urllib.parse import unquote, urlsplit
import configparser
import json
import re
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]


def heading_ids(text):
    """Approximate GitHub slugs for the simple headings used in this project."""
    counts = {}
    ids = set()
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    for title in re.findall(r"^#{1,6}\s+(.+)$", text, re.M):
        slug = re.sub(r"[^\w\- ]", "", title.lower()).replace(" ", "-")
        count = counts.get(slug, 0)
        counts[slug] = count + 1
        ids.add(slug + (f"-{count}" if count else ""))
    return ids


def check():
    errors = []
    files = [p for p in ROOT.rglob("*") if p.is_file() and ".git" not in p.parts]
    exact = {p.relative_to(ROOT).as_posix() for p in files}
    markdown = [p for p in files if p.suffix == ".md"]
    links = images = 0
    for path in markdown:
        text = path.read_text(encoding="utf-8")
        if len(re.findall(r"^# ", text, re.M)) != 1:
            errors.append(f"Expected one title: {path.relative_to(ROOT)}")
        body = re.sub(r"```.*?```", "", text, flags=re.S)
        for embedded, href in re.findall(r"(!?)\[[^\]]*\]\(([^)]+)\)", body):
            parsed = urlsplit(href)
            if parsed.scheme or parsed.netloc:
                continue
            links += 1
            images += bool(embedded)
            dest = (path.parent / unquote(parsed.path)).resolve() if parsed.path else path
            try:
                relative = dest.relative_to(ROOT).as_posix()
            except ValueError:
                errors.append(f"Path escapes project: {path.name}: {href}")
                continue
            if relative not in exact:
                errors.append(f"Missing or case-mismatched path: {path.name}: {href}")
            elif parsed.fragment and dest.suffix == ".md":
                if unquote(parsed.fragment) not in heading_ids(dest.read_text(encoding="utf-8")):
                    errors.append(f"Missing heading anchor: {path.name}: {href}")
    diagrams = [p for p in files if p.suffix == ".svg"]
    for path in diagrams:
        try:
            root = ET.parse(path).getroot()
            if root.tag != "{http://www.w3.org/2000/svg}svg":
                errors.append(f"Not an SVG: {path.name}")
            if root.find("{http://www.w3.org/2000/svg}title") is None:
                errors.append(f"SVG lacks accessible title: {path.name}")
        except ET.ParseError as exc:
            errors.append(f"Invalid SVG: {path.name}: {exc}")
    for filename in ("inputs.conf.example", "outputs.conf.example"):
        parser = configparser.ConfigParser(interpolation=None)
        parser.read(ROOT / "configs" / "splunk" / filename, encoding="utf-8")
        if filename.startswith("inputs"):
            for channel in ("Security", "System", "Microsoft-Windows-Sysmon/Operational"):
                section = f"WinEventLog://{channel}"
                if not parser.has_section(section) or parser.get(section, "index", fallback="") != "endpoint":
                    errors.append(f"Missing endpoint input: {channel}")
                if parser.get(section, "renderXml", fallback="").lower() != "true":
                    errors.append(f"XML rendering not enabled: {channel}")
        elif parser.get("tcpout:lab_receiver", "server", fallback="") != "192.168.10.10:9997":
            errors.append("Collector destination differs from address plan")
    result = {"files": len(files), "markdown": len(markdown), "local_links": links,
              "image_embeds": images, "svg_diagrams": len(diagrams), "errors": errors,
              "live_lab_validation": "not performed by this checker"}
    print(json.dumps(result, indent=2))
    return bool(errors)


if __name__ == "__main__":
    sys.exit(check())
