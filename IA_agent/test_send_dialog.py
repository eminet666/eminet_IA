import smtplib
from email.mime.text import MIMEText

# Configuration mail
smtp_server = "smtp.gmail.com"
smtp_port = 587
smtp_user = "eminet666@gmail.com"
smtp_password = "Kouk0ybag1@"  # Utilise un "App Password" si 2FA activé
destinataire = "eminet666@mail.com"

# Contenu du mail
sujet = "Dialogue en grec moderne - Vocabulaire du jour"
contenu = f"""
<h2>Dialogue du jour</h2>
<p>dialogue</p>

<h2>Vocabulaire et conjugaisons</h2>
<table border="1">
  <tr>
    <th>Mot grec</th>
    <th>Traduction</th>
    <th>Présent</th>
    <th>Aoriste</th>
  </tr>
  {"".join([f"""
  <tr>
    <td>{item['grec']}</td>
    <td>{item['fr']}</td>
    <td>{item['present']}</td>
    <td>{item['aorist']}</td>
  </tr>
  """ for item in vocabulaire])}
</table>
"""

msg = MIMEText(contenu, "html")
msg["Subject"] = sujet
msg["From"] = smtp_user
msg["To"] = destinataire

# Envoi du mail
with smtplib.SMTP(smtp_server, smtp_port) as server:
    server.starttls()
    server.login(smtp_user, smtp_password)
    server.send_message(msg)
