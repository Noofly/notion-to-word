from scripts import *
from pathlib import Path

################# CONFIG #################

table_style_name = "Style1"
notion_export_folder = Path("ressources/notion_export")
template_path = Path("ressources/template.dotx")
input_md_file = "example.md"
utf_8_md_file = "example_utf8.md"
table_cleaned_md_file = "example_table_cleaned.md"
table_image_cleaned_md_file = "example_table_image_cleaned.md"
pandoc_file = "result_uncleared.docx"
final_file = "result.docx"

##########################################

convert_markdown_to_utf8(str(notion_export_folder/input_md_file), str(notion_export_folder/utf_8_md_file))
clean_markdown_tables(str(notion_export_folder/input_md_file), str(notion_export_folder/table_cleaned_md_file))
clean_image_lines(str(notion_export_folder/table_cleaned_md_file), str(notion_export_folder/table_image_cleaned_md_file))
create_pandoc_docx(str(notion_export_folder/table_image_cleaned_md_file), str(notion_export_folder/pandoc_file), str(template_path))
apply_table_style(str(notion_export_folder/pandoc_file), final_file, table_style_name)




