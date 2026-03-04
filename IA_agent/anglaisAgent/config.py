# config.py
# Configuration générale de l'agent d'apprentissage de l'anglais

# Liste des destinataires des emails
EMAIL_RECIPIENTS = [
    "ebardet02@gmail.com"
]

# Configuration des voix edge-tts pour l'anglais
VOICES = {
    "Jack":  "en-GB-RyanNeural",
    "Emily": "en-GB-SoniaNeural"
}

# Vitesse de la voix (-20% = 20% plus lente, "0%" = normale)
AUDIO_RATE = "-15%"

# Durée de la pause entre les répliques (en millisecondes)
PAUSE_DURATION = 900

# Couleur d'accentuation (rouge drapeau anglais)
ACCENT_COLOR = "#c60b1e"

# Liste des sujets pour les dialogues (adaptés au niveau A2)
DIALOGUE_TOPICS = [
    "Introducing yourself and your family",
    "Ordering food and drinks at a café",
    "Shopping at the supermarket",
    "Asking for directions in the city",
    "Talking about weekend activities",
    "Describing your home or flat",
    "Talking about the weather",
    "Buying clothes in a shop",
    "Taking public transport",
    "Booking a hotel room",
    "Talking about favourite music",
    "A typical day at work or school",
    "Talking about holiday plans",
    "At the doctor's",
    "A day at the beach",
    "Favourite sports and hobbies",
    "Cooking a meal together",
    "A birthday party",
    "At the bank",
    "Talking about British traditions",
    "Visiting a museum in London",
    "A walk in the countryside",
    "Christmas traditions in the UK",
    "Talking about daily routine",
    "A picnic in the park",
    "Visiting Buckingham Palace",
    "A trip to Edinburgh",
    "A night at the theatre",
    "Planning a road trip in England",
    "Talking about dreams and ambitions",
]

# Prompt pour la génération du dialogue
DIALOGUE_PROMPT = """
Crée un dialogue en anglais (niveau A2) entre Jack et Emily, sur le sujet suivant : {sujet}

Le dialogue doit faire environ une page A4 (environ 400-500 mots).

NIVEAU A2 — RÈGLES LINGUISTIQUES STRICTES :
- Utilise uniquement du vocabulaire simple et courant, accessible à un débutant avancé
- Phrases courtes et structures grammaticales simples
- Temps utilisés : present simple, present continuous, past simple, going to
- Pas de subjonctif, pas de conditionnel complexe
- Des expressions du quotidien naturelles et utiles

FORMATAGE DU DIALOGUE :
- Commence par un titre en anglais en rapport avec le sujet, au format : <h3>Titre en anglais</h3>
- Exemple : <h3>En el mercado</h3> ou <h3>Una tarde con amigos</h3>
- Ensuite, chaque réplique dans une balise <p> séparée
- Format : <p><strong>Nom du personnage :</strong> texte de la réplique</p>
- Exemple : <p><strong>Jack:</strong> ¡Hola Emily! ¿Cómo estás?</p>

VOCABULAIRE :
Après le dialogue, ajoute une section "Vocabulario" avec un tableau HTML.

Le tableau doit avoir 3 colonnes :
- Colonne 1 : Mot en anglais (en gras)
- Colonne 2 : Traduction en français
- Colonne 3 : Phrase d'exemple en anglais

RÈGLES STRICTES POUR LE CHOIX DES MOTS :
1. Sélectionne uniquement les mots utiles et un peu difficiles du dialogue — pas les mots ultra-basiques
2. Pour les VERBES : donner l'infinitif + le past simple
   Exemple : <strong>to go → went</strong>, <strong>to buy → bought</strong>, <strong>to say → said</strong>
3. Pour les NOMS : inclure l'article défini (a / an / the)
   Exemple : <strong>the market</strong>, <strong>a shop</strong>
4. Pour les expressions utiles : les donner telles quelles
   Exemple : <strong>How much is it?</strong>, <strong>I would like...</strong>, <strong>What about you?</strong>
5. AUCUNE REDONDANCE : chaque mot ou expression une seule fois
6. Environ 20-25 entrées, toutes issues du dialogue

Utilise ce format de tableau :
<table class="vocab-table">
    <thead>
        <tr>
            <th>anglais</th>
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
