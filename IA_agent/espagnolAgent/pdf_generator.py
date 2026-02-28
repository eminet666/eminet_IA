# pdf_generator.py
# Génération du PDF avec WeasyPrint

import os
from datetime import datetime
from weasyprint import HTML
from config import ACCENT_COLOR


def generate_pdf_from_dialogue(html_content, title=None, output_file="dialogue_espagnol.pdf"):
    """
    Génère un fichier PDF stylisé à partir du dialogue HTML
    """
    print(f"- Génération du PDF...")

    # Titre du document
    pdf_title = title if title else "Dialogue en espagnol"

    pdf_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>{pdf_title}</title>
        <style>
            @page {{
                size: A4;
                margin: 1.5cm;
            }}

            body {{
                font-family: 'Arial', 'Helvetica', sans-serif;
                line-height: 1.4;
                color: #333;
                font-size: 11pt;
            }}

            .header {{
                text-align: center;
                margin-bottom: 15px;
                padding-bottom: 10px;
                border-bottom: 2px solid {ACCENT_COLOR};
            }}

            .header h1 {{
                color: #2c3e50;
                font-size: 20px;
                margin: 5px 0;
            }}

            .header .date {{
                color: #7f8c8d;
                font-size: 11px;
            }}

            .dialogue {{
                background-color: #f9f9f9;
                padding: 12px;
                border-radius: 5px;
                margin-bottom: 15px;
            }}

            .dialogue h3 {{
                color: #34495e;
                margin-top: 0;
                margin-bottom: 12px;
                font-size: 16px;
            }}

            .dialogue p {{
                margin: 6px 0;
                font-size: 11pt;
            }}

            .dialogue strong {{
                color: #2c3e50;
                font-weight: bold;
            }}

            .vocab-section {{
                margin-top: 15px;
            }}

            .vocab-section h3 {{
                color: #2c3e50;
                border-bottom: 2px solid {ACCENT_COLOR};
                padding-bottom: 5px;
                font-size: 16px;
                margin-bottom: 10px;
            }}

            .vocab-table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 10px;
                font-size: 11pt;
            }}

            .vocab-table th {{
                background-color: {ACCENT_COLOR};
                color: white;
                padding: 4px 4px;
                text-align: left;
                font-weight: bold;
                font-size: 11pt;
            }}

            .vocab-table td {{
                border: 1px solid #ddd;
                padding: 3px 4px;
                vertical-align: top;
                line-height: 1.3;
            }}

            .vocab-table tr:nth-child(even) {{
                background-color: #f9f9f9;
            }}

            .vocab-table td:first-child {{
                font-weight: bold;
                color: #2c3e50;
                width: 18%;
            }}

            .vocab-table td:nth-child(2) {{
                width: 22%;
            }}

            .vocab-table td:nth-child(3) {{
                width: 60%;
            }}

            .footer {{
                margin-top: 20px;
                padding-top: 10px;
                border-top: 1px solid #ecf0f1;
                text-align: center;
                color: #7f8c8d;
                font-size: 11pt;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>{pdf_title}</h1>
            <div class="date">{datetime.now().strftime('%d/%m/%Y')}</div>
        </div>

        <div class="dialogue">
            {html_content}
        </div>
    </body>
    </html>
    """

    try:
        HTML(string=pdf_html).write_pdf(output_file)
        file_size = os.path.getsize(output_file) / 1024
        print(f"✓ PDF généré : {output_file} ({file_size:.1f} KB)")
        return output_file

    except Exception as e:
        print(f"⚠️  Erreur lors de la génération du PDF : {e}")
        return None
