# languages/greek.py
# ============================================================
# Configuration GRECQUE — tous les paramètres propres au grec
# ============================================================

# ── Paramètres modifiables facilement ───────────────────────

# Destinataires spécifiques à cette langue
EMAIL_RECIPIENTS = [
    "eminet666@gmail.com",
]

# Niveau CECRL : A1, A2, B1, B2, C1, C2
LEVEL = "C1"

# Vitesse audio : "0%" normal | "-10%" léger | "-20%" lent | "-30%" très lent
AUDIO_RATE = "-20%"

# Pause entre les répliques (ms)
PAUSE_DURATION = 900

# ── Identité de l'agent ──────────────────────────────────────
ACCENT_COLOR  = "#3498db"
AGENT_PREFIX  = "grecAgent"
OUTPUT_PREFIX = "dialogue_grec"
VOCAB_HEADER  = "Lexilogio"
VOCAB_COL1    = "Grec"

# ── Personnages et voix ──────────────────────────────────────
CHARACTERS = {
    "Stephanos": {"voice": "el-GR-NestorasNeural"},
    "Anna":      {"voice": "el-GR-AthinaNeural"},
}

# ── Contexte narratif ────────────────────────────────────────
CONTEXT = """
CONTEXTE DES PERSONNAGES (à intégrer naturellement dans le dialogue) :
- Stephanos et Anna sont amoureux l'un de l'autre
- Anna a divorcé récemment et garde ses enfants une semaine sur deux
- Anna est artiste : elle peint des tableaux des Cyclades
- Anna crée aussi des bagues ornées de miniatures peintes sur motifs grecs
- Ton tendre, complice, parfois sensuel — séduction et compliments bienvenus
"""

# ── Focus grammatical ────────────────────────────────────────
# Modifie cette section pour orienter les points de grammaire du vocabulaire
GRAMMAR_FOCUS = """
RÈGLES STRICTES POUR LE VOCABULAIRE :
1. Uniquement les mots difficiles et rares du dialogue — pas les mots courants
2. Pour les VERBES : toujours donner les deux voix :
   - Voix active  : présent actif / aoriste actif
   - Voix passive : présent passif / aoriste passif (si elle existe)
   Exemple : agapo / agapisa | agapiemai / agapithika
3. Pour les NOMS rares : inclure l'article défini (o, i, to)
4. AUCUNE REDONDANCE : chaque mot une seule fois
5. Environ 20-25 entrées issues du dialogue
"""

# ── Sujets ───────────────────────────────────────────────────
TOPICS = [
    "Les courses au marché",
    "Un dîner en famille",
    "Une sortie au cinéma",
    "Un problème de voisinage",
    "Un voyage en bus",
    "Une discussion sur la météo",
    "Les plans pour le week-end",
    "Une visite chez le médecin",
    "L'organisation d'une fête",
    "Une conversation au café",
    "Les traditions grecques",
    "Une journée à la plage",
    "Les voyages en bateau",
    "Les habitudes alimentaires",
    "Les projets de vacances",
    "La littérature grecque",
    "La Crète", "Chios", "Samos", "Athènes", "Thessalonique",
    "Les îles grecques",
    "La musique grecque contemporaine",
    "Le rébétiko",
    "La cuisine grecque traditionnelle",
    "Les sites archéologiques",
    "La mythologie grecque",
    "Les fêtes religieuses en Grèce",
    "La guerre d'indépendance grecque",
    "La philosophie stoïcienne",
    "Les Jeux Olympiques antiques",
    "Anna parle de ses peintures des Cyclades",
    "Anna crée des bagues avec des miniatures peintes",
    "Stephanos admire le travail artistique d'Anna",
    "Anna et Stephanos planifient un voyage dans les Cyclades",
    "Les enfants d'Anna et la vie de famille recomposée",
    "Une soirée romantique entre Stephanos et Anna",
    "Stephanos fait des compliments à Anna",
    "Anna et Stephanos se confient leurs désirs",
    "Anna parle de sa vie après son divorce",
    "Une promenade romantique à Athènes",
]

# ── Prompt ───────────────────────────────────────────────────
PROMPT_TEMPLATE = """
Crée un dialogue en grec moderne (niveau {level}) entre Stephanos et Anna,
sur le sujet suivant : {sujet}

{context}

Le dialogue doit faire environ une page A4 (environ 500 mots).

FORMATAGE DU DIALOGUE :
- Titre en grec : <h3>Titre en grec</h3>
- Chaque réplique : <p><strong>Nom:</strong> texte</p>
- Exemple : <p><strong>Stephanos:</strong> Geia sou Anna!</p>

VOCABULAIRE :
Après le dialogue, section "{vocab_header}" avec tableau HTML.
Colonnes : {vocab_col1} | Français | Exemple

{grammar_focus}

<table class="vocab-table">
  <thead><tr><th>{vocab_col1}</th><th>Français</th><th>Exemple</th></tr></thead>
  <tbody><tr><td><strong>mot</strong></td><td>traduction</td><td>exemple</td></tr></tbody>
</table>
"""
