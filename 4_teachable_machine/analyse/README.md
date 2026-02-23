# Scripts d'Analyse pour Modèles Teachable Machine

Ce dossier contient une suite de scripts Python pour analyser en profondeur vos modèles créés avec [Teachable Machine](https://teachablemachine.withgoogle.com/).

## 📦 Fichiers Fournis

### Scripts d'Analyse

1. **`1_analyze_metadata.py`** - Analyse des métadonnées du modèle
2. **`2_analyze_model_architecture.py`** - Analyse détaillée de l'architecture
3. **`3_visualize_network.py`** - Visualisation du flux du réseau
4. **`4_analyze_weights.py`** - Analyse des poids (nécessite weights.bin)
5. **`5_generate_report.py`** - Génération d'un rapport Markdown complet
6. **`run_all_analysis.py`** - Script principal qui exécute tous les autres

### Documentation

- **`rapport_analyse_modele.md`** - Rapport complet généré automatiquement

## 🚀 Utilisation

### Prérequis

```bash
# Python 3.7 ou supérieur
python3 --version

# Installer numpy (pour l'analyse des poids)
pip install numpy
```

### Utilisation Basique

**Syntaxe générale :** Tous les scripts acceptent le **dossier du modèle** en paramètre.

```bash
# Syntaxe
python3 script.py /chemin/vers/dossier_modele
```

#### Option 1: Exécuter tous les scripts

```bash
# Avec le dossier par défaut
python3 run_all_analysis.py

# Avec votre dossier
python3 run_all_analysis.py /chemin/vers/mon_modele
```

Ce script exécute toutes les analyses dans l'ordre et génère un rapport complet.

#### Option 2: Exécuter les scripts individuellement

```bash
# Avec le dossier par défaut (/mnt/user-data/uploads)
python3 1_analyze_metadata.py
python3 2_analyze_model_architecture.py
python3 3_visualize_network.py
python3 4_analyze_weights.py
python3 5_generate_report.py

# Avec votre dossier personnalisé
python3 1_analyze_metadata.py /chemin/vers/mon_modele
python3 2_analyze_model_architecture.py /chemin/vers/mon_modele
python3 3_visualize_network.py /chemin/vers/mon_modele
python3 4_analyze_weights.py /chemin/vers/mon_modele
python3 5_generate_report.py /chemin/vers/mon_modele
```

**Exemples concrets :**

```bash
# Si vos fichiers sont dans ~/Downloads/mon_modele/
python3 1_analyze_metadata.py ~/Downloads/mon_modele

# Si vos fichiers sont dans /Users/jean/Documents/modele_chats_chiens/
python3 run_all_analysis.py /Users/jean/Documents/modele_chats_chiens

# Utiliser le chemin par défaut (sans paramètre)
python3 1_analyze_metadata.py
```

## 📂 Structure des Fichiers Teachable Machine

Votre modèle Teachable Machine est composé de 3 fichiers:

```
mon_modele/
├── metadata.json    # Métadonnées (classes, taille d'entrée, etc.)
├── model.json      # Architecture du réseau (couches, connexions)
└── weights.bin     # Poids entraînés (paramètres du modèle)
```

## 📊 Ce que Font les Scripts

### 1. Analyse des Métadonnées
- Nom du modèle
- Version des frameworks (TensorFlow.js, Teachable Machine)
- Classes de classification
- Taille des images d'entrée
- Date de création

### 2. Analyse de l'Architecture
- Type de modèle (Sequential, MobileNet)
- Nombre et types de couches
- Nombre total de paramètres
- Taille du modèle
- Top 10 des plus gros tenseurs

### 3. Visualisation du Réseau
- Flux complet du réseau
- Séparation par étapes (entrée, convolutions, pooling, classification)
- Détails de chaque couche importante

### 4. Analyse des Poids (nécessite weights.bin)
- Extraction des valeurs des poids
- Statistiques (min, max, moyenne, écart-type)
- Distribution des valeurs
- Analyse de la couche de classification
- Export optionnel en fichiers .npy

### 5. Génération de Rapport
- Rapport Markdown complet et structuré
- Toutes les informations importantes
- Exemples de code JavaScript et Python
- Instructions de conversion et d'utilisation

## 🔧 Personnalisation

### Exporter les Poids en NumPy

Le script `4_analyze_weights.py` peut exporter tous les poids en fichiers `.npy`:

```python
# Dans le script, décommenter ou appeler:
export_weights_to_numpy(weight_arrays, "./extracted_weights")
```

Cela créera un dossier avec:
- Un fichier `.npy` par tenseur
- Un fichier `index.json` avec les métadonnées

## 💡 Cas d'Usage

### 1. Comprendre votre Modèle
Utilisez ces scripts pour comprendre comment fonctionne votre modèle Teachable Machine.

### 2. Déboguer les Performances
Analysez les poids et l'architecture pour identifier les problèmes potentiels.

### 3. Documenter votre Projet
Générez automatiquement un rapport complet pour votre documentation.

### 4. Convertir pour Python
Utilisez les informations pour convertir et utiliser le modèle avec TensorFlow Python.

### 5. Optimiser le Modèle
Identifiez les couches les plus lourdes pour optimiser ou compresser le modèle.

## 🐍 Exemples d'Utilisation Avancée

### Charger et Utiliser les Poids en Python

```python
import numpy as np
import json

# Charger l'index
with open('extracted_weights/index.json') as f:
    index = json.load(f)

# Charger un poids spécifique
dense_kernel = np.load('extracted_weights/dense_Dense2_kernel.npy')
print(f"Shape: {dense_kernel.shape}")
print(f"Poids: {dense_kernel}")
```

### Analyser une Couche Spécifique

```python
import json

with open('model.json') as f:
    model = json.load(f)

# Trouver toutes les couches Dense
for manifest in model['weightsManifest']:
    for weight in manifest['weights']:
        if 'dense' in weight['name'].lower():
            print(f"{weight['name']}: {weight['shape']}")
```

## 🔍 Informations Techniques

### Architecture MobileNetV2
Le modèle utilise MobileNetV2, une architecture optimisée pour:
- Appareils mobiles et embarqués
- Navigateurs web (TensorFlow.js)
- Faible consommation de mémoire
- Inférence rapide

### Convolutions Séparables en Profondeur
MobileNet utilise des convolutions depthwise separable qui:
- Réduisent le nombre de paramètres
- Accélèrent les calculs
- Maintiennent une bonne précision

### Transfer Learning
Le modèle est pré-entraîné sur ImageNet puis ajusté pour votre tâche spécifique.

## 📚 Ressources Utiles

- [Documentation Teachable Machine](https://teachablemachine.withgoogle.com/)
- [TensorFlow.js](https://www.tensorflow.org/js)
- [MobileNetV2 Paper](https://arxiv.org/abs/1801.04381)
- [Convertir TFJS vers Keras](https://www.tensorflow.org/js/guide/conversion)

## 🐛 Dépannage

### Erreur: "Module numpy not found"
```bash
pip install numpy
```

### Erreur: "File weights.bin not found"
Le script 4 nécessite le fichier `weights.bin`. Téléchargez-le depuis Teachable Machine.

### Erreur: "Invalid JSON"
Vérifiez que les fichiers JSON ne sont pas corrompus et sont bien formés.

## 📝 Notes

- Ces scripts ont été testés avec Python 3.8+
- Compatible avec tous les modèles Teachable Machine (Image)
- Les poids sont stockés en float32 (4 octets par valeur)
- La taille totale des poids dépend du nombre de paramètres

## 🤝 Contribution

N'hésitez pas à modifier et améliorer ces scripts selon vos besoins!

## 📄 Licence

Scripts fournis à des fins éducatives. Libre d'utilisation et de modification.

---

**Créé pour vous aider à mieux comprendre vos modèles Teachable Machine! 🚀**
