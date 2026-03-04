# core/email_sender.py
# Envoi email avec pièces jointes — moteur générique

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime


def send_email(gmail_user, gmail_password, content, lang, title, audio_file, pdf_file):
    c = lang.ACCENT_COLOR

    msg            = MIMEMultipart()
    msg["From"]    = gmail_user
    msg["To"]      = ", ".join(lang.EMAIL_RECIPIENTS)
    msg["Subject"] = f"{lang.AGENT_PREFIX} : {title}" if title else f"{lang.AGENT_PREFIX} : Dialogue quotidien"

    attach_info = []
    if audio_file: attach_info.append("🎧 Fichier audio pour améliorer ta prononciation")
    if pdf_file:   attach_info.append("📄 PDF à imprimer ou à conserver")

    attach_html = ""
    if attach_info:
        attach_html = f"""
        <div class="notice">
            <strong>Pièces jointes :</strong><br>
            {"<br>".join(attach_info)}
        </div>"""

    html = f"""<html>
<head>
<style>
    body         {{ font-family: Arial, sans-serif; line-height: 1.5; max-width: 800px; margin: 0 auto; padding: 15px; font-size: 14px; }}
    h2           {{ color: #2c3e50; border-bottom: 2px solid {c}; padding-bottom: 8px; margin-bottom: 12px; font-size: 20px; }}
    .notice      {{ background: #f5f5f5; padding: 10px; border-radius: 4px; margin: 12px 0; font-size: 12px; }}
    .dialogue    {{ background: #f9f9f9; padding: 12px; border-radius: 5px; }}
    .dialogue p  {{ margin: 6px 0; }}
    /* ── Vocabulaire ── */
    .vocab-table                  {{ border-collapse: collapse; width: 100%; margin-top: 12px; font-size: 14px; }}
    .vocab-table th               {{ background: {c}; color: white; padding: 5px 4px; text-align: left; font-weight: bold; }}
    .vocab-table td               {{ border: 1px solid #ddd; padding: 4px 5px; vertical-align: top; line-height: 1.3; }}
    .vocab-table tr:nth-child(even) {{ background: #f9f9f9; }}
    .vocab-table td:first-child   {{ width: 18%; }}
    .vocab-table td:nth-child(2)  {{ width: 22%; }}
    .vocab-table td:nth-child(3)  {{ width: 60%; }}
    /* ── Point de grammaire ── */
    .grammar-box {{ background: #f0f7ff; border-left: 4px solid {c}; padding: 12px; margin-top: 20px; border-radius: 4px; }}
    .grammar-box h3 {{ color: #2c3e50; font-size: 15px; margin-top: 0; margin-bottom: 8px; }}
    .grammar-intro {{ margin: 6px 0 12px 0; }}
    .grammar-table {{ border-collapse: collapse; width: 100%; margin: 10px 0; font-size: 14px; }}
    .grammar-table th {{ background: #5d6d7e; color: white; padding: 5px 4px; text-align: left; }}
    .grammar-table td {{ border: 1px solid #ddd; padding: 4px 5px; vertical-align: top; }}
    .grammar-table tr:nth-child(even) {{ background: #f9f9f9; }}
    .grammar-box ul {{ margin: 6px 0; padding-left: 20px; }}
    .grammar-box li {{ margin: 4px 0; }}
</style>
</head>
<body>
    <h2>{title or "Dialogue"}</h2>
    {attach_html}
    <div class="dialogue">{content}</div>
</body>
</html>"""

    msg.attach(MIMEText(html, "html", "utf-8"))

    date_str = datetime.now().strftime('%Y%m%d')
    for fpath, mtype, msub, ext in [
        (audio_file, "audio",       "mpeg", "mp3"),
        (pdf_file,   "application", "pdf",  "pdf"),
    ]:
        if fpath and os.path.exists(fpath):
            try:
                with open(fpath, "rb") as f:
                    part = MIMEBase(mtype, msub)
                    part.set_payload(f.read())
                encoders.encode_base64(part)
                fname = f"{lang.OUTPUT_PREFIX}_{date_str}.{ext}"
                part.add_header("Content-Disposition", f"attachment; filename={fname}")
                msg.attach(part)
                print(f"ok Pièce jointe : {fname}")
            except Exception as e:
                print(f"Erreur pièce jointe : {e}")

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(gmail_user, gmail_password)
        server.send_message(msg)
