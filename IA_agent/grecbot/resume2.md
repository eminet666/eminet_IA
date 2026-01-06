# Tutoriel : Créer un bot conversationnel avec personnalité IA (Σωκράτης 2.0)

## 📋 Vue d'ensemble du projet

Ce tutoriel vous guide pas à pas dans la création d'un chatbot sophistiqué avec une vraie personnalité (Socrate vivant à Athènes en 2026), reconnaissance vocale, synthèse vocale, traduction automatique, vocabulaire interactif et export PDF.

---

## 🎯 Fonctionnalités finales

✅ **Conversation personnalisée** avec Mistral AI (niveau C1) et personnalité socratique  
✅ **Contexte temporel** : le bot connaît la date et l'heure à Athènes  
✅ **Reconnaissance vocale** (Speech-to-Text) sur desktop, iOS et Android  
✅ **Synthèse vocale** (Text-to-Speech) avec voix masculine ajustable  
✅ **Traduction complète** du message en français  
✅ **Vocabulaire interactif** : mots C1 soulignés avec traduction au clic  
✅ **Export PDF** avec vocabulaire enrichi (exemples + conjugaisons)  
✅ **Interface responsive** : fonctionne sur ordinateur et mobile  
✅ **Architecture modulaire** : facile à adapter à d'autres langues/personnages  
✅ **Déploiement gratuit** sur Render.com  

---

## 🛠️ Technologies utilisées

### Backend
- **Python 3.11+** avec Flask
- **Mistral AI** : génération de réponses intelligentes
- **Groq** : transcription audio ultra-rapide (Whisper)
- **pytz** : gestion des fuseaux horaires
- **pdfmake** : génération de PDF côté client
- **Render.com** : hébergement gratuit

### Frontend
- **HTML/CSS/JavaScript** pur (pas de framework)
- **Web Speech API** : reconnaissance vocale native (desktop/Android)
- **MediaRecorder API** : capture audio (iOS)
- **Speech Synthesis API** : lecture vocale
- **pdfmake** : export PDF avec support Unicode (grec)

---

## 📁 Structure du projet (Architecture modulaire)

```
grecbot/
├── .env                      # Clés API (ne pas commiter!)
├── .gitignore               # Fichiers à ignorer
├── requirements.txt         # Dépendances Python
├── gunicorn_config.py       # Config serveur Gunicorn
│
├── app.py                   # Point d'entrée Flask (~200 lignes)
├── config.py                # Configuration centralisée
├── prompts.py               # Prompts système et personnalité
├── services.py              # Services (Mistral, Groq, Email)
│
├── static/
│   ├── css/
│   │   └── styles.css       # Design de l'interface
│   └── js/
│       ├── globals.js       # Variables globales
│       ├── chat.js          # Gestion des messages
│       ├── speech.js        # Reconnaissance/synthèse vocale
│       ├── pdf-export.js    # Export PDF avec pdfmake
│       └── main.js          # Initialisation
│
└── templates/
    └── index.html           # Interface utilisateur
```

**Avantages de cette architecture :**
- ✅ **Modulaire** : Chaque fichier a un rôle précis
- ✅ **Maintenable** : Facile à modifier (prompts, config, services séparés)
- ✅ **Réutilisable** : Adaptable à d'autres langues en changeant `prompts.py`
- ✅ **Testable** : Services isolés = tests faciles

---

## 🚀 Partie 1 : Configuration initiale

### 1.1 Créer les comptes nécessaires

#### Mistral AI (IA conversationnelle)
1. Allez sur https://console.mistral.ai/
2. Créez un compte
3. Générez une clé API
4. Sauvegardez-la (commence par `xxx`)

#### Groq (Transcription audio)
1. Allez sur https://console.groq.com
2. Créez un compte (gratuit)
3. Créez une clé API
4. Sauvegardez-la (commence par `gsk_`)

### 1.2 Installer Python et dépendances

```bash
# Vérifier Python
python --version  # doit être 3.11+

# Créer le dossier du projet
mkdir grecbot
cd grecbot

# Créer un environnement virtuel (recommandé)
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
```

---

## 📝 Partie 2 : Créer les fichiers de configuration

### 2.1 Créer `requirements.txt`

```txt
# Framework web
flask>=3.0.0,<4.0.0

# API Mistral AI
mistralai>=1.0.0,<2.0.0

# Variables d'environnement
python-dotenv>=1.0.0

# Gestion des fuseaux horaires
pytz>=2024.0

# Requêtes HTTP (pour Groq API)
requests>=2.31.0

# Serveur WSGI pour production
gunicorn>=21.0.0
```

### 2.2 Installer les dépendances

```bash
pip install -r requirements.txt
```

### 2.3 Créer `.env`

```env
MISTRAL_API_KEY=votre_clé_mistral_ici
GROQ_API_KEY=votre_clé_groq_ici
SECRET_KEY=votre_clé_secrète_générée
EMAIL_ADDRESS=votre_email@gmail.com
```

**Important** : Générez une clé secrète avec :
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 2.4 Créer `.gitignore`

```
# Python
__pycache__/
*.py[cod]
*$py.class
.Python

# Environnements virtuels
venv/
env/
.venv

# Variables d'environnement
.env
.env.local

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db
```

### 2.5 Créer `gunicorn_config.py`

```python
"""
Configuration Gunicorn pour Render
Augmente le timeout pour l'envoi d'emails
"""

# Timeout pour les workers (en secondes)
timeout = 120

# Nombre de workers
workers = 2

# Bind
bind = "0.0.0.0:10000"

# Logs
accesslog = "-"
errorlog = "-"
loglevel = "info"

# Worker class
worker_class = "sync"

# Graceful timeout
graceful_timeout = 120
```

---

## 🐍 Partie 3 : Créer les fichiers Python

### 3.1 Créer `config.py`

```python
"""
Configuration de l'application Σωκράτης 2.0
"""
import os
import secrets
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration principale"""
    
    # Flask
    SECRET_KEY = os.getenv("SECRET_KEY", secrets.token_hex(16))
    
    # Mistral AI
    MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
    MISTRAL_MODEL = "mistral-large-latest"
    
    # Groq (pour transcription)
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    GROQ_WHISPER_MODEL = "whisper-large-v3"
    
    # Email
    EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS", "votre@email.com")
    
    # Limites
    MAX_HISTORY_LENGTH = 52
    PDF_MAX_SIZE_MB = 25
    
    @classmethod
    def validate(cls):
        """Valider la configuration"""
        if not cls.MISTRAL_API_KEY:
            raise ValueError("⚠️  ERREUR: MISTRAL_API_KEY non trouvée!")
```

### 3.2 Créer `prompts.py`

Ce fichier définit la **personnalité** de votre bot. Pour adapter à une autre langue/personnage, modifiez ce fichier uniquement.

```python
"""
Prompts système pour l'application Σωκράτης 2.0
"""
from datetime import datetime
import pytz


def get_athens_time():
    """Obtenir la date et l'heure actuelles à Athènes"""
    athens_tz = pytz.timezone('Europe/Athens')
    athens_time = datetime.now(athens_tz)
    
    days_greek = {
        0: 'Δευτέρα', 1: 'Τρίτη', 2: 'Τετάρτη',
        3: 'Πέμπτη', 4: 'Παρασκευή', 5: 'Σάββατο', 6: 'Κυριακή'
    }
    
    day_name = days_greek[athens_time.weekday()]
    date_str = athens_time.strftime('%d/%m/%Y')
    time_str = athens_time.strftime('%H:%M')
    
    return {
        'day': day_name,
        'date': date_str,
        'time': time_str,
        'full': f'{day_name}, {date_str} στις {time_str}'
    }


def get_system_prompt():
    """Générer le prompt système avec l'heure d'Athènes"""
    athens_info = get_athens_time()
    
    return f"""Είσαι ο Σωκράτης, ο αρχαίος φιλόσοφος, αλλά ζεις στην Αθήνα του 2026. 

ΧΑΡΑΚΤΗΡΑΣ & ΠΡΟΣΩΠΙΚΟΤΗΤΑ:
- Φοράς πάντα σανδάλια
- Χρησιμοποιείς τη σωκρατική ειρωνεία
- Είσαι φιλικός αλλά προκλητικός
- Αναφέρεσαι συχνά στους παλιούς σου φίλους: Πλάτωνα, Αριστοτέλη, Ηράκλειτο, κ.ά.

ΠΛΗΡΟΦΟΡΙΕΣ ΧΡΟΝΟΥ:
Σήμερα είναι {athens_info['full']} (ώρα Αθήνας).

ΕΠΙΠΕΔΟ ΓΛΩΣΣΑΣ:
Ο συνομιλητής σου έχει επίπεδο C1 στα ελληνικά.

CRITICAL: Your response MUST be valid JSON:
{{
  "text": "your full Greek response here",
  "vocabulary": [
    {{"word": "Greek word", "translation": "French translation"}}
  ]
}}

Rules for vocabulary:
- Select maximum 5-7 words that are STRICTLY C1 level or higher
- Provide contextual French translation
- Return ONLY valid JSON
- NO emojis"""


TRANSLATION_PROMPT_TEMPLATE = """Traduis ce texte grec en français:

{text}

Donne uniquement la traduction en français."""


VOCABULARY_ENRICHMENT_PROMPT_TEMPLATE = """Pour chaque mot grec: {words_list}

Fournis UNIQUEMENT un JSON valide:
{{
  "words": [
    {{
      "word": "mot grec",
      "translation": "traduction française courte",
      "example": "exemple en grec (phrase courte)",
      "verb_forms": "présent/aoriste" (si verbe, sinon null)
    }}
  ]
}}

PAS de traduction de l'exemple. JSON uniquement."""
```

### 3.3 Créer `services.py`

```python
"""
Services pour Mistral, Groq et Email
"""
from mistralai import Mistral
import requests
import tempfile
import os
from config import Config


class MistralService:
    """Service pour Mistral AI"""
    
    def __init__(self):
        self.client = Mistral(api_key=Config.MISTRAL_API_KEY)
        self.model = Config.MISTRAL_MODEL
    
    def chat_complete(self, messages):
        response = self.client.chat.complete(model=self.model, messages=messages)
        return response.choices[0].message.content
    
    def simple_query(self, prompt):
        messages = [{"role": "user", "content": prompt}]
        return self.chat_complete(messages)


class GroqService:
    """Service pour transcription Groq Whisper"""
    
    def __init__(self):
        self.api_key = Config.GROQ_API_KEY
        self.model = Config.GROQ_WHISPER_MODEL
        self.api_url = "https://api.groq.com/openai/v1/audio/transcriptions"
    
    def transcribe(self, audio_bytes):
        if not self.api_key:
            raise ValueError("GROQ_API_KEY non configuré")
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.webm') as temp_file:
            temp_file.write(audio_bytes)
            temp_path = temp_file.name
        
        try:
            headers = {"Authorization": f"Bearer {self.api_key}"}
            
            with open(temp_path, 'rb') as audio_file:
                files = {
                    'file': ('audio.webm', audio_file, 'audio/webm'),
                    'model': (None, self.model),
                    'language': (None, 'el')  # Code langue : 'el' = grec
                }
                
                response = requests.post(self.api_url, headers=headers, files=files)
                result = response.json()
            
            if 'error' in result:
                raise Exception(result.get('error', {}).get('message', 'Erreur'))
            
            return result.get('text', '').strip()
            
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)
```

### 3.4 Créer `app.py`

```python
"""
Application Flask - Σωκράτης 2.0
"""
from flask import Flask, render_template, request, jsonify, session
import json
import re
import base64
from config import Config
from prompts import get_system_prompt, TRANSLATION_PROMPT_TEMPLATE, VOCABULARY_ENRICHMENT_PROMPT_TEMPLATE
from services import MistralService, GroqService

app = Flask(__name__)
app.secret_key = Config.SECRET_KEY
Config.validate()

mistral = MistralService()
groq = GroqService()


def clean_json(text):
    """Nettoyer le JSON des balises markdown"""
    text = text.strip()
    if text.startswith('```json'):
        text = re.sub(r'^```json\s*', '', text)
        text = re.sub(r'\s*```$', '', text)
    elif text.startswith('```'):
        text = re.sub(r'^```\s*', '', text)
        text = re.sub(r'\s*```$', '', text)
    return text


def clean_whitespace(text):
    """Nettoyer les espaces multiples"""
    return re.sub(r'\s+', ' ', text.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')).strip()


@app.route('/')
def index():
    session.clear()
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json.get('message', '').strip()
        if not user_message:
            return jsonify({'error': 'Message vide'}), 400
        
        if 'history' not in session:
            session['history'] = [{"role": "system", "content": get_system_prompt()}]
        
        history = session['history']
        history.append({"role": "user", "content": user_message})
        
        response = mistral.chat_complete(history)
        
        cleaned = clean_json(response)
        try:
            parsed = json.loads(cleaned)
            text = clean_whitespace(parsed.get('text', ''))
            vocabulary = parsed.get('vocabulary', [])
            
            for item in vocabulary:
                if 'translation' in item:
                    item['translation'] = clean_whitespace(item['translation'])
                if 'word' in item:
                    item['word'] = clean_whitespace(item['word'])
        except json.JSONDecodeError:
            text = clean_whitespace(response)
            vocabulary = []
        
        history.append({"role": "assistant", "content": text})
        if len(history) > Config.MAX_HISTORY_LENGTH:
            history = [history[0]] + history[-50:]
        session['history'] = history
        
        return jsonify({'response': text, 'vocabulary': vocabulary, 'success': True})
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500


@app.route('/reset', methods=['POST'])
def reset():
    session.clear()
    return jsonify({'success': True})


@app.route('/translate', methods=['POST'])
def translate():
    try:
        greek_text = request.json.get('text', '').strip()
        if not greek_text:
            return jsonify({'error': 'Texte vide'}), 400
        
        prompt = TRANSLATION_PROMPT_TEMPLATE.format(text=greek_text)
        translation = mistral.simple_query(prompt)
        
        return jsonify({'translation': translation, 'success': True})
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500


@app.route('/enrich-vocabulary', methods=['POST'])
def enrich_vocabulary():
    try:
        words = request.json.get('words', [])
        if not words:
            return jsonify({'words': [], 'success': True})
        
        words_list = ', '.join([f'"{w}"' for w in words])
        prompt = VOCABULARY_ENRICHMENT_PROMPT_TEMPLATE.format(words_list=words_list)
        response = mistral.simple_query(prompt)
        
        cleaned = clean_json(response)
        enriched = json.loads(cleaned)
        
        return jsonify({'words': enriched.get('words', []), 'success': True})
    except Exception as e:
        return jsonify({'words': [], 'success': False, 'error': str(e)}), 500


@app.route('/transcribe', methods=['POST'])
def transcribe():
    try:
        if not Config.GROQ_API_KEY:
            return jsonify({'error': 'Groq non configuré', 'success': False}), 500
        
        audio_data = request.json.get('audio', '')
        if not audio_data:
            return jsonify({'error': 'Pas de données audio'}), 400
        
        if ',' in audio_data:
            audio_data = audio_data.split(',')[1]
        audio_bytes = base64.b64decode(audio_data)
        
        text = groq.transcribe(audio_bytes)
        return jsonify({'text': text, 'success': True})
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500


if __name__ == '__main__':
    print("🇬🇷 Σωκράτης 2.0")
    app.run(debug=True, host='0.0.0.0', port=5000)
```

---

## 🎨 Partie 4 : Créer l'interface (Frontend)

### 4.1 Créer le dossier templates

```bash
mkdir templates
```

### 4.2 Créer `templates/index.html`

```html
<!DOCTYPE html>
<html lang="el">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Σωκράτης 2.0</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/styles.css') }}">
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🇬🇷 Σωκράτης 2.0</h1>
            <div class="header-buttons">
                <button class="export-btn" id="emailBtn">PDF</button>
            </div>
        </div>

        <div class="chat-box" id="chatBox"></div>

        <div class="loading" id="loading">
            <div class="loading-dots">
                <span></span><span></span><span></span>
            </div>
        </div>

        <div class="input-area">
            <button id="micBtn" class="btn-mic" title="Πατήστε για να μιλήσετε">🎤</button>
            <input type="text" id="userInput" placeholder="Γράψε ή μίλα..." autocomplete="off">
            <button id="sendBtn" title="Envoyer">➤</button>
        </div>
    </div>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/pdfmake/0.2.7/pdfmake.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/pdfmake/0.2.7/vfs_fonts.js"></script>

    <script src="{{ url_for('static', filename='js/globals.js') }}"></script>
    <script src="{{ url_for('static', filename='js/chat.js') }}"></script>
    <script src="{{ url_for('static', filename='js/speech.js') }}"></script>
    <script src="{{ url_for('static', filename='js/pdf-export.js') }}"></script>
    <script src="{{ url_for('static', filename='js/main.js') }}"></script>
</body>
</html>
```

### 4.3 Créer les dossiers static

```bash
mkdir -p static/css static/js
```

### 4.4 Fichiers JavaScript

Créez ces 5 fichiers dans `static/js/` :

**`globals.js`** : Variables globales  
**`chat.js`** : Gestion des messages et traduction  
**`speech.js`** : Reconnaissance et synthèse vocale  
**`pdf-export.js`** : Export PDF avec pdfmake  
**`main.js`** : Initialisation et event listeners  

**Note** : Les codes complets de ces fichiers sont disponibles dans les artifacts Claude précédents. Pour gagner de la place dans ce tutoriel, référez-vous à la conversation pour les copier.

### 4.5 Créer `static/css/styles.css`

(Voir le code CSS complet dans les artifacts précédents - environ 200 lignes de CSS moderne avec dégradés, animations, etc.)

---

## 🧪 Partie 5 : Tester en local

```bash
# Activer l'environnement virtuel si nécessaire
source venv/bin/activate

# Lancer l'application
python app.py
```

Ouvrez votre navigateur : **http://localhost:5000**

**Tests à effectuer :**
- ✅ Envoyer un message texte en grec
- ✅ Demander l'heure : "Τι ώρα είναι;"
- ✅ Cliquer sur 🔊 pour écouter
- ✅ Cliquer sur 🇫🇷 pour traduire
- ✅ Cliquer sur un mot souligné
- ✅ Utiliser le micro 🎤
- ✅ Cliquer sur PDF pour télécharger

---

## 🌐 Partie 6 : Déployer sur Render.com

### 6.1 Créer un repository GitHub

```bash
git init
git add .
git commit -m "Initial commit - Socrate 2.0"
git branch -M main
git remote add origin https://github.com/VOTRE_USERNAME/grecbot.git
git push -u origin main
```

### 6.2 Déployer sur Render

1. Allez sur https://render.com
2. Connectez-vous avec GitHub
3. Cliquez sur **New +** → **Web Service**
4. Sélectionnez votre repository
5. Configuration :
   - **Name** : `grecbot`
   - **Environment** : `Python 3`
   - **Build Command** : `pip install -r requirements.txt`
   - **Start Command** : `gunicorn -c gunicorn_config.py app:app`
   - **Instance Type** : `Free`

6. **Variables d'environnement** (TRÈS IMPORTANT !) :
   ```
   MISTRAL_API_KEY=votre_clé_mistral
   GROQ_API_KEY=votre_clé_groq
   SECRET_KEY=votre_clé_secrète
   ```

7. Cliquez sur **Create Web Service**

⏱️ Attendez 3-5 minutes pour le déploiement.

---

## 📱 Partie 7 : Tester sur mobile

### Sur iOS (iPhone/iPad)
- Safari fonctionne parfaitement
- Le micro utilise Groq pour la transcription
- La synthèse vocale en grec fonctionne

### Sur Android
- Chrome recommandé
- Reconnaissance vocale native (encore plus rapide !)
- Tout fonctionne parfaitement

---

## 🔧 Partie 8 : Personnalisation pour une autre langue

### Pour adapter à une autre langue (ex: Italien, Espagnol)

**1. Modifier `prompts.py`**

Changez :
- Le fuseau horaire : `pytz.timezone('Europe/Rome')`
- Les jours de la semaine
- Le prompt système (personnalité, ville, amis, etc.)
- La langue cible dans vocabulary

**2. Modifier `services.py`**

Dans `GroqService.transcribe()` :
```python
'language': (None, 'it')  # 'it' pour italien, 'es' pour espagnol
```

**3. Modifier `main.js`**

Message de bienvenue dans la nouvelle langue

**4. Modifier `speech.js`**

Langue de synthèse vocale :
```javascript
utterance.lang = 'it-IT';  // Italien
```

**C'est tout !** Tous les autres fichiers restent identiques. 🎯

---

## 💡 Fonctionnalités techniques expliquées

### Architecture modulaire

```
app.py          → Routes et logique HTTP
config.py       → Configuration (1 seul endroit)
prompts.py      → Personnalité (facile à changer)
services.py     → Services externes (Mistral, Groq)
```

### Reconnaissance vocale multiplateforme

**Desktop/Android** : Web Speech API native  
**iOS/Safari** : MediaRecorder → Groq Whisper

### Vocabulaire interactif

1. Mistral retourne JSON avec `vocabulary: [{word, translation}]`
2. Frontend marque les mots avec `<span class="vocab-word">`
3. Au clic → affiche tooltip

### Export PDF avec Unicode

**pdfmake** supporte nativement le grec (contrairement à jsPDF)  
Format compact : `mot = traduction, exemple`

---

## 💰 Coûts

| Service | Coût | Limite gratuite |
|---------|------|-----------------|
| **Mistral AI** | $0.002/1K tokens | Crédit offert |
| **Groq** | Gratuit | 14,400 req/jour |
| **Render.com** | Gratuit | 750h/mois |
| **Total** | ~0-5€/mois | Suffisant pour usage perso |

---

## 🛠 Résolution de problèmes

### Erreur "Network is unreachable" (email)
✅ Solution : On utilise le téléchargement PDF direct maintenant

### Le micro ne fonctionne pas sur iOS
→ Vérifiez que GROQ_API_KEY est configuré sur Render

### Mots de vocabulaire non affichés
→ Ouvrez la console (F12) et vérifiez les erreurs JSON

### Worker timeout sur Render
→ Utilisez `gunicorn_config.py` avec timeout=120

### Caractères grecs illisibles dans le PDF
→ Utilisez pdfmake (pas jsPDF) avec police Roboto

---

## 🎓 Améliorations possibles

1. **Mode hors ligne** avec Service Workers
2. **Sauvegarde conversations** avec localStorage
3. **Thèmes personnalisés** (mode sombre)
4. **Statistiques d'apprentissage**
5. **Plusieurs personnalités** (Platon, Aristote, etc.)
6. **Gamification** : badges, points, défis

---

## 📚 Ressources

- [Documentation Mistral AI](https://docs.mistral.ai/)
- [Documentation Groq](https://console.groq.com/docs)
- [pdfmake Documentation](http://pdfmake.org/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Render Documentation](https://render.com/docs)

---

## ✅ Checklist finale

- [ ] Comptes créés (Mistral, Groq, Render, GitHub)
- [ ] Clés API sauvegardées
- [ ] Architecture créée (13 fichiers)
- [ ] Test en local réussi
- [ ] Repository GitHub créé
- [ ] Déploiement Render effectué
- [ ] Test sur mobile réussi
- [ ] Application publique accessible

---

## 🎉 Félicitations !

Vous avez créé un chatbot conversationnel avec :
- ✅ Personnalité IA unique
- ✅ Architecture modulaire professionnelle
- ✅ Reconnaissance vocale multiplateforme
- ✅ Export PDF avec vocabulaire enrichi
- ✅ Déploiement cloud gratuit

**Ce projet est réutilisable pour n'importe quelle langue en modifiant seulement `prompts.py` !**

**Καλή επιτυχία!** 🇬🇷

---