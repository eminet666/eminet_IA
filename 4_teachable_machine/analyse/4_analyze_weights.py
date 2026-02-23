#!/usr/bin/env python3
"""
Script pour analyser le fichier weights.bin
ATTENTION: Ce script nécessite que weights.bin soit présent
"""
import json
import struct
import numpy as np
from pathlib import Path


def analyze_weights_bin(weights_path, model_path):
    """Analyse le fichier binaire des poids"""
    
    # Charger la structure des poids depuis model.json
    with open(model_path, 'r') as f:
        model_data = json.load(f)
    
    # Charger les données binaires
    with open(weights_path, 'rb') as f:
        weights_data = f.read()
    
    print("=" * 80)
    print("ANALYSE DES POIDS DU MODÈLE (weights.bin)")
    print("=" * 80)
    
    print(f"\n📦 Informations sur le fichier:")
    print(f"  • Taille du fichier: {len(weights_data):,} octets ({len(weights_data) / (1024**2):.2f} MB)")
    
    # Extraire les spécifications des poids
    weights_manifest = model_data.get('weightsManifest', [])
    
    offset = 0
    weight_arrays = []
    
    print(f"\n⚖️  Extraction des tenseurs de poids:\n")
    
    for manifest in weights_manifest:
        for weight_spec in manifest.get('weights', []):
            name = weight_spec['name']
            shape = weight_spec['shape']
            dtype = weight_spec['dtype']
            
            # Calculer le nombre d'éléments
            num_elements = np.prod(shape)
            
            # Taille en octets (float32 = 4 octets)
            if dtype == 'float32':
                bytes_size = num_elements * 4
                
                # Extraire les données
                chunk = weights_data[offset:offset + bytes_size]
                
                # Convertir en array numpy
                values = struct.unpack(f'{num_elements}f', chunk)
                array = np.array(values).reshape(shape)
                
                # Statistiques
                weight_arrays.append({
                    'name': name,
                    'shape': shape,
                    'array': array,
                    'min': np.min(array),
                    'max': np.max(array),
                    'mean': np.mean(array),
                    'std': np.std(array),
                    'size_bytes': bytes_size
                })
                
                offset += bytes_size
    
    print(f"  • Nombre de tenseurs extraits: {len(weight_arrays)}")
    print(f"  • Octets traités: {offset:,} / {len(weights_data):,}")
    
    # Afficher les statistiques des poids importants
    print(f"\n📊 STATISTIQUES DES PRINCIPAUX TENSEURS:\n")
    
    # Filtrer les poids de kernels/weights (pas les biais ou batch norm)
    kernel_weights = [w for w in weight_arrays if 'kernel' in w['name'].lower() or 
                     ('dense' in w['name'].lower() and 'kernel' in w['name'])]
    
    print(f"{'Nom du tenseur':<55} | {'Shape':<20} | {'Min':>10} | {'Max':>10} | {'Mean':>10} | {'Std':>10}")
    print("─" * 130)
    
    for weight in kernel_weights[:20]:  # Afficher les 20 premiers
        shape_str = 'x'.join(map(str, weight['shape']))
        print(f"{weight['name']:<55} | {shape_str:<20} | "
              f"{weight['min']:>10.4f} | {weight['max']:>10.4f} | "
              f"{weight['mean']:>10.4f} | {weight['std']:>10.4f}")
    
    # Analyse de la distribution des poids
    print(f"\n📈 ANALYSE DE LA DISTRIBUTION DES POIDS:\n")
    
    all_kernel_values = np.concatenate([w['array'].flatten() for w in kernel_weights])
    
    print(f"  • Nombre total de paramètres (kernels): {len(all_kernel_values):,}")
    print(f"  • Valeur minimale: {np.min(all_kernel_values):.6f}")
    print(f"  • Valeur maximale: {np.max(all_kernel_values):.6f}")
    print(f"  • Moyenne: {np.mean(all_kernel_values):.6f}")
    print(f"  • Écart-type: {np.std(all_kernel_values):.6f}")
    print(f"  • Médiane: {np.median(all_kernel_values):.6f}")
    
    # Percentiles
    percentiles = [1, 5, 25, 50, 75, 95, 99]
    print(f"\n  Percentiles:")
    for p in percentiles:
        value = np.percentile(all_kernel_values, p)
        print(f"    {p:3d}%: {value:>10.6f}")
    
    # Analyse des couches de classification
    print(f"\n🎯 COUCHES DE CLASSIFICATION FINALE:\n")
    
    classification_layers = [w for w in weight_arrays if 'dense' in w['name'].lower()]
    
    for layer in classification_layers:
        shape_str = 'x'.join(map(str, layer['shape']))
        print(f"  • {layer['name']}")
        print(f"    Shape: {shape_str}")
        print(f"    Range: [{layer['min']:.4f}, {layer['max']:.4f}]")
        print(f"    Mean: {layer['mean']:.4f}, Std: {layer['std']:.4f}")
        
        # Si c'est la dernière couche (2 classes), afficher les poids complets
        if layer['shape'] == [100, 2] or layer['shape'] == [2]:
            print(f"    Valeurs complètes:")
            print(f"{layer['array']}")
        print()
    
    print("=" * 80)
    
    return weight_arrays


def export_weights_to_numpy(weight_arrays, output_dir="./extracted_weights"):
    """Exporte les poids en fichiers .npy pour réutilisation"""
    
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    print(f"\n💾 Export des poids en fichiers .npy...")
    
    for weight in weight_arrays:
        safe_name = weight['name'].replace('/', '_')
        file_path = output_path / f"{safe_name}.npy"
        np.save(file_path, weight['array'])
    
    print(f"  ✓ {len(weight_arrays)} fichiers exportés dans {output_dir}")
    
    # Créer un fichier d'index
    index = {
        w['name']: {
            'filename': w['name'].replace('/', '_') + '.npy',
            'shape': w['shape'],
            'dtype': 'float32'
        }
        for w in weight_arrays
    }
    
    with open(output_path / 'index.json', 'w') as f:
        json.dump(index, f, indent=2)
    
    print(f"  ✓ Fichier d'index créé: {output_dir}/index.json")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        model_dir = Path(sys.argv[1])
        weights_path = model_dir / "weights.bin"
        model_path = model_dir / "model.json"
    else:
        weights_path = "/mnt/user-data/uploads/weights.bin"
        model_path = "/mnt/user-data/uploads/model.json"
        print(f"ℹ️  Aucun dossier spécifié, utilisation des chemins par défaut\n")
    
    # Vérifier que le fichier existe
    if not Path(weights_path).exists():
        print("❌ ERREUR: Le fichier weights.bin n'est pas trouvé.")
        print(f"   Recherché dans: {weights_path}")
        print("   Veuillez uploader le fichier weights.bin pour exécuter ce script.")
    else:
        weight_arrays = analyze_weights_bin(weights_path, model_path)
        
        # Optionnel: exporter les poids
        export_choice = input("\nVoulez-vous exporter les poids en fichiers .npy? (y/n): ")
        if export_choice.lower() == 'y':
            # Utiliser un chemin relatif au script
            script_dir = Path(__file__).parent
            output_dir = script_dir / "extracted_weights"
            export_weights_to_numpy(weight_arrays, str(output_dir))
            print(f"\n✓ Les poids ont été exportés dans: {output_dir.absolute()}")
