# languages/spanish.py
# ============================================================
# Configuration ESPAGNOLE — tous les paramètres propres à l'espagnol
# ============================================================

EMAIL_RECIPIENTS = [
    "eric.sandillon@ensaama.net",
    "eminet666@gmail.com",
]

LEVEL = "A2"
AUDIO_RATE = "-25%"
PAUSE_DURATION = 1000

ACCENT_COLOR  = "#c60b1e"
AGENT_PREFIX  = "espAgent"
OUTPUT_PREFIX = "dialogue_espagnol"
VOCAB_HEADER  = "Vocabulario"
VOCAB_COL1    = "Espagnol"

CHARACTERS = {
    "Pablo":     {"voice": "es-ES-AlvaroNeural"},
    "Esperanza": {"voice": "es-ES-ElviraNeural"},
}

CONTEXT = """
CONTEXTE DES PERSONNAGES :
- Pablo et Esperanza sont deux amis espagnols de Madrid
- Ton simple, naturel et encourageant — adapté à un apprenant débutant
"""

GRAMMAR_FOCUS = """
RÈGLES STRICTES POUR LE CHOIX DES MOTS :
1. Sélectionne uniquement les mots utiles et un peu difficiles du dialogue — pas les mots ultra-basiques
2. Pour les VERBES : donner l'infinitif + la conjugaison au présent à la 1ère personne
   Exemple : <strong>querer → quiero</strong>, <strong>poder → puedo</strong>, <strong>ir → voy</strong>
3. Pour les NOMS : inclure l'article défini (el, la, los, las)
   Exemple : <strong>la tienda</strong>, <strong>el mercado</strong>
4. Pour les expressions utiles : les donner telles quelles
   Exemple : <strong>¿cuánto cuesta?</strong>, <strong>me gustaría</strong>
5. AUCUNE REDONDANCE : chaque mot ou expression une seule fois
6. Environ 20-25 entrées, toutes issues du dialogue
"""

TOPICS = [
    "Se présenter et parler de sa famille",
    "Commander au café ou au restaurant",
    "Faire les courses au marché",
    "Demander son chemin dans la ville",
    "Parler de ses activités du week-end",
    "Décrire sa maison ou son appartement",
    "Parler de la météo",
    "Acheter des vêtements dans un magasin",
    "Prendre les transports en commun",
    "Réserver une chambre d'hôtel",
    "Parler de ses goûts musicaux",
    "Une journée typique au travail",
    "Parler de ses vacances préférées",
    "Chez le médecin",
    "À la plage en été",
    "Les sports et loisirs préférés",
    "Préparer un repas ensemble",
    "Une fête d'anniversaire",
    "À la banque",
    "Les fêtes espagnoles",
    "Visiter un musée à Madrid",
    "Une promenade à Barcelone",
    "Le flamenco et la musique espagnole",
    "La gastronomie espagnole — tapas et paella",
    "Un voyage en Andalousie",
    "Visiter l'Alhambra de Grenade",
    "Les îles Canaries",
    "Un rendez-vous romantique à Séville",
    "Parler de sa routine quotidienne",
    "Parler de ses animaux de compagnie",
    "Un pique-nique dans un parc",
    "Les marchés de Noël en Espagne",
]

PROMPT_TEMPLATE = """
Crée un dialogue en espagnol (niveau {level}) entre Pablo et Esperanza,
sur le sujet suivant : {sujet}

{context}

RÈGLES LINGUISTIQUES NIVEAU {level} :
- Vocabulaire simple et courant, phrases courtes
- Temps : présent, pretérito perfecto, futur immédiat (ir + infinitif)
- Pas de subjonctif, pas de conditionnel complexe
- Expressions du quotidien naturelles et utiles

Le dialogue doit faire environ 400-500 mots.

FORMATAGE DU DIALOGUE :
- Titre en espagnol : <h3>Titre en espagnol</h3>
- Exemple : <h3>En el mercado</h3>
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
Après le vocabulaire, identifie UNE structure grammaticale accessible au niveau {level} présente
dans le dialogue (ex : ser vs estar, présent irrégulier, genre des noms, accord adjectif...).
Crée une section "Gramática" avec ce format :

<div class="grammar-box">
  <h3>Gramática : [nom du point en espagnol — traduction en français]</h3>
  <p class="grammar-intro">[Explication simple en français, 2-3 phrases maximum]</p>

  <table class="grammar-table">
    <thead><tr><th>Forme</th><th>Exemple en espagnol</th><th>Traduction</th></tr></thead>
    <tbody>
      <tr><td>...</td><td>...</td><td>...</td></tr>
    </tbody>
  </table>

  <p><strong>Exemples tirés du dialogue :</strong></p>
  <ul>
    <li>[phrase du dialogue en espagnol] — [traduction française]</li>
    <li>[phrase du dialogue en espagnol] — [traduction française]</li>
  </ul>
</div>
"""
