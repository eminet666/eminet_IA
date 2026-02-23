# config.py
# Configuration générale de l'agent d'apprentissage de l'italien

# Liste des destinataires des emails
EMAIL_RECIPIENTS = [
    "eminet666@gmail.com",
    "anne.lafond@ensaama.net"
]

# Configuration des voix edge-tts pour l'italien
VOICES = {
    "Marco": "it-IT-DiegoNeural",   # Voix masculine italienne
    "Sofia": "it-IT-ElsaNeural"     # Voix féminine italienne
}

# Durée de la pause entre les répliques (en millisecondes)
PAUSE_DURATION = 800

# Couleur d'accentuation (vert drapeau italien)
ACCENT_COLOR = "#009246"

# Liste des sujets pour les dialogues
DIALOGUE_TOPICS = [
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
    "Lo sport in Italia",
    "Un viaggio in Sicilia",
    "La musica italiana contemporanea",
    "Il sistema scolastico italiano",
    "Un problema con il vicino",
    "Le tradizioni napoletane",
    "L'arte barocca italiana",
    "Una conversazione romantica",
    "I musei di Firenze",
    "La commedia dell'arte",
    "Un weekend in Toscana",
    "Il caffè italiano e la sua cultura",
    "Una discussione sulla politica italiana",
    "Il design italiano",
    "Una visita agli Uffizi",
    "La storia dell'Impero Romano",
    "Le isole italiane",
    "La Sardegna",
    "Il carnevale di Venezia",
    "La pizza napoletana",
    "Un viaggio in treno per l'Italia",
    "Una serata all'opera",
    "Gli sport invernali in Italia",
    "La filosofia italiana del Rinascimento",
    "Una lite bonaria tra colleghi",
    "Le tradizioni del Natale italiano",
    "Un incontro inaspettato",
    "La vita notturna italiana",
    "Un appuntamento romantico a Verona"
]

# Prompt pour la génération du dialogue
DIALOGUE_PROMPT = """
Crée un dialogue en italien (niveau B2) entre Marco et Sofia, sur le sujet suivant : {sujet}

Le dialogue doit faire environ une page A4 (environ 500 mots).

FORMATAGE DU DIALOGUE :
- Commence par un titre en italien en rapport avec le sujet du dialogue, au format : <h3>Titre en italien</h3>
- Exemple : <h3>Al mercato</h3> ou <h3>Una serata tra amici</h3>
- Ensuite, chaque réplique doit être dans une balise <p> séparée
- Format : <p><strong>Nom du personnage :</strong> texte de la réplique</p>
- Exemple : <p><strong>Marco:</strong> Ciao Sofia! Come stai?</p>
- Chaque réplique dans son propre paragraphe <p> pour créer un retour à la ligne automatique

VOCABULAIRE :
Après le dialogue, ajoute une section "Vocabolario" (Vocabulaire) avec un tableau HTML.

Le tableau doit avoir 3 colonnes :
- Colonne 1 : Mot en italien (en gras)
- Colonne 2 : Traduction en français
- Colonne 3 : Phrase d'exemple en italien

RÈGLES IMPORTANTES POUR LE VOCABULAIRE :
- Pour les NOMS : toujours inclure l'article défini (il, la, lo, l', i, le, gli)
  Exemple : <strong>il mercato</strong> (pas juste "mercato")
- Pour les VERBES : donner l'infinitif ET le passé composé selon ce format : "infinitif / passé composé"
  Exemple : <strong>andare / sono andato</strong>, <strong>mangiare / ho mangiato</strong>, <strong>dire / ho detto</strong>
- Pour les autres mots (adjectifs, adverbes, etc.) : format normal

Utilise ce format de tableau :
<table class="vocab-table">
    <thead>
        <tr>
            <th>Italien</th>
            <th>Français</th>
            <th>Exemple</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>mot italien avec article OU verbe infinitif/passé composé</strong></td>
            <td>traduction</td>
            <td>phrase d'exemple</td>
        </tr>
    </tbody>
</table>

Assure-toi que le vocabulaire contient environ 20-25 mots clés du dialogue.
"""
