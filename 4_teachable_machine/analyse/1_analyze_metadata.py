#!/usr/bin/env python3
"""
Script pour analyser les métadonnées d'un modèle Teachable Machine
"""
import json
from datetime import datetime
from pathlib import Path


def analyze_metadata(metadata_path):
    """Analyse le fichier metadata.json"""
    
    with open(metadata_path, 'r') as f:
        metadata = json.load(f)
    
    print("=" * 60)
    print("ANALYSE DES MÉTADONNÉES DU MODÈLE")
    print("=" * 60)
    
    print("\n📦 Informations générales:")
    print(f"  • Nom du modèle: {metadata.get('modelName', 'N/A')}")
    print(f"  • Package: {metadata.get('packageName', 'N/A')}")
    print(f"  • Version package: {metadata.get('packageVersion', 'N/A')}")
    
    print("\n🔧 Versions des frameworks:")
    print(f"  • TensorFlow.js: {metadata.get('tfjsVersion', 'N/A')}")
    print(f"  • Teachable Machine: {metadata.get('tmVersion', 'N/A')}")
    
    print("\n📅 Date de création:")
    timestamp = metadata.get('timeStamp')
    if timestamp:
        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        print(f"  • {dt.strftime('%d/%m/%Y à %H:%M:%S')}")
    
    print("\n🏷️  Classes identifiées:")
    labels = metadata.get('labels', [])
    for i, label in enumerate(labels):
        print(f"  • Classe {i}: {label}")
    
    print(f"\n🖼️  Taille des images d'entrée:")
    image_size = metadata.get('imageSize', 'N/A')
    print(f"  • {image_size}x{image_size} pixels")
    
    print("\n" + "=" * 60)
    
    return metadata


if __name__ == "__main__":
    import sys
    from pathlib import Path
    
    if len(sys.argv) > 1:
        model_dir = Path(sys.argv[1])
        metadata_path = model_dir / "metadata.json"
    else:
        metadata_path = "/mnt/user-data/uploads/metadata.json"
        print(f"ℹ️  Aucun dossier spécifié, utilisation du chemin par défaut: {metadata_path}\n")
    
    analyze_metadata(metadata_path)
