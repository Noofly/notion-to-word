from scripts import *
from pathlib import Path
import re

################# CONFIG #################

table_style_name = "Style1"
notion_export_folder = Path("ressources/notion_export")
template_path = Path("ressources/template.dotx")
input_md_file = "example.md"
utf_8_md_file = "example_utf8.md"
table_cleaned_md_file = "example_table_cleaned.md"
table_image_cleaned_md_file = "example_table_image_cleaned.md"
merged_file = "merged.md"
pandoc_file = "result_uncleared.docx"
final_file = "result.docx"

##########################################
def example_custom_key(filename: str):
    """
    Ordering :
    1. File named "First Position File"
    2. File names starting with a number (ascending)
    3. Remaining files (alphabetical order)
    """
    name = filename.lower()

    if name.startswith("first position"):
        return (0, name)
    elif re.match(r"^\d+", name):
        number = int(re.match(r"^\d+", name).group())
        return (1, number)
    else:
        return (2, name)

def run_on_folder(folder):
    mapping = build_title_mapping(folder)
    print(mapping)

    for md_file in folder.glob("*.md"):
        print(f"File \"{md_file}\" :")
        convert_markdown_to_utf8(str(md_file))
        clean_markdown_tables(str(md_file))
        clean_image_lines(str(md_file))
        convert_links_using_mapping(str(md_file), mapping)

    
    merge_markdown_files(folder, str(folder/merged_file), key_func=example_custom_key, page_break='openxml')
    create_pandoc_docx(str(folder/merged_file), str(folder/pandoc_file), str(template_path))
    apply_table_style(str(folder/pandoc_file), table_style_name, final_file)

def example_run():
    convert_markdown_to_utf8(str(notion_export_folder/input_md_file), str(notion_export_folder/utf_8_md_file))
    clean_markdown_tables(str(notion_export_folder/utf_8_md_file), str(notion_export_folder/table_cleaned_md_file))
    clean_image_lines(str(notion_export_folder/table_cleaned_md_file), str(notion_export_folder/table_image_cleaned_md_file))
    create_pandoc_docx(str(notion_export_folder/table_image_cleaned_md_file), str(notion_export_folder/pandoc_file), str(template_path))
    apply_table_style(str(notion_export_folder/pandoc_file), table_style_name, final_file)


if __name__ == '__main__':
    run_on_folder(notion_export_folder)


