# config.py
# Configuration générale de l'agent d'apprentissage de l'italien

# Liste des destinataires des emails
EMAIL_RECIPIENTS = [
    "eric.sandillon@ensaama.net", 
    "eminet666@gmail.com"
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
    " Un apéritif entre amis ",
    " Au marché local ",
    " Une excursion à Rome ",
    " Le cinéma italien ",
    " Une discussion sur le football ",
    " Les vacances d'été ",
    " La cuisine régionale italienne ",
    " Un entretien d'embauche ",
    " Les transports à Milan ",
    " Une visite à Venise ",
    " La mode italienne ",
    " La Renaissance ",
    " Un dîner en famille ",
    " Les vins italiens ",
    " Dante et la littérature italienne ",
    " Les fêtes traditionnelles italiennes ",
    " Le sport en Italie ",
    " Un voyage en Sicile ",
    " La musique italienne contemporaine ",
    " Le système scolaire italien ",
    " Un problème avec le voisin ",
    " Les traditions napolitaines ",
    " L'art baroque italien ",
    " Une conversation romantique ",
    " Les musées de Florence ",
    " La commedia dell'arte ",
    " Un week-end en Toscane ",
    " Le café italien et sa culture ",
    " Une discussion sur la politique italienne ",
    " Le design italien ",
    " Une visite aux Offices ",
    " L'histoire de l'Empire romain ",
    " Les îles italiennes ",
    " La Sardaigne ",
    " Le carnaval de Venise ",
    " La pizza napolitaine ",
    " Un voyage en train à travers l'Italie ",
    " Une soirée à l'opéra ",
    " Les sports d'hiver en Italie ",
    " La philosophie italienne de la Renaissance ",
    " Une querelle amicale entre collègues ",
    " Les traditions de Noël en Italie ",
    " Une rencontre inattendue ",
    " La vie nocturne en Italie ",
    " Un rendez-vous romantique à Vérone "
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
