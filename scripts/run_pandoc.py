import subprocess
from pathlib import Path

def create_pandoc_docx(input_md, output_docx, template):
    """
    Calls Pandoc to convert Markdown into Word (.docx)
    
    Args:
        input_md : path to the Markdown file
        output_docx : path to the output Word file
        template : path to the .dotx file to use as a template
    """
    input_path = Path(input_md)
    output_path = Path(output_docx).resolve()
    template_path = Path(template)

    cmd = [
        "pandoc",
        input_path.name,
        "-o", str(output_path),
        "--reference-doc=" + str(template_path.resolve())
    ]

    print(f"[Pandoc] Converting {input_md} into {output_docx}...")
    subprocess.run(cmd, check=True, cwd=input_path.parent)
    print(f"[Pandoc] {output_docx} generated successfully !")

if __name__ == '__main__':
    create_pandoc_docx("ressources/notion_export/example.md", "test.docx", "ressources/template.dotx")