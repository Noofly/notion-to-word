import re

def clean_image_lines(input_file, output_file : str = None):
    """
    Removes all textual traces of Notion images
    
    Args:
        input_file : path of the source Markdown file
        output_file : path of the cleaned Markdown file 
            If None, it overwrites the original file.
    """
    if output_file is None:
        output_file = input_file

    pattern = re.compile(r'!\[.*?\]\(([^)]+)\)', re.IGNORECASE)

    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    cleaned_lines = []
    for line in lines:
        # Remplace le contenu des crochets par vide, conserve les parenthèses
        new_line = pattern.sub(r'![](\1)', line)
        cleaned_lines.append(new_line)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(cleaned_lines)


if __name__ == '__main__':
    clean_image_lines("ressources/notion_export/example.md", "ressources/notion_export/example_images_cleaned.md")