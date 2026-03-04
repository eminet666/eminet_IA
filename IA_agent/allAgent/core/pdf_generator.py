# core/pdf_generator.py
# Génération PDF avec WeasyPrint — moteur générique

import os
from datetime import datetime
from weasyprint import HTML


def generate_pdf(html_content, lang, title, config, output_file):
    print("- Génération du PDF...")

    pdf_title = title or "Dialogue"
    c         = lang.ACCENT_COLOR

    pdf_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{pdf_title}</title>
    <style>
        @page {{
            size: {config.PDF_PAGE_SIZE};
            margin: {config.PDF_MARGIN};
        }}
        body {{
            font-family: Arial, Helvetica, sans-serif;
            line-height: 1.4;
            color: #333;
            font-size: {config.FONT_SIZE_BODY};
        }}
        .header {{
            text-align: center;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 2px solid {c};
        }}
        .header h1 {{ color: #2c3e50; font-size: 20px; margin: 5px 0; }}
        .header .date {{ color: #7f8c8d; font-size: 11px; }}
        .dialogue {{
            background-color: #f9f9f9;
            padding: 12px;
            border-radius: 5px;
            margin-bottom: 15px;
        }}
        .dialogue h3 {{ color: #34495e; margin-top: 0; margin-bottom: 12px; font-size: 16px; }}
        .dialogue p {{ margin: 6px 0; font-size: {config.FONT_SIZE_BODY}; }}
        .dialogue strong {{ color: #2c3e50; font-weight: bold; }}
        /* ── Vocabulaire ── */
        .vocab-table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 10px;
            font-size: {config.FONT_SIZE_BODY};
        }}
        .vocab-table th {{
            background-color: {c};
            color: white;
            padding: 4px;
            text-align: left;
            font-weight: bold;
        }}
        .vocab-table td {{ border: 1px solid #ddd; padding: 3px 4px; vertical-align: top; line-height: 1.3; }}
        .vocab-table tr:nth-child(even) {{ background-color: #f9f9f9; }}
        .vocab-table td:first-child {{ font-weight: bold; color: #2c3e50; width: 18%; }}
        .vocab-table td:nth-child(2) {{ width: 22%; }}
        .vocab-table td:nth-child(3) {{ width: 60%; }}
        /* ── Point de grammaire ── */
        .grammar-box {{
            background-color: #f0f7ff;
            border-left: 4px solid {c};
            padding: 12px;
            margin-top: 20px;
            border-radius: 4px;
        }}
        .grammar-box h3 {{ color: #2c3e50; font-size: 15px; margin-top: 0; margin-bottom: 8px; }}
        .grammar-intro {{ margin: 6px 0 12px 0; }}
        .grammar-table {{
            width: 100%;
            border-collapse: collapse;
            margin: 10px 0;
            font-size: {config.FONT_SIZE_BODY};
        }}
        .grammar-table th {{ background-color: #5d6d7e; color: white; padding: 4px; text-align: left; }}
        .grammar-table td {{ border: 1px solid #ddd; padding: 3px 5px; vertical-align: top; }}
        .grammar-table tr:nth-child(even) {{ background-color: #f9f9f9; }}
        .grammar-box ul {{ margin: 6px 0; padding-left: 20px; }}
        .grammar-box li {{ margin: 4px 0; }}
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
</html>"""

    try:
        HTML(string=pdf_html).write_pdf(output_file)
        size = os.path.getsize(output_file) / 1024
        print(f"ok PDF : {output_file} ({size:.1f} KB)")
        return output_file
    except Exception as e:
        print(f"Erreur PDF : {e}")
        return None
