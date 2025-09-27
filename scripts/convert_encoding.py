import shutil

def convert_markdown_to_utf8(input_file: str, output_file: str = None):
    """
    Converts a Markdown file to UTF-8 encoding.

    Args:
        input_file: Path to the input Markdown file
        output_file: Path to save the UTF-8 encoded file. 
            If None, it overwrites the original file.
    """
    if output_file is None:
        output_file = input_file

    # Try to detect the original encoding
    import chardet
    with open(input_file, 'rb') as f:
        raw_data = f.read()
        detected = chardet.detect(raw_data)
        encoding = detected['encoding'] or 'utf-8'
    
    print(f"Encoding detected : {encoding}")
    if encoding.lower().replace("-", "") == 'utf8':
        print("File is already encoded as utf-8")
        if output_file is not None:
            print(f"Copying {input_file} to {output_file}")
            shutil.copy(input_file, output_file)
        return

    # Read and decode
    text = raw_data.decode(encoding, errors='replace')

    # Write as UTF-8
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(text)

    print(f"File '{input_file}' converted to UTF-8 and saved as '{output_file}'")


if __name__ == '__main__':
    convert_markdown_to_utf8("ressources/notion_export/example.md", "ressources/notion_export/example_utf8.md")