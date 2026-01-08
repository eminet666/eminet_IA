# 🇬🇷 Σωκράτης 2.0 - Tutoriel Complet

Chatbot conversationnel pour l'apprentissage du grec moderne (niveau C1) avec Socrate comme professeur philosophe.

## 📋 Table des matières

- [Fonctionnalités](#-fonctionnalités)
- [Technologies utilisées](#-technologies-utilisées)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Structure du projet](#-structure-du-projet)
- [Déploiement](#-déploiement)
- [Utilisation](#-utilisation)
- [Troubleshooting](#-troubleshooting)

---

## ✨ Fonctionnalités

### 🗣️ Conversation en grec
- **Socrate comme professeur** : Personnage avec ironie socratique et références philosophiques
- **Niveau C1** : Vocabulaire avancé, idiomes, expressions culturelles
- **Contexte temporel** : Socrate vit à Athènes en 2026
- **Vocabulaire interactif** : Traductions au survol des mots C1

### 🎤 Reconnaissance vocale
- **Sur desktop** : Web Speech API (navigateur)
- **Sur mobile** : Groq Whisper avec post-correction phonétique
- **Corrections automatiques** : σα → θα, τα → θα, etc.
- **Affichage avant envoi** : Possibilité de relire et corriger

### 🔊 Synthèse vocale
- **Azure Speech Services** : Voix masculine grecque (Nestoras Neural)
- **Uniforme sur tous les appareils** : Même voix sur iOS, Android, Windows, Mac
- **Personnalisée** : Vitesse ralentie (-15%) et voix grave (-5Hz) pour Socrate
- **Gratuit** : 500,000 caractères/mois avec Azure for Students

### 📄 Export PDF
- **Conversation complète** avec vocabulaire enrichi
- **Exemples d'usage** et conjugaisons des verbes
- **Téléchargement direct** sur tous les appareils

### 📱 Interface responsive
- **Textarea extensible** : S'adapte automatiquement au texte (1-4 lignes)
- **Défilement vertical uniquement** : Pas de swipe horizontal
- **Compatible barres d'outils mobile** : Zone de saisie toujours visible
- **Design moderne** : Gradient violet, animations fluides

---

## 🛠️ Technologies utilisées

### Backend
- **Flask** : Framework web Python
- **Mistral AI (mistral-large-latest)** : Génération des réponses de Socrate
- **Groq Whisper (whisper-large-v3)** : Transcription audio (mobile)
- **Azure Speech Services** : Synthèse vocale (el-GR-NestorasNeural)

### Frontend
- **Vanilla JavaScript** : Architecture modulaire (5 fichiers JS)
- **CSS3** : Animations, responsive, variables CSS
- **pdfmake** : Génération de PDF côté client

### APIs externes
- **Web Speech API** : Reconnaissance vocale desktop
- **MediaRecorder API** : Capture audio mobile

---

## 📦 Installation

### 1. Cloner le projet

```bash
git clone https://github.com/ton-username/socrates-bot.git
cd socrates-bot
```

### 2. Créer un environnement virtuel

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

**Contenu de `requirements.txt`** :
```
Flask==3.0.0
mistralai==1.0.1
python-dotenv==1.0.0
requests==2.31.0
pytz==2024.1
gunicorn==21.2.0
```

---

## 🔐 Configuration

### 1. Créer le fichier `.env`

```bash
touch .env
```

### 2. Ajouter les variables d'environnement

```env
# Flask
SECRET_KEY=ton_secret_key_ici

# Mistral AI (obligatoire)
MISTRAL_API_KEY=ta_clé_mistral_ici

# Groq Whisper (optionnel, pour reconnaissance vocale mobile)
GROQ_API_KEY=ta_clé_groq_ici

# Azure Speech (optionnel, pour synthèse vocale)
AZURE_SPEECH_KEY=ta_clé_azure_ici
AZURE_SPEECH_REGION=westeurope

# Email (optionnel, pour envoi PDF par email)
EMAIL_ADDRESS=ton_email@gmail.com
EMAIL_PASSWORD=ton_mot_de_passe_app
```

### 3. Obtenir les clés API

#### **Mistral AI** (obligatoire)
1. Va sur [console.mistral.ai](https://console.mistral.ai/)
2. Crée un compte
3. Génère une clé API

#### **Groq** (optionnel)
1. Va sur [console.groq.com](https://console.groq.com/)
2. Crée un compte
3. Génère une clé API

#### **Azure Speech** (recommandé - gratuit pour étudiants)
1. Va sur [Azure for Students](https://azure.microsoft.com/en-us/free/students/)
2. Inscris-toi avec ton email étudiant (pas de carte bancaire !)
3. Dans le portail Azure : Create a resource → Speech Services
   - **Region** : West Europe
   - **Pricing tier** : F0 (gratuit - 500,000 caractères/mois)
4. Récupère ta **Key** et ta **Region** dans "Keys and Endpoint"

---

## 📁 Structure du projet

```
socrates-bot/
├── app.py                    # Application Flask principale
├── config.py                 # Configuration et variables d'env
├── services.py               # Services (Mistral, Groq, Azure, Email)
├── prompts.py                # Prompts système pour Socrate
├── requirements.txt          # Dépendances Python
├── .env                      # Variables d'environnement (à créer)
├── .gitignore               # Fichiers à ignorer par Git
│
├── templates/
│   └── index.html           # Template HTML principal
│
└── static/
    ├── css/
    │   └── styles.css       # Styles CSS
    │
    └── js/
        ├── globals.js       # Variables globales + fix viewport
        ├── chat.js          # Gestion des messages
        ├── speech.js        # Reconnaissance + synthèse vocale
        ├── pdf-export.js    # Génération et téléchargement PDF
        └── main.js          # Initialisation + event listeners
```

---

## 🚀 Déploiement

### Déploiement local

```bash
python app.py
```

Puis ouvre [http://localhost:5000](http://localhost:5000)

### Déploiement sur Render.com

#### 1. Préparer le projet

**a) Créer `render.yaml`** :

```yaml
services:
  - type: web
    name: socrates-bot
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app:app
    envVars:
      - key: MISTRAL_API_KEY
        sync: false
      - key: GROQ_API_KEY
        sync: false
      - key: AZURE_SPEECH_KEY
        sync: false
      - key: AZURE_SPEECH_REGION
        sync: false
      - key: SECRET_KEY
        generateValue: true
```

**b) Créer `.gitignore`** :

```
.env
venv/
__pycache__/
*.pyc
.DS_Store
```

#### 2. Pousser sur GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/ton-username/socrates-bot.git
git push -u origin main
```

#### 3. Déployer sur Render

1. Va sur [render.com](https://render.com)
2. Connecte ton compte GitHub
3. New → Web Service
4. Sélectionne ton repository
5. **Environment Variables** : Ajoute toutes tes clés API
6. Deploy

---

## 💻 Utilisation

### 🗣️ Conversation texte

1. Tape ton message en grec dans la zone de saisie
2. Appuie sur **Enter** ou clique sur **➤**
3. Socrate répond avec du vocabulaire C1 surligné
4. **Clique sur un mot** pour voir sa traduction

### 🎤 Conversation vocale

#### Sur desktop (Windows/Mac)
1. Clique sur **🎤**
2. Parle en grec
3. Le texte apparaît automatiquement
4. Vérifie et envoie avec **Enter**

#### Sur mobile (iOS/Android)
1. Clique sur **🎤**
2. Parle en grec
3. Le texte transcrit apparaît (avec correction automatique σα → θα)
4. **Relis et corrige** si nécessaire
5. Envoie avec **➤**

### 🔊 Écouter les réponses

1. Clique sur **🔊** sous un message de Socrate
2. Écoute la prononciation avec la voix de Nestoras

### 🇫🇷 Traduire un message

1. Clique sur **🇫🇷** sous un message de Socrate
2. La traduction française apparaît en dessous

### 📄 Exporter en PDF

1. Clique sur **PDF** en haut à droite
2. Le PDF se télécharge automatiquement avec :
   - Toute la conversation
   - Le vocabulaire enrichi (exemples + conjugaisons)

---

## 🎨 Personnalisation

### Changer la voix de Socrate

Dans `services.py`, ligne ~150 :

```python
self.speaking_rate = "-15%"  # -50% à +100%
self.pitch = "-5Hz"          # -50Hz à +50Hz
```

**Recommandations** :
- **Socrate réfléchi** : `rate = "-20%"`, `pitch = "-10Hz"`
- **Socrate énergique** : `rate = "0%"`, `pitch = "0Hz"`

### Ajouter des corrections phonétiques

Dans `services.py`, classe `GroqService`, dictionnaire `phonetic_corrections` :

```python
self.phonetic_corrections = {
    r'\bσα\b': 'θα',           # σα → θα (futur)
    r'\bτα\b': 'θα',           # τα → θα (futur)
    # Ajoute tes propres corrections ici
    r'\bton_erreur\b': 'correction',
}
```

### Modifier le personnage de Socrate

Dans `prompts.py`, fonction `get_system_prompt()`, modifie :
- La personnalité
- Les références culturelles
- Le ton et le style
- Les exemples de phrases

---

## 🐛 Troubleshooting

### La voix ne fonctionne pas sur mobile

**Problème** : Azure Speech non configuré

**Solution** :
1. Vérifie que `AZURE_SPEECH_KEY` et `AZURE_SPEECH_REGION` sont dans `.env`
2. Sur Render : ajoute ces variables dans Environment
3. Redéploie l'application

**Fallback** : L'app utilise automatiquement Web Speech API si Azure n'est pas disponible

### La reconnaissance vocale ne fonctionne pas

**Problème** : Groq API non configurée

**Solution** :
1. Ajoute `GROQ_API_KEY` dans `.env`
2. Sur mobile, autorise l'accès au micro dans les paramètres du navigateur

**Sur desktop** : Web Speech API fonctionne sans Groq

### Les boutons sont cachés par la barre d'outils mobile

**Problème** : Résolu dans la version actuelle

**Vérification** :
- `globals.js` contient la fonction `setViewportHeight()`
- `styles.css` utilise `calc(var(--vh) * 100)`

### La transcription fait des erreurs phonétiques

**Solution** : Ajoute les corrections dans `services.py`

```python
# Dans GroqService.__init__()
self.phonetic_corrections = {
    r'\bton_erreur\b': 'correction',
}
```

**Exemples déjà corrigés** :
- σα → θα
- δα → θα
- σαν → θαν

### L'export PDF ne fonctionne pas

**Problème** : pdfmake non chargé

**Solution** : Vérifie dans `index.html` :

```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/pdfmake/0.2.7/pdfmake.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/pdfmake/0.2.7/vfs_fonts.js"></script>
```

---

## 📊 Limites des API gratuites

### Mistral AI
- **Gratuit** : Crédits initiaux à l'inscription
- **Payant** : ~$2 pour 1 million de tokens après épuisement

### Groq Whisper
- **Gratuit** : Usage raisonnable (pas de limite stricte documentée)
- **Rate limit** : 30 requêtes/minute

### Azure Speech (Azure for Students)
- **Gratuit** : 500,000 caractères/mois
- **$100 de crédit** valable 12 mois
- **Après expiration** : ~$1 pour 1 million de caractères

### Recommandation pour usage personnel
Avec **Azure for Students**, tu as largement de quoi utiliser l'app gratuitement pendant 1 an minimum ! 🎓

---

## 🤝 Contributions

Les contributions sont les bienvenues ! Pour contribuer :

1. Fork le projet
2. Crée une branche (`git checkout -b feature/amelioration`)
3. Commit tes changements (`git commit -m 'Ajout fonctionnalité'`)
4. Push vers la branche (`git push origin feature/amelioration`)
5. Ouvre une Pull Request

---

## 📝 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

---

## 👨‍💻 Auteur

Créé avec ❤️ pour l'apprentissage du grec moderne niveau C1

**Contact** : eminet666@gmail.com

---

## 🙏 Remerciements

- **Mistral AI** : Pour leur excellent LLM
- **Groq** : Pour Whisper ultra-rapide
- **Microsoft Azure** : Pour Azure for Students et les voix neurales
- **Socrate** : Pour l'inspiration philosophique (même s'il aurait probablement questionné l'utilité de ce bot) 😉

---

## 🔗 Liens utiles

- [Documentation Mistral AI](https://docs.mistral.ai/)
- [Documentation Groq](https://console.groq.com/docs)
- [Documentation Azure Speech](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/)
- [Azure for Students](https://azure.microsoft.com/en-us/free/students/)
- [Flask Documentation](https://flask.palletsprojects.com/)

---

**Καλή τύχη με τα ελληνικά!** 🇬🇷✨