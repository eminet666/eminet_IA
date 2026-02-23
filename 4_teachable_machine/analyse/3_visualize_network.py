#!/usr/bin/env python3
"""
Script pour visualiser l'architecture du réseau de neurones
"""
import json


def visualize_network_flow(model_path):
    """Crée une représentation visuelle du flux du réseau"""
    
    with open(model_path, 'r') as f:
        model_data = json.load(f)
    
    print("=" * 80)
    print("VISUALISATION DU FLUX DU RÉSEAU DE NEURONES")
    print("=" * 80)
    
    # Extraction des couches principales
    topology = model_data['modelTopology']
    
    def extract_layer_sequence(config, depth=0):
        """Extrait la séquence de couches avec indentation"""
        layers_info = []
        
        if 'layers' in config:
            for layer in config['layers']:
                class_name = layer.get('class_name', 'Unknown')
                layer_config = layer.get('config', {})
                layer_name = layer_config.get('name', 'unnamed')
                
                # Informations spécifiques selon le type
                info = ""
                if class_name == 'Conv2D':
                    filters = layer_config.get('filters', '?')
                    kernel = layer_config.get('kernel_size', '?')
                    strides = layer_config.get('strides', '?')
                    info = f"filters={filters}, kernel={kernel}, strides={strides}"
                elif class_name == 'DepthwiseConv2D':
                    kernel = layer_config.get('kernel_size', '?')
                    strides = layer_config.get('strides', '?')
                    info = f"kernel={kernel}, strides={strides}"
                elif class_name == 'Dense':
                    units = layer_config.get('units', '?')
                    activation = layer_config.get('activation', 'linear')
                    info = f"units={units}, activation={activation}"
                elif class_name == 'InputLayer':
                    shape = layer_config.get('batch_input_shape', '?')
                    info = f"shape={shape}"
                elif class_name == 'Dropout':
                    rate = layer_config.get('rate', '?')
                    info = f"rate={rate}"
                
                layers_info.append({
                    'depth': depth,
                    'class': class_name,
                    'name': layer_name,
                    'info': info
                })
                
                # Récursion
                if 'config' in layer:
                    layers_info.extend(extract_layer_sequence(layer['config'], depth + 1))
        
        return layers_info
    
    layers = extract_layer_sequence(topology['config'])
    
    # Filtrer pour ne garder que les couches importantes
    important_types = [
        'InputLayer', 'Conv2D', 'DepthwiseConv2D', 'Dense', 
        'GlobalAveragePooling2D', 'Dropout', 'Flatten'
    ]
    
    print("\n📊 FLUX PRINCIPAL DU RÉSEAU:\n")
    
    current_stage = ""
    stage_counter = 0
    
    for i, layer in enumerate(layers):
        if layer['class'] not in important_types:
            continue
        
        # Détection des différentes sections
        if 'input' in layer['name'].lower():
            current_stage = "ENTRÉE"
            stage_counter += 1
            print(f"\n{'─' * 80}")
            print(f"  ÉTAPE {stage_counter}: {current_stage}")
            print(f"{'─' * 80}")
        elif 'Conv1' in layer['name'] and 'block' not in layer['name']:
            current_stage = "CONVOLUTION INITIALE"
            stage_counter += 1
            print(f"\n{'─' * 80}")
            print(f"  ÉTAPE {stage_counter}: {current_stage}")
            print(f"{'─' * 80}")
        elif 'block_1_' in layer['name'] and current_stage != "BLOCS MOBILENET":
            current_stage = "BLOCS MOBILENET"
            stage_counter += 1
            print(f"\n{'─' * 80}")
            print(f"  ÉTAPE {stage_counter}: {current_stage}")
            print(f"{'─' * 80}")
        elif 'global' in layer['name'].lower():
            current_stage = "POOLING GLOBAL"
            stage_counter += 1
            print(f"\n{'─' * 80}")
            print(f"  ÉTAPE {stage_counter}: {current_stage}")
            print(f"{'─' * 80}")
        elif 'dense' in layer['name'].lower() and current_stage != "CLASSIFICATION":
            current_stage = "CLASSIFICATION"
            stage_counter += 1
            print(f"\n{'─' * 80}")
            print(f"  ÉTAPE {stage_counter}: {current_stage}")
            print(f"{'─' * 80}")
        
        # Affichage de la couche
        indent = "  " * (layer['depth'] + 1)
        arrow = "└──>" if layer['depth'] > 0 else "──>"
        
        print(f"{indent}{arrow} {layer['class']:<25} | {layer['name']:<35} | {layer['info']}")
    
    print(f"\n{'─' * 80}\n")
    
    # Résumé
    print("📝 RÉSUMÉ DE L'ARCHITECTURE:")
    print("  1. Entrée: Image 224x224x3 (RGB)")
    print("  2. Convolution initiale: Extraction des caractéristiques de base")
    print("  3. Blocs MobileNet: 16 blocs de convolutions efficaces (depthwise separable)")
    print("  4. Pooling global: Réduction spatiale pour obtenir un vecteur")
    print("  5. Classification: Couches denses pour prédire Chats vs Chiens")
    print("  6. Sortie: Probabilités pour 2 classes\n")
    
    print("=" * 80)


if __name__ == "__main__":
    import sys
    from pathlib import Path
    
    if len(sys.argv) > 1:
        model_dir = Path(sys.argv[1])
        model_path = model_dir / "model.json"
    else:
        model_path = "/mnt/user-data/uploads/model.json"
        print(f"ℹ️  Aucun dossier spécifié, utilisation du chemin par défaut: {model_path}\n")
    
    visualize_network_flow(model_path)
