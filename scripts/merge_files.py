import os

def merge_markdown_files(md_folder, output_file, file_order=None, key_func=None, page_break=None):
    """
    Merges multiple Markdown files into a single file.

    Args:
        md_folder (str): Path to the folder containing the .md files
        output_file (str): Path of the output merged markdown file
        file_order (list, optional): List of file names to enfoce merging order
        key_func (callable, optional): sorting function (returns a key from a file name)
        page_break: None | 'openxml' | 'marker' | 'formfeed'
        - 'openxml' : insert a raw openxml fenced block (works for docx)
        - 'marker'  : inserts the literal '\newpage' (requires a pandoc filter to be effective for docx)
        - 'formfeed': inserts a literal form-feed character '\f'
    """
    all_files = [f for f in os.listdir(md_folder) if f.endswith(".md")]

    if file_order is not None:
        files = file_order
    else:
        if key_func is not None:
            files = sorted(all_files, key=key_func)
        else:
            files = sorted(all_files)

    merged_lines = []

    for md_file in files:
        path = os.path.join(md_folder, md_file)
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        merged_lines.append(f"\n<!-- START OF {md_file} -->\n\n")
        merged_lines.extend(lines)
        merged_lines.append(f"\n<!-- END OF {md_file} -->\n\n")
        
        if page_break == 'openxml':
            merged_lines.append(
                '\n```{=openxml}\n<w:p><w:r><w:br w:type="page"/></w:r></w:p>\n```\n\n'
            )
        elif page_break == 'marker':
            merged_lines.append("\n\\newpage\n\n")
        elif page_break == 'formfeed':
            merged_lines.append("\n\f\n\n")

        print(f"[Merge] merging {md_file} ..")

    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(merged_lines)

    print(f"[Merge] {len(files)} files merged into {output_file}")
