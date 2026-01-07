# config.py
# Configuration générale de l'agent d'apprentissage du grec

# Liste des destinataires des emails
EMAIL_RECIPIENTS = [
    "eminet666@gmail.com",
    "anne.lafond@ensaama.net"
]

# Configuration des voix edge-tts pour le grec
VOICES = {
    "Stephanos": "el-GR-NestorasNeural",  # Voix masculine grecque
    "Anna": "el-GR-AthinaNeural"          # Voix féminine grecque
}

# Durée de la pause entre les répliques (en millisecondes)
PAUSE_DURATION = 800

# Liste des sujets pour les dialogues
DIALOGUE_TOPICS = [
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
    "Les activités de loisirs",
    "Une dispute amicale",
    "Les traditions grecques",
    "Une journée à la plage",
    "Les transports en commun",
    "Les voyages en bateau",
    "Une rencontre imprévue",
    "Les habitudes alimentaires",
    "Les projets de vacances",
    "Une visite culturelle",
    "La littérature grecque",
    "La Crète",
    "Chios",
    "Samos",
    "Athènes",
    "Thessalonique",
    "Les îles grecques",
    "La Thessalie",
    "Les séries grecques populaires",
    "Le cinéma grec",
    "La musique grecque contemporaine",
    "Le rébétiko",
    "La cuisine grecque traditionnelle",
    "Les sites archéologiques en Grèce",
    "Les musées archéologiques",
    "L'histoire de la Grèce antique",
    "La mythologie grecque",
    "Les fêtes religieuses en Grèce",
    "La guerre d'indépendance grecque",
    "La vie quotidienne en Grèce moderne",
    "L'histoire moderne de la Grèce",
    "La politique en Grèce contemporaine",
    "Les grands philosophes grecs",
    "La démocratie athénienne",
    "Les Jeux Olympiques antiques",
    "La philosophie stoïcienne",
    "Les écoles philosophiques grecques",
    "La statuaire grecque antique",
    "Un rapprochement amoureux",
    "Une discussion de séduction",
    "Une conversation sur les relations amoureuses"
]

# Prompt pour la génération du dialogue
DIALOGUE_PROMPT = """
Crée un dialogue en grec moderne (niveau C1) entre Stephanos et Anna, sur le sujet suivant : {sujet}

Le dialogue doit faire environ une page A4 (environ 500 mots).

FORMATAGE DU DIALOGUE :
- Commence par un titre en grec en rapport avec le sujet du dialogue, au format : <h3>Titre en grec</h3>
- Exemple : <h3>Στο Σουπερμάρκετ</h3> ou <h3>Μια Συζήτηση για τον Καιρό</h3>
- Ensuite, chaque réplique doit être dans une balise <p> séparée
- Format : <p><strong>Nom du personnage :</strong> texte de la réplique</p>
- Exemple : <p><strong>Στέφανος:</strong> Γεια σου Άννα! Τι κάνεις;</p>
- Chaque réplique dans son propre paragraphe <p> pour créer un retour à la ligne automatique

VOCABULAIRE :
Après le dialogue, ajoute une section "Λεξιλόγιο" (Vocabulaire) avec un tableau HTML.

Le tableau doit avoir 3 colonnes :
- Colonne 1 : Mot en grec (en gras)
- Colonne 2 : Traduction en français
- Colonne 3 : Phrase d'exemple en grec

RÈGLES IMPORTANTES POUR LE VOCABULAIRE :
- Pour les SUBSTANTIFS : toujours inclure l'article défini (ο, η, το)
  Exemple : <strong>ο καιρός</strong> (pas juste "καιρός")
- Pour les VERBES : donner la forme au présent ET à l'aoriste selon ce format : "présent / aoriste"
  Exemple : <strong>πηγαίνω / πήγα</strong>, <strong>τρώω / έφαγα</strong>, <strong>λέω / είπα</strong>
- Pour les autres mots (adjectifs, adverbes, etc.) : format normal

Utilise ce format de tableau :
<table class="vocab-table">
    <thead>
        <tr>
            <th>Grec</th>
            <th>Français</th>
            <th>Exemple</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>mot grec avec article OU verbe présent/aoriste</strong></td>
            <td>traduction</td>
            <td>phrase d'exemple</td>
        </tr>
    </tbody>
</table>

Assure-toi que le vocabulaire contient environ 20-25 mots clés du dialogue.
"""