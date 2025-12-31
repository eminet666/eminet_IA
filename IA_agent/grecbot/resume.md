# Tutoriel : Créer un bot conversationnel grec avec IA (Σωκράτης 2.0)

## 📋 Vue d'ensemble du projet

Ce tutoriel vous guide pas à pas dans la création d'un chatbot sophistiqué pour apprendre le grec moderne, avec reconnaissance vocale, synthèse vocale, traduction automatique et apprentissage du vocabulaire interactif.

---

## 🎯 Fonctionnalités finales

✅ **Conversation en grec** avec Mistral AI (niveau C1)  
✅ **Reconnaissance vocale** (Speech-to-Text) sur desktop, iOS et Android  
✅ **Synthèse vocale** (Text-to-Speech) avec voix masculine ajustable  
✅ **Traduction complète** du message en français  
✅ **Vocabulaire interactif** : mots complexes soulignés avec traduction au clic  
✅ **Interface responsive** : fonctionne sur ordinateur et mobile  
✅ **Déploiement gratuit** sur Render.com  

---

## 🛠️ Technologies utilisées

### Backend
- **Python 3.11** avec Flask
- **Mistral AI** : génération de réponses intelligentes en grec
- **Groq** : transcription audio ultra-rapide (Whisper)
- **Render.com** : hébergement gratuit

### Frontend
- **HTML/CSS/JavaScript** pur (pas de framework)
- **Web Speech API** : reconnaissance vocale native (desktop/Android)
- **MediaRecorder API** : capture audio (iOS)
- **Speech Synthesis API** : lecture vocale

---

## 📁 Structure du projet

```
grecbot/
├── app.py                  # Serveur Flask + API
├── requirements.txt        # Dépendances Python
├── .env                    # Clés API (ne pas commiter!)
├── .gitignore             
└── templates/
    └── index.html          # Interface utilisateur
```

---

## 🚀 Partie 1 : Configuration initiale

### 1.1 Créer un compte Mistral AI

1. Allez sur https://console.mistral.ai/
2. Créez un compte
3. Générez une clé API
4. Sauvegardez-la (commence par `xxx`)

### 1.2 Créer un compte Groq

1. Allez sur https://console.groq.com
2. Créez un compte (gratuit)
3. Créez une clé API
4. Sauvegardez-la (commence par `gsk_`)

### 1.3 Installer Python et dépendances

```bash
# Vérifier Python
python --version  # doit être 3.7+

# Créer le dossier du projet
mkdir grecbot
cd grecbot

# Créer un environnement virtuel (optionnel mais recommandé)
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate

# Installer les dépendances
pip install Flask==3.0.0 mistralai==1.0.0 python-dotenv==1.0.0 requests==2.31.0
```

---

## 📝 Partie 2 : Créer les fichiers

### 2.1 Créer `requirements.txt`

```txt
Flask==3.0.0
mistralai==1.0.0
python-dotenv==1.0.0
gunicorn==21.2.0
requests==2.31.0
```

### 2.2 Créer `.env`

```env
MISTRAL_API_KEY=votre_clé_mistral_ici
GROQ_API_KEY=votre_clé_groq_ici
SECRET_KEY=une_clé_secrète_aléatoire
```

**Important** : Générez une clé secrète avec :
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 2.3 Créer `.gitignore`

```
.env
__pycache__/
*.pyc
venv/
.DS_Store
```

### 2.4 Créer `app.py`

Copiez le code de l'artifact `greek_bot_webapp` (le code Python complet avec Mistral et Groq).

### 2.5 Créer `templates/index.html`

```bash
mkdir templates
```

Copiez le code de l'artifact `greek_bot_html` (l'interface complète).

---

## 🧪 Partie 3 : Tester en local

```bash
python app.py
```

Ouvrez votre navigateur : http://localhost:5000

**Tests à effectuer :**
- ✅ Envoyer un message texte en grec
- ✅ Cliquer sur 🔊 pour écouter
- ✅ Cliquer sur 🇫🇷 pour traduire
- ✅ Cliquer sur un mot souligné pour voir la traduction
- ✅ Utiliser le micro 🎤 (sur desktop)

---

## 🌐 Partie 4 : Déployer sur Render.com

### 4.1 Créer un repository GitHub

```bash
git init
git add .
git commit -m "Initial commit - Greek chatbot"
git branch -M main
git remote add origin https://github.com/VOTRE_USERNAME/greek-bot.git
git push -u origin main
```

### 4.2 Déployer sur Render

1. Allez sur https://render.com
2. Connectez-vous avec GitHub
3. Cliquez sur **New +** → **Web Service**
4. Sélectionnez votre repository
5. Configuration :
   - **Name** : `greek-bot`
   - **Root Directory** : (laissez vide ou `IA_agent/grecbot` si sous-dossier)
   - **Environment** : `Python 3`
   - **Build Command** : `pip install -r requirements.txt`
   - **Start Command** : `gunicorn app:app`
   - **Instance Type** : `Free`

6. **Variables d'environnement** (très important !) :
   - `MISTRAL_API_KEY` = votre clé Mistral
   - `GROQ_API_KEY` = votre clé Groq
   - `SECRET_KEY` = votre clé secrète

7. Cliquez sur **Create Web Service**

⏱️ Attendez 2-5 minutes pour le déploiement.

---

## 📱 Partie 5 : Tester sur mobile

### Sur iOS (iPhone/iPad)
- Safari fonctionne parfaitement
- Le micro utilise Groq pour la transcription
- La synthèse vocale fonctionne avec voix grecque

### Sur Android
- Chrome recommandé
- Reconnaissance vocale native (encore plus rapide !)
- Tout fonctionne parfaitement

---

## 🎨 Partie 6 : Personnalisation

### Modifier la vitesse de lecture

Dans `index.html`, ligne ~8 :
```javascript
const SPEECH_RATE = 0.8;  // 0.5 = lent, 1.0 = normal, 1.5 = rapide
```

### Modifier la voix (grave/aiguë)

Dans la fonction `speakText()` :
```javascript
utterance.pitch = 0.8;  // 0.7 = très grave, 1.0 = neutre, 1.3 = aigu
```

### Modifier les couleurs

Dans le `<style>` de `index.html` :
```css
/* Fond d'écran */
background: linear-gradient(135deg, #100666 0%, #270874 100%);

/* Boutons */
background: linear-gradient(135deg, #100666 0%, #270874 100%);
```

### Modifier le niveau de langue

Dans `app.py`, ligne ~20, changez :
```python
Ο συνομιλητής σου έχει επίπεδο C1 στα ελληνικά
```
Par `A2`, `B1`, `B2`, etc.

---

## 🔧 Fonctionnalités techniques expliquées

### Comment fonctionne la reconnaissance vocale ?

**Sur Desktop (Chrome/Edge)** :
1. Web Speech API native du navigateur
2. Gratuit et instantané
3. Transcription directe en grec

**Sur iOS/Safari** :
1. Capture audio avec `MediaRecorder`
2. Conversion en base64
3. Envoi au serveur Flask
4. Serveur envoie à Groq (Whisper)
5. Retour du texte transcrit
6. Envoi automatique du message

### Comment fonctionne le vocabulaire interactif ?

1. Mistral retourne un JSON structuré :
```json
{
  "text": "Χαίρε! Πώς είσαι;",
  "vocabulary": [
    {"word": "Χαίρε", "translation": "Salut/Réjouis-toi"}
  ]
}
```

2. Le frontend parcourt le texte mot par mot
3. Les mots présents dans `vocabulary` sont marqués avec `<span class="vocab-word">`
4. Au clic, affiche une bulle avec la traduction

### Pourquoi Groq et pas OpenAI ?

- ✅ Groq est **gratuit** (limites généreuses)
- ✅ **10x plus rapide** qu'OpenAI Whisper
- ✅ Même qualité de transcription
- ✅ API compatible OpenAI

---

## 💰 Coûts

| Service | Coût | Limite gratuite |
|---------|------|-----------------|
| **Mistral AI** | $0.002/1K tokens | Crédit offert à l'inscription |
| **Groq** | Gratuit | 14,400 requêtes/jour |
| **Render.com** | Gratuit | 750h/mois (suffisant) |
| **Total** | ~0-5€/mois | Largement suffisant pour tests |

**Note** : Après expiration du crédit Mistral, comptez ~2-5€/mois selon utilisation.

---

## 🐛 Résolution de problèmes courants

### Erreur "API key not configured"
→ Vérifiez que les variables d'environnement sont bien définies dans `.env` (local) et sur Render

### Le micro ne fonctionne pas sur iOS
→ Vérifiez que GROQ_API_KEY est bien configuré sur Render

### La voix lit "point d'exclamation"
→ Vérifié : le code nettoie maintenant les emojis avant la lecture

### Les mots de vocabulaire ne s'affichent pas
→ Vérifiez dans la console du navigateur (F12) si le JSON est bien parsé

### Le serveur ne démarre pas
→ Vérifiez que toutes les dépendances sont installées : `pip install -r requirements.txt`

---

## 🎓 Améliorations possibles (exercices)

1. **Ajouter un bouton "Répéter"** pour réécouter le dernier message
2. **Sauvegarder l'historique** avec localStorage
3. **Ajouter des thèmes** (mode sombre/clair)
4. **Statistiques d'apprentissage** : nombre de mots appris, temps de conversation
5. **Export de vocabulaire** en PDF ou CSV
6. **Mode conversation guidée** avec des suggestions de sujets

---

## 📚 Ressources complémentaires

- [Documentation Mistral AI](https://docs.mistral.ai/)
- [Documentation Groq](https://console.groq.com/docs)
- [Web Speech API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Speech_API)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Render Documentation](https://render.com/docs)

---

## ✅ Checklist finale

- [ ] Comptes créés (Mistral, Groq, Render, GitHub)
- [ ] Clés API obtenues et sauvegardées
- [ ] Code téléchargé et configuré
- [ ] Test en local réussi
- [ ] Repository GitHub créé
- [ ] Déploiement sur Render effectué
- [ ] Test sur mobile iOS/Android réussi
- [ ] Application accessible via URL publique

---

## 🎉 Félicitations !

Vous avez créé un chatbot conversationnel multilingue avec IA, reconnaissance vocale et déployé sur le web, le tout **gratuitement** ! 

Ce projet combine des technologies modernes (IA, APIs REST, déploiement cloud) et peut servir de base pour d'autres projets similaires dans d'autres langues.

**Καλή επιτυχία!** (Bonne chance !) 🇬🇷





---
Powered by [Claude Exporter](https://www.claudexporter.com)