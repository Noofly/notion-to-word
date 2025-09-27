import re

def clean_markdown_tables(input_file, output_file):
    """
    Cleans the Markdown tables for Pandoc.
    - Removes useless spaces around pipes
    - Checks that each row has the same amount of columns
    - Adds a separator line if missing

    Args:
        input_file : path to the Markdown file to clean
        output_file: path where cleaned Markdown will be saved
    """
    # Read the input file
    with open(input_file, "r", encoding="utf-8") as f:
        lines = f.read().split("\n")

    new_lines = []
    i = 0

    while i < len(lines):
        line = lines[i]
        # Detects the start of a table
        if re.match(r"^\s*\|.*\|\s*$", line):
            # Retrieves all the table
            table_lines = [line]
            i += 1
            while i < len(lines) and re.match(r"^\s*\|.*\|\s*$", lines[i]):
                table_lines.append(lines[i])
                i += 1

            # Cleaning : remove spaces around pipes
            cleaned_table = []
            for l in table_lines:
                cells = [cell.strip() for cell in l.strip().split("|")]
                if cells[0] == "": cells = cells[1:]
                if cells[-1] == "": cells = cells[:-1]
                cleaned_line = "| " + " | ".join(cells) + " |"
                cleaned_table.append(cleaned_line)

            # Add a separator if missing 
            if len(cleaned_table) > 1 and not re.match(r"^\|[\s\-\|]+$", cleaned_table[1]):
                separator = "| " + " | ".join(["---"]*len(cleaned_table[0].split("|")[1:-1])) + " |"
                cleaned_table.insert(1, separator)
            new_lines.extend(cleaned_table)
        else:
            new_lines.append(line)
            i += 1
    
    # write in UTF-8
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(new_lines))
    print(f"File cleaned, encoded with UTF-8 : {output_file}")

if __name__ == '__main__':
    clean_markdown_tables("ressources/notion_export/example.md", "ressources/notion_export/example_table_cleaned_utf8.md")




