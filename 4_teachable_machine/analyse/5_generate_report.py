#!/usr/bin/env python3
"""
Génère un rapport complet en Markdown sur le modèle Teachable Machine
"""
import json
from datetime import datetime
from pathlib import Path


def generate_report(metadata_path, model_path, output_path):
    """Génère un rapport Markdown complet"""
    
    # Charger les données
    with open(metadata_path, 'r') as f:
        metadata = json.load(f)
    
    with open(model_path, 'r') as f:
        model_data = json.load(f)
    
    # Début du rapport
    report = []
    report.append("# Rapport d'Analyse du Modèle Teachable Machine")
    report.append("")
    report.append(f"*Généré le {datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}*")
    report.append("")
    report.append("---")
    report.append("")
    
    # Section 1: Métadonnées
    report.append("## 1. Métadonnées du Modèle")
    report.append("")
    report.append(f"- **Nom du modèle**: `{metadata.get('modelName')}`")
    report.append(f"- **Package**: {metadata.get('packageName')} v{metadata.get('packageVersion')}")
    report.append(f"- **TensorFlow.js**: v{metadata.get('tfjsVersion')}")
    report.append(f"- **Teachable Machine**: v{metadata.get('tmVersion')}")
    
    timestamp = metadata.get('timeStamp')
    if timestamp:
        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        report.append(f"- **Date de création**: {dt.strftime('%d/%m/%Y à %H:%M:%S')}")
    
    report.append("")
    
    # Classes
    report.append("### Classes de Classification")
    report.append("")
    labels = metadata.get('labels', [])
    for i, label in enumerate(labels):
        report.append(f"- **Classe {i}**: {label}")
    
    report.append("")
    report.append(f"**Taille d'entrée**: {metadata.get('imageSize')}×{metadata.get('imageSize')} pixels (RGB)")
    report.append("")
    report.append("---")
    report.append("")
    
    # Section 2: Architecture
    report.append("## 2. Architecture du Réseau")
    report.append("")
    
    # Compter les couches
    layers = []
    
    def extract_layers(config):
        if 'layers' in config:
            for layer in config['layers']:
                if 'class_name' in layer:
                    layers.append(layer['class_name'])
                if 'config' in layer:
                    extract_layers(layer['config'])
    
    topology = model_data['modelTopology']
    extract_layers(topology['config'])
    
    from collections import Counter
    layer_counts = Counter(layers)
    
    report.append(f"**Type de modèle**: {topology['class_name']} (MobileNetV2 + Classificateur)")
    report.append("")
    report.append(f"**Nombre total de couches**: {len(layers)}")
    report.append("")
    
    report.append("### Répartition des Couches")
    report.append("")
    report.append("| Type de Couche | Nombre |")
    report.append("|---------------|--------|")
    for layer_type, count in layer_counts.most_common():
        report.append(f"| {layer_type} | {count} |")
    
    report.append("")
    report.append("---")
    report.append("")
    
    # Section 3: Paramètres
    report.append("## 3. Paramètres du Modèle")
    report.append("")
    
    weights_manifest = model_data.get('weightsManifest', [])
    
    total_params = 0
    weight_info = []
    
    for manifest in weights_manifest:
        for weight in manifest.get('weights', []):
            name = weight['name']
            shape = weight['shape']
            
            params = 1
            for dim in shape:
                params *= dim
            
            total_params += params
            weight_info.append({
                'name': name,
                'shape': shape,
                'params': params
            })
    
    report.append(f"- **Nombre total de paramètres**: {total_params:,}")
    report.append(f"- **Nombre de tenseurs**: {len(weight_info)}")
    report.append(f"- **Taille du modèle (float32)**: ~{total_params * 4 / (1024**2):.2f} MB")
    report.append("")
    
    report.append("### Top 10 des Plus Gros Tenseurs")
    report.append("")
    report.append("| Rang | Nom du Tenseur | Shape | Paramètres |")
    report.append("|------|---------------|-------|------------|")
    
    sorted_weights = sorted(weight_info, key=lambda x: x['params'], reverse=True)[:10]
    for i, weight in enumerate(sorted_weights, 1):
        shape_str = '×'.join(map(str, weight['shape']))
        report.append(f"| {i} | `{weight['name']}` | {shape_str} | {weight['params']:,} |")
    
    report.append("")
    report.append("---")
    report.append("")
    
    # Section 4: Architecture détaillée
    report.append("## 4. Flux du Réseau de Neurones")
    report.append("")
    report.append("### Pipeline de Traitement")
    report.append("")
    report.append("```")
    report.append("Image (224×224×3)")
    report.append("    ↓")
    report.append("Convolution Initiale (16 filtres)")
    report.append("    ↓")
    report.append("Blocs MobileNet ×16")
    report.append("  • Convolutions séparables en profondeur")
    report.append("  • Batch Normalization + ReLU6")
    report.append("  • Connexions résiduelles")
    report.append("    ↓")
    report.append("Convolution finale (1280 filtres)")
    report.append("    ↓")
    report.append("Global Average Pooling")
    report.append("    ↓")
    report.append("Dense (1280 → 100) + ReLU")
    report.append("    ↓")
    report.append("Dense (100 → 2) + Softmax")
    report.append("    ↓")
    report.append("Prédiction [P(Cats), P(Dogs)]")
    report.append("```")
    report.append("")
    report.append("---")
    report.append("")
    
    # Section 5: Caractéristiques de MobileNet
    report.append("## 5. Caractéristiques du Modèle")
    report.append("")
    report.append("### MobileNetV2")
    report.append("")
    report.append("Ce modèle utilise l'architecture **MobileNetV2**, optimisée pour:")
    report.append("")
    report.append("- ✅ **Efficacité**: Peu de paramètres (~538k) pour une bonne précision")
    report.append("- ✅ **Rapidité**: Convolutions séparables en profondeur (depthwise separable)")
    report.append("- ✅ **Mobilité**: Adapté aux appareils mobiles et navigateurs web")
    report.append("- ✅ **Transfer Learning**: Pré-entraîné sur ImageNet puis ajusté pour votre tâche")
    report.append("")
    
    report.append("### Innovations de MobileNet")
    report.append("")
    report.append("1. **Depthwise Separable Convolutions**: Séparation des convolutions spatiales et en canaux")
    report.append("2. **Inverted Residuals**: Expansion puis compression des canaux")
    report.append("3. **Linear Bottlenecks**: Préservation de l'information dans les couches de projection")
    report.append("4. **ReLU6**: Activation bornée pour meilleure stabilité numérique")
    report.append("")
    report.append("---")
    report.append("")
    
    # Section 6: Utilisation
    report.append("## 6. Utilisation du Modèle")
    report.append("")
    
    report.append("### Prérequis")
    report.append("")
    report.append("```bash")
    report.append("# Installation de TensorFlow.js")
    report.append("npm install @tensorflow/tfjs")
    report.append("npm install @teachablemachine/image")
    report.append("```")
    report.append("")
    
    report.append("### Exemple de Code (JavaScript)")
    report.append("")
    report.append("```javascript")
    report.append("// Charger le modèle")
    report.append("const modelURL = './model.json';")
    report.append("const model = await tmImage.load(modelURL, './metadata.json');")
    report.append("")
    report.append("// Prédire sur une image")
    report.append("const predictions = await model.predict(imageElement);")
    report.append("")
    report.append("// Afficher les résultats")
    report.append("predictions.forEach(pred => {")
    report.append("    console.log(`${pred.className}: ${(pred.probability * 100).toFixed(2)}%`);")
    report.append("});")
    report.append("```")
    report.append("")
    
    report.append("### Exemple de Code (Python)")
    report.append("")
    report.append("```python")
    report.append("import tensorflow as tf")
    report.append("import numpy as np")
    report.append("from PIL import Image")
    report.append("")
    report.append("# Charger le modèle (après conversion)")
    report.append("model = tf.keras.models.load_model('converted_model')")
    report.append("")
    report.append("# Prétraiter l'image")
    report.append("img = Image.open('test_image.jpg').resize((224, 224))")
    report.append("img_array = np.array(img) / 255.0")
    report.append("img_array = np.expand_dims(img_array, axis=0)")
    report.append("")
    report.append("# Prédiction")
    report.append("predictions = model.predict(img_array)")
    report.append("classes = ['Cats', 'Dogs']")
    report.append("predicted_class = classes[np.argmax(predictions)]")
    report.append("confidence = np.max(predictions) * 100")
    report.append("")
    report.append(f"print(f'Prédiction: {{predicted_class}} ({{confidence:.2f}}%)')")
    report.append("```")
    report.append("")
    report.append("---")
    report.append("")
    
    # Section 7: Conversion
    report.append("## 7. Conversion du Modèle")
    report.append("")
    report.append("Pour utiliser ce modèle avec TensorFlow Python, vous devez le convertir:")
    report.append("")
    report.append("```bash")
    report.append("# Installer le convertisseur")
    report.append("pip install tensorflowjs")
    report.append("")
    report.append("# Convertir le modèle")
    report.append("tensorflowjs_converter \\")
    report.append("    --input_format=tfjs_layers_model \\")
    report.append("    --output_format=keras \\")
    report.append("    model.json \\")
    report.append("    converted_model/")
    report.append("```")
    report.append("")
    report.append("---")
    report.append("")
    
    # Section 8: Optimisations possibles
    report.append("## 8. Optimisations Possibles")
    report.append("")
    report.append("1. **Quantization**: Réduire la précision des poids (float32 → int8) pour diminuer la taille")
    report.append("2. **Pruning**: Supprimer les connexions peu importantes")
    report.append("3. **Knowledge Distillation**: Entraîner un modèle plus petit à imiter ce modèle")
    report.append("4. **Data Augmentation**: Améliorer la généralisation avec plus de variations d'entraînement")
    report.append("5. **Fine-tuning**: Ré-entraîner les dernières couches sur plus de données")
    report.append("")
    report.append("---")
    report.append("")
    
    # Conclusion
    report.append("## 9. Conclusion")
    report.append("")
    report.append(f"Ce modèle Teachable Machine utilise MobileNetV2 pour classifier des images entre **{' et '.join(labels)}**.")
    report.append("")
    report.append("**Points forts:**")
    report.append("- Architecture légère et efficace")
    report.append("- Compatible navigateur web et mobile")
    report.append("- Facile à déployer et à utiliser")
    report.append("")
    report.append("**Limitations:**")
    report.append("- Limité à 2 classes actuellement")
    report.append("- Performances dépendant de la qualité des données d'entraînement")
    report.append("- Nécessite des images 224×224 pixels")
    report.append("")
    report.append("---")
    report.append("")
    report.append("*Rapport généré automatiquement par les scripts d'analyse Python*")
    
    # Écrire le rapport
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report))
    
    print(f"✓ Rapport généré: {output_path}")
    return output_path


if __name__ == "__main__":
    import sys
    from pathlib import Path
    
    if len(sys.argv) > 1:
        model_dir = Path(sys.argv[1])
        metadata_path = model_dir / "metadata.json"
        model_path = model_dir / "model.json"
        output_path = "/mnt/user-data/outputs/rapport_analyse_modele.md"
    else:
        metadata_path = "/mnt/user-data/uploads/metadata.json"
        model_path = "/mnt/user-data/uploads/model.json"
        output_path = "/mnt/user-data/outputs/rapport_analyse_modele.md"
        print(f"ℹ️  Aucun dossier spécifié, utilisation des chemins par défaut\n")
    
    generate_report(metadata_path, model_path, output_path)
