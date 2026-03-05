# languages/greek.py
# ============================================================
# Configuration GRECQUE — tous les paramètres propres au grec
# ============================================================

# ── Paramètres modifiables facilement ───────────────────────

EMAIL_RECIPIENTS = [
    "eric.sandillon@ensaama.net",
    "eminet666@gmail.com",
]

LEVEL = "C1"

AUDIO_RATE = "-20%"

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

# ── Focus grammatical (règles pour le tableau de vocabulaire) ─
GRAMMAR_FOCUS = """
RÈGLES STRICTES POUR LE VOCABULAIRE :
1. Uniquement les mots difficiles et rares du dialogue — pas les mots courants
2. Pour les VERBES : toujours donner les deux voix :
   - Voix active  : présent actif / aoriste actif
   - Voix passive : présent passif / aoriste passif (si elle existe)
   Exemple : αγαπώ / αγάπησα | αγαπιέμαι / αγαπήθηκα
3. Pour les NOMS rares : inclure l'article défini (ο, η, το)
4. AUCUNE REDONDANCE : chaque mot une seule fois
5. Environ 20-25 entrées issues du dialogue
"""

# ── Thèmes de grammaire avancée (niveau C — indépendants du dialogue) ──
# Mistral pioche dans cette liste selon le jour.
# Ajoute, supprime ou réordonne librement ces thèmes.
GRAMMAR_TOPICS = [
    # Déclinaisons — noms
    "Déclinaison des noms masculins de la 1re déclinaison en -ας et -ης (ex. : ο ναύτης, ο άντρας) — paradigme complet au singulier et au pluriel",
    "Déclinaison des noms féminins de la 1re déclinaison en -α et -η (ex. : η γυναίκα, η αγάπη) — paradigme complet",
    "Déclinaison des noms masculins de la 2e déclinaison en -ος (ex. : ο άνθρωπος, ο φίλος) — singulier et pluriel",
    "Déclinaison des noms neutres en -ο et -ι (ex. : το βιβλίο, το παιδί) — singulier et pluriel",
    "Déclinaison des noms neutres en -μα (ex. : το γράμμα, το πρόβλημα) — singulier et pluriel",
    "Déclinaison des noms irréguliers fréquents (ex. : ο πατέρας, η μητέρα, ο καφές, το φως)",
    # Déclinaisons — adjectifs
    "Déclinaison des adjectifs en -ος/-α/-ο (ex. : ωραίος, ωραία, ωραίο) — accord en genre, nombre et cas",
    "Déclinaison des adjectifs en -ύς/-ιά/-ύ (ex. : βαθύς, βαθιά, βαθύ) — paradigme complet",
    "Déclinaison des adjectifs en -ής/-ής/-ές (ex. : συνεχής, ειλικρινής) — paradigme complet",
    "Le comparatif et le superlatif des adjectifs — formes synthétiques et analytiques",
    # Conjugaisons — voix active
    "Conjugaison complète au présent actif des verbes de type A en -ω (ex. : γράφω, διαβάζω)",
    "Conjugaison complète au présent actif des verbes contractes en -άω/-ώ (ex. : αγαπώ, περνώ)",
    "Conjugaison complète au présent actif des verbes contractes en -έω/-ώ et -όω/-ώ (ex. : καλώ, αργώ)",
    "L'imparfait actif : formation et usage — différence aspectuelle avec l'aoriste (ex. : έγραφα vs έγραψα)",
    "L'aoriste actif : verbes du 1er groupe (ex. : έγραψα) et du 2e groupe (ex. : έφαγα, είπα)",
    "Le futur simple actif : formation avec θα + présent et θα + aoriste — distinction aspectuelle",
    "Le parfait et le plus-que-parfait actifs : formation avec έχω/είχα + participe invariable",
    # Conjugaisons — voix passive
    "Conjugaison complète au présent passif (ex. : γράφομαι, αγαπιέμαι) — terminaisons et accent",
    "L'aoriste passif : formation et paradigme (ex. : γράφτηκα, αγαπήθηκα, λέχτηκα)",
    "Le futur passif : formation et exemples — distinction aspectuelle",
    "Les verbes déponents : passifs de forme, actifs de sens (ex. : έρχομαι, σκέφτομαι, κοιμάμαι)",
    # Modes et aspects
    "Le subjonctif en grec moderne : formation avec να + présent ou aoriste — usages principaux",
    "L'aspect verbal en grec : imperfectif (présent/imparfait) vs perfectif (aoriste) — exemples contrastés",
    "Le participe présent actif en -οντας/-ώντας : formation, accord et usages",
    "L'infinitif en grec moderne : il n'existe pas — comment le remplacer (να + subjonctif, etc.)",
    # Pronoms
    "Les pronoms personnels forts et clitiques (faibles) : formes, place et usage en grec moderne",
    "Les pronoms relatifs : ο οποίος / που — différences d'usage et exemples",
    "Les pronoms démonstratifs : αυτός, εκείνος, τούτος — déclinaison et usage",
    "Les pronoms indéfinis : κάποιος, κάτι, κανένας, τίποτα — formes et contextes",
    # Syntaxe avancée
    "La proposition conditionnelle en grec : réelle (αν + présent), potentielle, irréelle — exemples",
    "La proposition causale : γιατί, επειδή, μιας και, αφού — nuances et registres",
    "La proposition concessive : αν και, μολονότι, παρόλο που — exemples en contexte",
    "La proposition temporelle : όταν, μόλις, πριν, αφού — choix du mode et de l'aspect",
    "Le discours indirect en grec moderne : transformations des temps et des pronoms",
    # Orthographe et accentuation
    "Les règles d'accentuation en grec moderne : principes généraux et cas particuliers",
    "Homophones et paronymes fréquents en grec moderne (ex. : αυτός/αυτός, πότε/ποτέ, ότι/ό,τι)",
]

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
- Exemple : <p><strong>Stephanos:</strong> Γεια σου Άννα!</p>

VOCABULAIRE :
Après le dialogue, section "{vocab_header}" avec tableau HTML.
Colonnes : {vocab_col1} | Français | Exemple

{grammar_focus}

<table class="vocab-table">
  <thead><tr><th>{vocab_col1}</th><th>Français</th><th>Exemple</th></tr></thead>
  <tbody><tr><td><strong>mot</strong></td><td>traduction</td><td>exemple</td></tr></tbody>
</table>

POINT DE GRAMMAIRE AVANCÉE :
Présente un exposé complet et pédagogique sur le thème suivant :
{grammar_topic}

Ce point est INDÉPENDANT du dialogue — construis tes propres exemples clairs et représentatifs.
L'objectif est la révision approfondie d'un point de grammaire grecque pour un apprenant de niveau {level}.

LANGUE DE L'EXPLICATION : tout le texte explicatif (intro, en-têtes du tableau, commentaires)
doit être rédigé EN FRANÇAIS. Seuls les exemples grecs et les formes du tableau sont en grec.

Crée une section "Γραμματική" avec ce format :

<div class="grammar-box">
  <h3>Γραμματική : [titre du point en grec — traduction en français]</h3>
  <p class="grammar-intro">[Explication complète EN FRANÇAIS : règle, formation, usage, pièges éventuels — 4-5 phrases]</p>

  <table class="grammar-table">
    <thead><tr><th>Forme</th><th>Exemple en grec</th><th>Traduction en français</th></tr></thead>
    <tbody>
      <tr><td>[nom de la forme EN FRANÇAIS]</td><td>[exemple grec]</td><td>[traduction française]</td></tr>
    </tbody>
  </table>

  <p><strong>Exemples en contexte :</strong></p>
  <ul>
    <li>[phrase construite en grec] — [traduction française]</li>
    <li>[phrase construite en grec] — [traduction française]</li>
    <li>[phrase construite en grec] — [traduction française]</li>
  </ul>
</div>
"""
