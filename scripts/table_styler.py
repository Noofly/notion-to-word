from docx import Document

def apply_table_style(input_file, output_file, table_style_name):
    """
    Apply a style to all tables in a Word document.
    
    Args:
        input_file (str): Path to the input Word document.
        output_file (str): Path where the styled document will be saved.
        table_style_name (str): Name of the table style to apply.
    """
    doc = Document(input_file)

    for table in doc.tables:
        table.style = table_style_name

    doc.save(output_file)
    print(f"All tables now have the style '{table_style_name}' in : {output_file}")


if __name__ == '__main__':
    apply_table_style("example.docx", "example_styled.docx", "Style1")