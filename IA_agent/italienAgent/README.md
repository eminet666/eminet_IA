# 🇬🇷 Agent d'Apprentissage du Grec Quotidien

Agent IA automatisé qui génère et envoie chaque matin un dialogue en grec moderne avec audio et PDF, pour pratiquer la langue au niveau C1.

## 📋 Description

Cet agent utilise l'API Mistral pour créer des dialogues quotidiens entre deux personnages (Stéphanos et Anna), génère une version audio avec des voix grecques naturelles (edge-tts), et produit un PDF stylisé. Le tout est envoyé automatiquement par email chaque matin à 6h.

## ✨ Fonctionnalités

- **Dialogue quotidien** : Conversation réaliste de ~500 mots en grec moderne (niveau C1)
- **50+ sujets variés** : Culture, histoire, vie quotidienne, philosophie, mythologie, etc.
- **Audio haute qualité** : Voix grecques naturelles masculines et féminines (edge-tts)
- **Vocabulaire enrichi** :
  - Articles définis pour les substantifs (ο, η, το)
  - Formes verbales présent/aoriste
  - 20-25 mots clés avec exemples
- **PDF formaté** : Document A4 prêt à imprimer avec mise en page professionnelle
- **Automatisation complète** : Via GitHub Actions, exécution quotidienne à 6h

## 🏗️ Architecture du projet

```
IA_agent/grecB2_new/
├── main.py                   # Script principal orchestrant le workflow
├── config.py                 # Configuration centralisée (sujets, voix, destinataires)
├── dialogue_generator.py     # Génération du dialogue avec Mistral AI
├── audio_generator.py        # Création audio avec edge-tts
├── pdf_generator.py          # Génération du PDF avec WeasyPrint
├── email_sender.py           # Envoi email avec pièces jointes
├── .env                      # Variables d'environnement (non versionné)
└── .github/workflows/
    └── daily_greek_agent.yml # Automatisation GitHub Actions
```

## 🔧 Technologies utilisées

- **Python 3.11**
- **Mistral AI** : Génération de dialogues intelligents
- **edge-tts** : Synthèse vocale grecque naturelle (Microsoft Azure)
- **pydub** : Traitement audio
- **WeasyPrint** : Génération de PDF
- **GitHub Actions** : Automatisation et déploiement
- **SMTP Gmail** : Envoi des emails

## 📦 Installation locale

### Prérequis

- Python 3.11+
- ffmpeg installé sur votre système
- Compte Gmail avec mot de passe d'application

### Installation des dépendances

```bash
# Cloner le dépôt
git clone <votre-repo>
cd IA_agent/grecB2_new

# Installer les dépendances Python
pip install mistralai python-dotenv edge-tts pydub weasyprint

# Sur Ubuntu/Debian, installer les dépendances système
sudo apt-get install ffmpeg libpango-1.0-0 libpangoft2-1.0-0 libharfbuzz0b libfontconfig1
```

### Configuration

Créer un fichier `.env` à la racine du projet :

```env
MISTRAL_API_KEY=votre_clé_api_mistral
GMAIL_USER=votre_email@gmail.com
GMAIL_PASSWORD=votre_mot_de_passe_application
```

### Exécution

```bash
python main.py
```

## ⚙️ Configuration

### Modifier les destinataires

Dans `config.py`, section `EMAIL_RECIPIENTS` :

```python
EMAIL_RECIPIENTS = [
    "email1@example.com",
    "email2@example.com"
]
```

### Ajouter des sujets de dialogue

Dans `config.py`, section `DIALOGUE_TOPICS` :

```python
DIALOGUE_TOPICS = [
    "Nouveau sujet 1",
    "Nouveau sujet 2",
    # ...
]
```

### Modifier les voix

Dans `config.py`, section `VOICES` :

```python
VOICES = {
    "Stephanos": "el-GR-NestorasNeural",  # Voix masculine
    "Anna": "el-GR-AthinaNeural"          # Voix féminine
}
```

Autres voix grecques disponibles :
- Masculines : `el-GR-NestorasNeural`
- Féminines : `el-GR-AthinaNeural`

## 🤖 Automatisation GitHub Actions

Le workflow s'exécute automatiquement tous les jours à 6h (heure de Paris).

### Configuration des secrets

Dans votre dépôt GitHub, allez dans **Settings > Secrets and variables > Actions** et ajoutez :

- `MISTRAL_API_KEY` : Votre clé API Mistral
- `GMAIL_USER` : Votre adresse Gmail
- `GMAIL_PASSWORD` : Mot de passe d'application Gmail

### Déclencher manuellement

Depuis l'onglet **Actions** de votre dépôt GitHub, vous pouvez déclencher manuellement le workflow avec le bouton "Run workflow".

## 📧 Format de l'email

**Objet :** `grecAgent : [Titre du dialogue en grec] - Dialogue grec quotidien`

**Pièces jointes :**
- 🎧 `dialogue_grec_YYYYMMDD.mp3` : Fichier audio (~2-3 minutes)
- 📄 `dialogue_grec_YYYYMMDD.pdf` : Document PDF (1 page A4)

**Contenu :**
- Dialogue formaté avec mise en page HTML
- Tableau de vocabulaire interactif
- Liens et informations pratiques

## 🎓 Exemple de vocabulaire généré

| Grec | Français | Exemple |
|------|----------|---------|
| **ο καιρός** | le temps (météo) | Ο καιρός σήμερα είναι υπέροχος! |
| **πηγαίνω / πήγα** | aller | Πήγα στην αγορά χθες το πρωί. |
| **η θάλασσα** | la mer | Η θάλασσα είναι γαλάζια σήμερα. |

## 🔍 Dépannage

### L'audio ne se génère pas
- Vérifiez que ffmpeg est installé : `ffmpeg -version`
- Vérifiez votre connexion Internet (edge-tts nécessite une connexion)

### Le PDF n'est pas créé
- Vérifiez que les dépendances WeasyPrint sont installées
- Sur Linux : `sudo apt-get install libpango-1.0-0 libpangoft2-1.0-0`

### L'email n'est pas envoyé
- Vérifiez que vous utilisez un **mot de passe d'application** Gmail (pas votre mot de passe habituel)
- Activez l'authentification à deux facteurs sur Gmail
- Créez un mot de passe d'application : https://myaccount.google.com/apppasswords

### GitHub Actions échoue
- Vérifiez que tous les secrets sont bien configurés
- Consultez les logs dans l'onglet Actions de votre dépôt

## 📝 Logs et suivi

Le script affiche des messages de progression :

```
✓ Configuration chargée
- Génération du dialogue...
✓ Dialogue généré
✓ Titre extrait : Στην Ταβέρνα
✓ 24 répliques extraites
- Génération audio de 24 répliques avec edge-tts...
  ✓ Réplique 1/24 - Stephanos
  ✓ Réplique 2/24 - Anna
  ...
✓ Audio généré : dialogue_grec.mp3 (142.3s)
- Génération du PDF...
✓ PDF généré : dialogue_grec.pdf (87.5 KB)
- Envoi de l'email...
✓ Fichier audio attaché : dialogue_grec_20260107.mp3
✓ Fichier PDF attaché : dialogue_grec_20260107.pdf
✓ Email envoyé avec audio et PDF en pièces jointes
```

## 📅 Rotation des sujets

Les sujets tournent automatiquement en fonction du jour du mois :
- Jour 1 → Sujet 1
- Jour 2 → Sujet 2
- ...
- Jour 31 → Sujet 31
- Jour 32 → Retour au sujet 1

Avec 50+ sujets configurés, vous aurez une grande variété sur plusieurs mois.

## 🤝 Contribution

Pour ajouter de nouvelles fonctionnalités :

1. **Nouveaux sujets** : Modifier `config.py`
2. **Nouveau format de sortie** : Créer un nouveau module (ex: `html_generator.py`)
3. **Nouvelles voix** : Modifier `VOICES` dans `config.py`
4. **Niveau de langue** : Modifier le prompt dans `config.py`

## 📜 Licence

Projet personnel d'apprentissage du grec moderne.

## 🙏 Remerciements

- **Mistral AI** pour l'API de génération de dialogues
- **Microsoft Azure** pour les voix edge-tts
- **Claude (Anthropic)** pour l'assistance au développement

---

**Καλή μελέτη!** (Bonne étude !) 📚🇬🇷