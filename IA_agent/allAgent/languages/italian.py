# languages/italian.py
# ============================================================
# Configuration ITALIENNE — tous les paramètres propres à l'italien
# ============================================================

EMAIL_RECIPIENTS = [
    "eric.sandillon@ensaama.net"
]

LEVEL = "B2"
AUDIO_RATE = "-20%"
PAUSE_DURATION = 900

ACCENT_COLOR  = "#009246"
AGENT_PREFIX  = "italAgent"
OUTPUT_PREFIX = "dialogue_italien"
VOCAB_HEADER  = "Vocabolario"
VOCAB_COL1    = "Italien"

CHARACTERS = {
    "Marco": {"voice": "it-IT-DiegoNeural"},
    "Sofia": {"voice": "it-IT-ElsaNeural"},
}

CONTEXT = """
CONTEXTE DES PERSONNAGES :
- Marco et Sofia sont deux amis italiens cultivés et curieux
- Ils aiment discuter de culture, de gastronomie et de vie quotidienne
- Ton naturel, chaleureux et spontané
"""

GRAMMAR_FOCUS = """
RÈGLES POUR LE VOCABULAIRE :
1. Mots utiles et un peu difficiles uniquement — pas les ultra-basiques
2. Pour les VERBES : infinitif + passé composé
   Exemple : andare / sono andato, mangiare / ho mangiato, dire / ho detto
3. Pour les NOMS : inclure l'article défini (il, la, lo, l', i, le, gli)
4. AUCUNE REDONDANCE : chaque mot une seule fois
5. Environ 20-25 entrées issues du dialogue
"""

TOPICS = [
    "Un aperitivo tra amici",
    "Al mercato rionale",
    "Una gita a Roma",
    "Il cinema italiano",
    "Una discussione sul calcio",
    "Le vacanze estive",
    "La cucina italiana regionale",
    "Un colloquio di lavoro",
    "I trasporti a Milano",
    "Una visita a Venezia",
    "La moda italiana",
    "Il Rinascimento",
    "Una cena in famiglia",
    "I vini italiani",
    "Dante e la letteratura italiana",
    "Le feste tradizionali italiane",
    "Un viaggio in Sicilia",
    "La musica italiana contemporanea",
    "Un problema con il vicino",
    "Le tradizioni napoletane",
    "L'arte barocca italiana",
    "Una conversazione romantica",
    "I musei di Firenze",
    "La commedia dell'arte",
    "Un weekend in Toscana",
    "Il caffè italiano e la sua cultura",
    "Il design italiano",
    "Una visita agli Uffizi",
    "La storia dell'Impero Romano",
    "Il carnevale di Venezia",
    "La pizza napoletana",
    "Una serata all'opera",
    "Un appuntamento romantico a Verona",
]

PROMPT_TEMPLATE = """
Crée un dialogue en italien (niveau {level}) entre Marco et Sofia,
sur le sujet suivant : {sujet}

{context}

Le dialogue doit faire environ une page A4 (environ 500 mots).

FORMATAGE DU DIALOGUE :
- Titre en italien : <h3>Titre en italien</h3>
- Exemple : <h3>Al mercato</h3>
- Chaque réplique : <p><strong>Nom:</strong> texte</p>

VOCABULAIRE :
Après le dialogue, section "{vocab_header}" avec tableau HTML.
Colonnes : {vocab_col1} | Français | Exemple

{grammar_focus}

<table class="vocab-table">
  <thead><tr><th>{vocab_col1}</th><th>Français</th><th>Exemple</th></tr></thead>
  <tbody><tr><td><strong>mot</strong></td><td>traduction</td><td>exemple</td></tr></tbody>
</table>

POINT DE GRAMMAIRE :
Après le vocabulaire, identifie UNE structure grammaticale importante présente dans le dialogue
(ex : subjonctif, conditionnel, gérondif, accord du participe passé, pronoms...).
Crée une section "Grammatica" avec ce format :

<div class="grammar-box">
  <h3>Grammatica : [nom du point en italien — traduction en français]</h3>
  <p class="grammar-intro">[Explication claire en français, 2-3 phrases maximum]</p>

  <table class="grammar-table">
    <thead><tr><th>Forme</th><th>Exemple en italien</th><th>Traduction</th></tr></thead>
    <tbody>
      <tr><td>...</td><td>...</td><td>...</td></tr>
    </tbody>
  </table>

  <p><strong>Exemples tirés du dialogue :</strong></p>
  <ul>
    <li>[phrase du dialogue en italien] — [traduction française]</li>
    <li>[phrase du dialogue en italien] — [traduction française]</li>
  </ul>
</div>
"""
