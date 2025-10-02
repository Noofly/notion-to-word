import re
import os
import unicodedata
from urllib.parse import unquote
from pathlib import Path



def normalize_anchor(text: str) -> str:
    """
    Transforms a title into a Pandoc/Word compatible slug 
    """
    #process accents ("é"/"è") and special characters of the french language("ç")
    text = unicodedata.normalize('NFKD', text) 
    text = "".join(c for c in text if not unicodedata.combining(c))
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'\s+', '-', text)
    return text.strip('-')

def ensure_title(md_file) -> str:
    """
    Make sure the .md file starts with a title.
    Returns the title (either found or created).
    """
    with open(md_file, "r+", encoding="utf-8") as f:
        lines = f.readlines()
        if lines and lines[0].startswith("#"):
            title = lines[0].lstrip("#").strip()
        else:
            # Fallback on filename (removing trailing hash-like strings)
            title = re.sub(r'\s*\w{32,}\s*$', '', md_file.stem)
            lines.insert(0, f"# {title}\n")
            f.seek(0)
            f.truncate()
            f.writelines(lines)
    return title

def build_title_mapping(md_folder):
    """
    Parse all .md files to create a mapping :
    filename -> anchor based on the main title (# Title)
    """
    mapping = {}
    for md_file in md_folder.glob("*.md"):
        #create mapping object
        title = ensure_title(md_file)
        anchor = normalize_anchor(title)
        mapping[md_file.name] = anchor

        #Update file to ensure a robust anchoring system
        lines = Path(md_file).read_text(encoding='utf-8').splitlines()
        first_line = lines[0]
        first_line = re.sub(r"\s*\{#.*?\}\s*$", "", first_line)
        lines[0] = f"{first_line} {{#{anchor}}}"

        Path(md_file).write_text("\n".join(lines), encoding='utf-8')

    return mapping

def convert_links_using_mapping(input_file, mapping, output_file = None):
    """
    Converts Notion links [Title](File.md) into mapping-based internal links
    """
    if output_file is None:
        output_file = input_file

    pattern = re.compile(r'\[([^\]]+)\]\(([^\)]+\.md)\)')

    with open(input_file, 'r', encoding='utf-8') as f:
        text = f.read()

    def replacer(match):
        label = match.group(1)
        target = os.path.basename(match.group(2))
        target = unquote(target)
        if target in mapping:
            print(f"[Links] Found a link : {target}")
            anchor = mapping[target]
            return f"[{label}](#{anchor})"
        else:
            print(f"[Links] No mapping for {target}, leaving as is")
            return match.group(0)

    new_text = pattern.sub(replacer, text)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(new_text)
    print(f"[Links] Internal links converted using title mapping -> {output_file}")

if __name__ == '__main__':
    md_folder = "ressources/notion_export"
    mapping = build_title_mapping(md_folder)
    print(mapping)
    convert_links_using_mapping("example.md", mapping, "example_clean_links.md")
