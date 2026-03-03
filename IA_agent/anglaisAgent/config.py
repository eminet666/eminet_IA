# config.py
# ============================================================
# Configuration globale — commune à tous les agents de langue
# ============================================================
# C'est ici que tu ajustes les paramètres partagés.
# Les paramètres spécifiques à chaque langue sont dans languages/
# ============================================================

# ── Destinataires des emails ────────────────────────────────
EMAIL_RECIPIENTS = [
    "ebardet02@gmail.com",
    "eminet666@gmail.com"
]

# ── Audio ───────────────────────────────────────────────────
# Vitesse d'élocution edge-tts
# "0%"  = vitesse normale
# "-10%" = légèrement plus lent
# "-20%" = lent (recommandé pour A2/B1)
# "-30%" = très lent
AUDIO_RATE = "-20%"

# Pause entre les répliques (en millisecondes)
PAUSE_DURATION = 900

# ── Niveaux de langue ───────────────────────────────────────
# Ces niveaux sont injectés dans le prompt de chaque langue.
# Tu peux les modifier ici sans toucher aux fichiers de langue.
LANGUAGE_LEVELS = {
    "greek":   "C1",
    "italian": "B2",
    "spanish": "A2",
    "english": "A2"
}

# ── PDF ─────────────────────────────────────────────────────
PDF_PAGE_SIZE  = "A4"
PDF_MARGIN     = "1.5cm"
FONT_SIZE_BODY = "11pt"
