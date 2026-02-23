# Guide Rapide - Scripts d'Analyse Teachable Machine

## 🚀 Utilisation en 3 secondes

### Analyser un modèle dans un dossier spécifique :
```bash
python3 run_all_analysis.py /chemin/vers/mon_modele
```

### Analyser le modèle par défaut (sans paramètre) :
```bash
python3 run_all_analysis.py
```

## 📂 Structure attendue du dossier

Votre dossier doit contenir :
```
mon_modele/
├── metadata.json    ✅ Obligatoire
├── model.json      ✅ Obligatoire  
└── weights.bin     ⚠️  Optionnel (pour script 4)
```

## 🎯 Scripts individuels

Tous les scripts suivent la même syntaxe :

```bash
# Avec dossier personnalisé
python3 1_analyze_metadata.py /chemin/vers/mon_modele
python3 2_analyze_model_architecture.py /chemin/vers/mon_modele
python3 3_visualize_network.py /chemin/vers/mon_modele
python3 4_analyze_weights.py /chemin/vers/mon_modele
python3 5_generate_report.py /chemin/vers/mon_modele

# Sans paramètre (utilise /mnt/user-data/uploads par défaut)
python3 1_analyze_metadata.py
python3 2_analyze_model_architecture.py
# etc...
```

## 💡 Exemples concrets

```bash
# Modèle dans ~/Downloads/modele_chiens_chats/
python3 run_all_analysis.py ~/Downloads/modele_chiens_chats

# Modèle dans le dossier courant
python3 run_all_analysis.py .

# Modèle dans /tmp/mon_modele/
python3 1_analyze_metadata.py /tmp/mon_modele
python3 2_analyze_model_architecture.py /tmp/mon_modele
```

## 📊 Résultats

- **Scripts 1-4** : Affichage console
- **Script 5** : Génère `rapport_analyse_modele.md` dans `/mnt/user-data/outputs/`
- **Script 6** : Lance tous les scripts + génère le rapport

## ⚠️ Important

- Si aucun dossier n'est spécifié → utilise `/mnt/user-data/uploads/` par défaut
- Le dossier doit contenir au minimum `metadata.json` et `model.json`
- `weights.bin` est optionnel (uniquement pour le script 4)

## 🆘 En cas d'erreur

```bash
# Vérifier que les fichiers existent
ls -la /chemin/vers/mon_modele

# Le dossier doit contenir au moins :
metadata.json
model.json
```
