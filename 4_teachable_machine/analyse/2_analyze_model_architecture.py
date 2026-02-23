#!/usr/bin/env python3
"""
Script pour analyser l'architecture du modèle Teachable Machine
"""
import json
from collections import Counter


def analyze_model_architecture(model_path):
    """Analyse le fichier model.json pour comprendre l'architecture"""
    
    with open(model_path, 'r') as f:
        model_data = json.load(f)
    
    print("=" * 60)
    print("ANALYSE DE L'ARCHITECTURE DU MODÈLE")
    print("=" * 60)
    
    # Architecture du modèle
    topology = model_data['modelTopology']
    print(f"\n🏗️  Type de modèle: {topology['class_name']}")
    
    # Analyse des couches
    layers = []
    
    def extract_layers(config):
        """Extrait récursivement toutes les couches"""
        if 'layers' in config:
            for layer in config['layers']:
                if 'class_name' in layer:
                    layers.append(layer['class_name'])
                if 'config' in layer:
                    extract_layers(layer['config'])
    
    extract_layers(topology['config'])
    
    # Comptage des types de couches
    layer_counts = Counter(layers)
    
    print(f"\n📊 Statistiques des couches:")
    print(f"  • Nombre total de couches: {len(layers)}")
    print(f"\n  Répartition par type:")
    for layer_type, count in layer_counts.most_common():
        print(f"    - {layer_type}: {count}")
    
    # Analyse des poids
    print(f"\n⚖️  Informations sur les poids:")
    weights_manifest = model_data.get('weightsManifest', [])
    
    total_params = 0
    weight_info = []
    
    for manifest in weights_manifest:
        for weight in manifest.get('weights', []):
            name = weight['name']
            shape = weight['shape']
            dtype = weight['dtype']
            
            # Calcul du nombre de paramètres
            params = 1
            for dim in shape:
                params *= dim
            
            total_params += params
            weight_info.append({
                'name': name,
                'shape': shape,
                'params': params,
                'dtype': dtype
            })
    
    print(f"  • Nombre de tenseurs de poids: {len(weight_info)}")
    print(f"  • Nombre total de paramètres: {total_params:,}")
    print(f"  • Taille estimée (float32): {total_params * 4 / (1024**2):.2f} MB")
    
    # Afficher les 10 plus gros tenseurs
    print(f"\n📦 Les 10 plus gros tenseurs de poids:")
    sorted_weights = sorted(weight_info, key=lambda x: x['params'], reverse=True)[:10]
    
    for i, weight in enumerate(sorted_weights, 1):
        shape_str = 'x'.join(map(str, weight['shape']))
        print(f"  {i:2d}. {weight['name']:<50} | {shape_str:>15} | {weight['params']:>10,} params")
    
    # Analyse de la structure MobileNet
    print(f"\n🔍 Détails de l'architecture MobileNet:")
    mobilenet_layers = [l for l in layers if 'block' in l.lower() or 'conv' in l.lower()]
    print(f"  • Couches convolutionnelles/blocks: {len(mobilenet_layers)}")
    
    # Couches de classification
    dense_weights = [w for w in weight_info if 'dense' in w['name'].lower()]
    if dense_weights:
        print(f"\n🎯 Couches de classification:")
        for weight in dense_weights:
            shape_str = 'x'.join(map(str, weight['shape']))
            print(f"  • {weight['name']}: {shape_str}")
    
    print("\n" + "=" * 60)
    
    return model_data, weight_info


if __name__ == "__main__":
    import sys
    from pathlib import Path
    
    if len(sys.argv) > 1:
        model_dir = Path(sys.argv[1])
        model_path = model_dir / "model.json"
    else:
        model_path = "/mnt/user-data/uploads/model.json"
        print(f"ℹ️  Aucun dossier spécifié, utilisation du chemin par défaut: {model_path}\n")
    
    analyze_model_architecture(model_path)
