# config.py
# Configuration générale de l'agent d'apprentissage de l'espagnol

# Liste des destinataires des emails
EMAIL_RECIPIENTS = [
    "eminet666@gmail.com"
]

# Configuration des voix edge-tts pour l'espagnol
VOICES = {
    "Pablo": "es-ES-AlvaroNeural",       # Voix masculine espagnole
    "Esperanza": "es-ES-ElviraNeural"    # Voix féminine espagnole
}

# Vitesse de la voix (-20% = 20% plus lente, "0%" = normale)
AUDIO_RATE = "-15%"

# Durée de la pause entre les répliques (en millisecondes)
PAUSE_DURATION = 900

# Couleur d'accentuation (rouge drapeau espagnol)
ACCENT_COLOR = "#c60b1e"

# Liste des sujets pour les dialogues (adaptés au niveau A2)
DIALOGUE_TOPICS = [
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
    "Parler de son pays d'origine",
    "Les sports et loisirs préférés",
    "Préparer un repas ensemble",
    "Une fête d'anniversaire",
    "Parler de ses amis",
    "À la banque",
    "Regarder un film ensemble",
    "Parler des fêtes espagnoles",
    "Visiter un musée à Madrid",
    "Une promenade à Barcelone",
    "Les traditions de la Semaine Sainte",
    "Le flamenco et la musique espagnole",
    "La gastronomie espagnole — tapas et paella",
    "Un voyage en Andalousie",
    "La sieste et les habitudes espagnoles",
    "Les marchés de Noël en Espagne",
    "Parler de sa routine quotidienne",
    "Une visite au zoo",
    "Apprendre à cuisiner une recette espagnole",
    "Parler de ses animaux de compagnie",
    "Un pique-nique dans un parc",
    "Les fêtes de la Tomatina",
    "Visiter l'Alhambra de Grenade",
    "Les îles Canaries",
    "Parler de son film préféré",
    "Une sortie au théâtre",
    "Parler de la famille royale espagnole",
    "Un rendez-vous romantique à Séville",
    "Les marchés espagnols",
    "Parler des couleurs et des formes"
]

# Prompt pour la génération du dialogue
DIALOGUE_PROMPT = """
Crée un dialogue en espagnol (niveau A2) entre Pablo et Esperanza, sur le sujet suivant : {sujet}

Le dialogue doit faire environ une page A4 (environ 400-500 mots).

NIVEAU A2 — RÈGLES LINGUISTIQUES STRICTES :
- Utilise uniquement du vocabulaire simple et courant, accessible à un débutant avancé
- Phrases courtes et structures grammaticales simples
- Temps utilisés : présent de l'indicatif, passé composé (pretérito perfecto), futur immédiat (ir + infinitif)
- Pas de subjonctif, pas de conditionnel complexe
- Des expressions du quotidien naturelles et utiles

FORMATAGE DU DIALOGUE :
- Commence par un titre en espagnol en rapport avec le sujet, au format : <h3>Titre en espagnol</h3>
- Exemple : <h3>En el mercado</h3> ou <h3>Una tarde con amigos</h3>
- Ensuite, chaque réplique dans une balise <p> séparée
- Format : <p><strong>Nom du personnage :</strong> texte de la réplique</p>
- Exemple : <p><strong>Pablo:</strong> ¡Hola Esperanza! ¿Cómo estás?</p>

VOCABULAIRE :
Après le dialogue, ajoute une section "Vocabulario" avec un tableau HTML.

Le tableau doit avoir 3 colonnes :
- Colonne 1 : Mot en espagnol (en gras)
- Colonne 2 : Traduction en français
- Colonne 3 : Phrase d'exemple en espagnol

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

Utilise ce format de tableau :
<table class="vocab-table">
    <thead>
        <tr>
            <th>Espagnol</th>
            <th>Français</th>
            <th>Exemple</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>mot ou expression</strong></td>
            <td>traduction</td>
            <td>phrase d'exemple tirée ou inspirée du dialogue</td>
        </tr>
    </tbody>
</table>

Assure-toi que le vocabulaire contient environ 20-25 entrées utiles du dialogue.
"""
