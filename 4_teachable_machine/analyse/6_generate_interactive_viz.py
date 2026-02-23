#!/usr/bin/env python3
"""
Génère une visualisation interactive HTML du réseau de neurones Teachable Machine
"""
import json
import numpy as np
from pathlib import Path
from collections import defaultdict


def extract_network_structure(model_path):
    """Extrait la structure du réseau depuis model.json"""
    
    # Convertir en Path pour gérer correctement les chemins Windows/Linux
    model_path = Path(model_path)
    
    with open(model_path, 'r') as f:
        model_data = json.load(f)
    
    topology = model_data['modelTopology']
    
    # Extraire toutes les couches avec leurs connexions
    layers_data = []
    
    def extract_layers_recursive(config, parent_name=None, depth=0):
        if 'layers' in config:
            for idx, layer in enumerate(config['layers']):
                class_name = layer.get('class_name', 'Unknown')
                layer_config = layer.get('config', {})
                layer_name = layer_config.get('name', f'layer_{idx}')
                
                # Extraire les paramètres importants
                layer_info = {
                    'name': layer_name,
                    'type': class_name,
                    'depth': depth,
                    'parent': parent_name
                }
                
                # Ajouter des paramètres spécifiques selon le type
                if class_name == 'Conv2D':
                    layer_info['filters'] = layer_config.get('filters')
                    layer_info['kernel_size'] = layer_config.get('kernel_size')
                    layer_info['strides'] = layer_config.get('strides')
                elif class_name == 'DepthwiseConv2D':
                    layer_info['kernel_size'] = layer_config.get('kernel_size')
                    layer_info['strides'] = layer_config.get('strides')
                elif class_name == 'Dense':
                    layer_info['units'] = layer_config.get('units')
                    layer_info['activation'] = layer_config.get('activation', 'linear')
                elif class_name == 'InputLayer':
                    layer_info['input_shape'] = layer_config.get('batch_input_shape')
                elif class_name == 'BatchNormalization':
                    layer_info['axis'] = layer_config.get('axis')
                
                # Extraire les connexions entrantes
                inbound = layer.get('inbound_nodes', [])
                if inbound:
                    layer_info['inputs'] = []
                    for connection in inbound:
                        if connection:
                            for conn in connection:
                                if isinstance(conn, list) and len(conn) > 0:
                                    layer_info['inputs'].append(conn[0])
                
                layers_data.append(layer_info)
                
                # Récursion
                if 'config' in layer:
                    extract_layers_recursive(layer['config'], layer_name, depth + 1)
    
    extract_layers_recursive(topology['config'])
    
    return layers_data


def extract_weights_info(model_path):
    """Extrait les informations sur les poids"""
    
    # Convertir en Path pour gérer correctement les chemins Windows/Linux
    model_path = Path(model_path)
    
    with open(model_path, 'r') as f:
        model_data = json.load(f)
    
    weights_info = []
    weights_manifest = model_data.get('weightsManifest', [])
    
    for manifest in weights_manifest:
        for weight in manifest.get('weights', []):
            name = weight['name']
            shape = weight['shape']
            
            params = np.prod(shape)
            
            weights_info.append({
                'name': name,
                'shape': shape,
                'params': int(params),
                'layer': name.split('/')[0] if '/' in name else name
            })
    
    return weights_info


def generate_visualization_html(model_path, metadata_path, output_path):
    """Génère le fichier HTML de visualisation"""
    
    # Convertir en Path pour gérer correctement les chemins Windows/Linux
    model_path = Path(model_path)
    metadata_path = Path(metadata_path)
    output_path = Path(output_path)
    
    # Charger les données
    layers = extract_network_structure(model_path)
    weights = extract_weights_info(model_path)
    
    with open(metadata_path, 'r') as f:
        metadata = json.load(f)
    
    # Grouper les couches par type
    layers_by_type = defaultdict(list)
    for layer in layers:
        layers_by_type[layer['type']].append(layer)
    
    # Calculer les statistiques
    total_params = sum(w['params'] for w in weights)
    
    # Générer le HTML
    html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Visualisation Réseau - {metadata.get('modelName')}</title>
    <script src="https://cdn.jsdelivr.net/npm/d3@7"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;600;700&family=Space+Grotesk:wght@300;500;700&display=swap');
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        :root {{
            --bg-primary: #0a0e27;
            --bg-secondary: #1a1f3a;
            --bg-tertiary: #252b4a;
            --accent-1: #00d4ff;
            --accent-2: #7c3aed;
            --accent-3: #ec4899;
            --text-primary: #e0e7ff;
            --text-secondary: #94a3b8;
            --border: #2d3558;
        }}
        
        body {{
            font-family: 'Space Grotesk', sans-serif;
            background: linear-gradient(135deg, var(--bg-primary) 0%, #0f1629 100%);
            color: var(--text-primary);
            min-height: 100vh;
            overflow-x: hidden;
        }}
        
        .grain {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            pointer-events: none;
            opacity: 0.03;
            background-image: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" width="300" height="300"><filter id="noise"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="4" /></filter><rect width="100%" height="100%" filter="url(%23noise)" /></svg>');
            z-index: 1000;
        }}
        
        header {{
            padding: 2rem 3rem;
            background: rgba(26, 31, 58, 0.4);
            backdrop-filter: blur(20px);
            border-bottom: 1px solid var(--border);
            position: sticky;
            top: 0;
            z-index: 100;
        }}
        
        h1 {{
            font-size: 2.5rem;
            font-weight: 700;
            background: linear-gradient(135deg, var(--accent-1) 0%, var(--accent-2) 50%, var(--accent-3) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5rem;
            letter-spacing: -0.02em;
        }}
        
        .subtitle {{
            color: var(--text-secondary);
            font-size: 1rem;
            font-family: 'JetBrains Mono', monospace;
        }}
        
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1.5rem;
            padding: 2rem 3rem;
            margin-bottom: 2rem;
        }}
        
        .stat-card {{
            background: linear-gradient(135deg, var(--bg-secondary) 0%, var(--bg-tertiary) 100%);
            padding: 1.5rem;
            border-radius: 16px;
            border: 1px solid var(--border);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }}
        
        .stat-card:hover {{
            transform: translateY(-4px);
            border-color: var(--accent-1);
            box-shadow: 0 20px 60px rgba(0, 212, 255, 0.1);
        }}
        
        .stat-label {{
            font-size: 0.875rem;
            color: var(--text-secondary);
            font-family: 'JetBrains Mono', monospace;
            margin-bottom: 0.5rem;
            text-transform: uppercase;
            letter-spacing: 0.1em;
        }}
        
        .stat-value {{
            font-size: 2rem;
            font-weight: 700;
            color: var(--accent-1);
        }}
        
        .controls {{
            padding: 0 3rem 2rem;
            display: flex;
            gap: 1rem;
            flex-wrap: wrap;
        }}
        
        .btn {{
            padding: 0.75rem 1.5rem;
            background: var(--bg-secondary);
            border: 1px solid var(--border);
            color: var(--text-primary);
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.875rem;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.2s;
            font-weight: 500;
        }}
        
        .btn:hover {{
            background: var(--accent-1);
            color: var(--bg-primary);
            border-color: var(--accent-1);
            transform: translateY(-2px);
        }}
        
        .btn.active {{
            background: linear-gradient(135deg, var(--accent-2) 0%, var(--accent-3) 100%);
            border-color: var(--accent-2);
        }}
        
        .visualization {{
            padding: 0 3rem 3rem;
        }}
        
        #network-viz {{
            background: var(--bg-secondary);
            border: 1px solid var(--border);
            border-radius: 16px;
            overflow: hidden;
        }}
        
        .layer-node {{
            cursor: pointer;
            transition: all 0.3s;
        }}
        
        .layer-node:hover {{
            filter: brightness(1.3);
        }}
        
        .layer-label {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 11px;
            fill: var(--text-primary);
            pointer-events: none;
        }}
        
        .connection {{
            stroke: var(--accent-1);
            stroke-opacity: 0.2;
            fill: none;
            transition: all 0.3s;
        }}
        
        .connection.highlighted {{
            stroke-opacity: 0.8;
            stroke-width: 2;
        }}
        
        .tooltip {{
            position: absolute;
            background: rgba(26, 31, 58, 0.95);
            backdrop-filter: blur(20px);
            border: 1px solid var(--accent-1);
            border-radius: 8px;
            padding: 1rem;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.875rem;
            pointer-events: none;
            opacity: 0;
            transition: opacity 0.2s;
            z-index: 1000;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
        }}
        
        .tooltip.show {{
            opacity: 1;
        }}
        
        .layer-detail {{
            padding: 2rem 3rem;
            background: var(--bg-secondary);
            border-radius: 16px;
            margin: 2rem 3rem;
            border: 1px solid var(--border);
        }}
        
        .layer-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 1rem;
            margin-top: 1rem;
        }}
        
        .layer-item {{
            background: var(--bg-tertiary);
            padding: 1rem;
            border-radius: 8px;
            border-left: 3px solid var(--accent-2);
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.75rem;
        }}
        
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        .fade-in {{
            animation: fadeIn 0.6s cubic-bezier(0.4, 0, 0.2, 1) forwards;
        }}
    </style>
</head>
<body>
    <div class="grain"></div>
    
    <header>
        <h1>Visualisation du Réseau de Neurones</h1>
        <div class="subtitle">{metadata.get('modelName')} • MobileNetV2 • {len(metadata.get('labels', []))} classes</div>
    </header>
    
    <div class="stats">
        <div class="stat-card fade-in" style="animation-delay: 0.1s">
            <div class="stat-label">Total Couches</div>
            <div class="stat-value">{len(layers)}</div>
        </div>
        <div class="stat-card fade-in" style="animation-delay: 0.2s">
            <div class="stat-label">Paramètres</div>
            <div class="stat-value">{total_params:,}</div>
        </div>
        <div class="stat-card fade-in" style="animation-delay: 0.3s">
            <div class="stat-label">Taille Entrée</div>
            <div class="stat-value">{metadata.get('imageSize')}×{metadata.get('imageSize')}</div>
        </div>
        <div class="stat-card fade-in" style="animation-delay: 0.4s">
            <div class="stat-label">Classes</div>
            <div class="stat-value">{' • '.join(metadata.get('labels', []))}</div>
        </div>
    </div>
    
    <div class="controls">
        <button class="btn active" onclick="showView('flow')">Vue Flux</button>
        <button class="btn" onclick="showView('layers')">Par Type de Couche</button>
        <button class="btn" onclick="showView('weights')">Poids & Paramètres</button>
    </div>
    
    <div class="visualization">
        <svg id="network-viz" width="100%" height="800"></svg>
    </div>
    
    <div id="layer-details"></div>
    
    <div class="tooltip"></div>
    
    <script>
        // Vérifier que D3 est chargé
        if (typeof d3 === 'undefined') {{
            document.body.innerHTML = '<div style="padding: 2rem; text-align: center; color: #ef4444;"><h1>Erreur de chargement</h1><p>La bibliothèque D3.js n\\'a pas pu être chargée. Vérifiez votre connexion Internet.</p></div>';
            throw new Error('D3.js not loaded');
        }}
        
        // Données du réseau
        const layers = {json.dumps(layers, indent=2)};
        const weights = {json.dumps(weights, indent=2)};
        const metadata = {json.dumps(metadata, indent=2)};
        
        let currentView = 'flow';
        
        // Couleurs par type de couche
        const layerColors = {{
            'InputLayer': '#00d4ff',
            'Conv2D': '#7c3aed',
            'DepthwiseConv2D': '#ec4899',
            'BatchNormalization': '#f59e0b',
            'ReLU': '#10b981',
            'Dense': '#ef4444',
            'GlobalAveragePooling2D': '#8b5cf6',
            'Add': '#06b6d4',
            'ZeroPadding2D': '#64748b',
            'Sequential': '#6366f1',
            'Model': '#14b8a6'
        }};
        
        function showView(view) {{
            currentView = view;
            
            // Update button states
            document.querySelectorAll('.btn').forEach(btn => btn.classList.remove('active'));
            event.target.classList.add('active');
            
            // Clear current visualization
            d3.select('#network-viz').selectAll('*').remove();
            d3.select('#layer-details').html('');
            
            // Show appropriate view
            if (view === 'flow') {{
                visualizeFlow();
            }} else if (view === 'layers') {{
                visualizeByLayerType();
            }} else if (view === 'weights') {{
                visualizeWeights();
            }}
        }}
        
        function visualizeFlow() {{
            const svg = d3.select('#network-viz');
            const width = parseInt(svg.style('width'));
            const height = 800;
            
            // Filter important layers for visualization
            const importantTypes = ['InputLayer', 'Conv2D', 'DepthwiseConv2D', 'Dense', 'GlobalAveragePooling2D'];
            const visibleLayers = layers.filter(l => importantTypes.includes(l.type));
            
            const layerHeight = height / (visibleLayers.length + 2);
            
            const g = svg.append('g');
            
            // Draw connections first
            visibleLayers.forEach((layer, i) => {{
                if (i > 0) {{
                    g.append('path')
                        .attr('class', 'connection')
                        .attr('d', `M ${{width/2}},${{(i)*layerHeight + 50}} L ${{width/2}},${{(i+1)*layerHeight + 50}}`)
                        .attr('stroke-width', 1.5);
                }}
            }});
            
            // Draw layers
            visibleLayers.forEach((layer, i) => {{
                const y = (i+1) * layerHeight;
                
                // Node
                const node = g.append('g')
                    .attr('class', 'layer-node')
                    .attr('transform', `translate(${{width/2}},${{y}})`);
                
                const radius = layer.type === 'Dense' ? 40 : 30;
                
                node.append('circle')
                    .attr('r', radius)
                    .attr('fill', layerColors[layer.type] || '#666')
                    .attr('opacity', 0.8)
                    .attr('stroke', '#fff')
                    .attr('stroke-width', 2);
                
                // Label
                node.append('text')
                    .attr('class', 'layer-label')
                    .attr('y', radius + 20)
                    .attr('text-anchor', 'middle')
                    .text(layer.type);
                
                // Add hover tooltip
                node.on('mouseover', function(event) {{
                    showTooltip(event, layer);
                }})
                .on('mouseout', hideTooltip);
            }});
        }}
        
        function visualizeByLayerType() {{
            const svg = d3.select('#network-viz');
            const width = parseInt(svg.style('width'));
            const height = 800;
            
            // Group layers by type
            const layersByType = {{}};
            layers.forEach(layer => {{
                if (!layersByType[layer.type]) layersByType[layer.type] = [];
                layersByType[layer.type].push(layer);
            }});
            
            const types = Object.keys(layersByType);
            const columnWidth = width / types.length;
            
            const g = svg.append('g');
            
            types.forEach((type, typeIdx) => {{
                const typeLayers = layersByType[type];
                const x = typeIdx * columnWidth + columnWidth/2;
                
                // Type header
                g.append('text')
                    .attr('x', x)
                    .attr('y', 30)
                    .attr('text-anchor', 'middle')
                    .attr('fill', layerColors[type] || '#666')
                    .attr('font-size', '14px')
                    .attr('font-weight', 'bold')
                    .attr('font-family', 'JetBrains Mono')
                    .text(`${{type}} (${{typeLayers.length}})`);
                
                // Draw each layer
                const layerSpacing = (height - 100) / (typeLayers.length + 1);
                
                typeLayers.forEach((layer, idx) => {{
                    const y = 80 + (idx + 1) * layerSpacing;
                    
                    const node = g.append('g')
                        .attr('class', 'layer-node')
                        .attr('transform', `translate(${{x}},${{y}})`);
                    
                    node.append('circle')
                        .attr('r', 8)
                        .attr('fill', layerColors[type] || '#666')
                        .attr('opacity', 0.8);
                    
                    node.on('mouseover', function(event) {{
                        showTooltip(event, layer);
                    }})
                    .on('mouseout', hideTooltip);
                }});
            }});
        }}
        
        function visualizeWeights() {{
            const svg = d3.select('#network-viz');
            const width = parseInt(svg.style('width'));
            const height = 800;
            
            // Sort weights by size
            const sortedWeights = [...weights].sort((a, b) => b.params - a.params).slice(0, 30);
            
            const maxParams = Math.max(...sortedWeights.map(w => w.params));
            const g = svg.append('g').attr('transform', 'translate(50, 50)');
            
            const barHeight = (height - 100) / sortedWeights.length;
            
            sortedWeights.forEach((weight, i) => {{
                const barWidth = (weight.params / maxParams) * (width - 300);
                const y = i * barHeight;
                
                // Bar
                g.append('rect')
                    .attr('x', 200)
                    .attr('y', y)
                    .attr('width', barWidth)
                    .attr('height', barHeight - 2)
                    .attr('fill', `hsl(${{240 + (i * 120 / sortedWeights.length)}}, 80%, 60%)`)
                    .attr('opacity', 0.8)
                    .attr('rx', 4);
                
                // Label
                g.append('text')
                    .attr('x', 0)
                    .attr('y', y + barHeight/2)
                    .attr('fill', '#e0e7ff')
                    .attr('font-size', '10px')
                    .attr('font-family', 'JetBrains Mono')
                    .attr('dominant-baseline', 'middle')
                    .text(weight.name.substring(0, 25));
                
                // Value
                g.append('text')
                    .attr('x', 210 + barWidth)
                    .attr('y', y + barHeight/2)
                    .attr('fill', '#00d4ff')
                    .attr('font-size', '10px')
                    .attr('font-family', 'JetBrains Mono')
                    .attr('dominant-baseline', 'middle')
                    .text(weight.params.toLocaleString());
            }});
        }}
        
        function showTooltip(event, layer) {{
            const tooltip = d3.select('.tooltip');
            
            let content = `<strong>${{layer.name}}</strong><br>`;
            content += `Type: ${{layer.type}}<br>`;
            
            if (layer.filters) content += `Filtres: ${{layer.filters}}<br>`;
            if (layer.kernel_size) content += `Kernel: ${{layer.kernel_size.join('×')}}<br>`;
            if (layer.units) content += `Units: ${{layer.units}}<br>`;
            if (layer.activation) content += `Activation: ${{layer.activation}}<br>`;
            
            tooltip.html(content)
                .style('left', (event.pageX + 10) + 'px')
                .style('top', (event.pageY + 10) + 'px')
                .classed('show', true);
        }}
        
        function hideTooltip() {{
            d3.select('.tooltip').classed('show', false);
        }}
        
        // Initialize
        visualizeFlow();
    </script>
</body>
</html>"""
    
    # Écrire le fichier
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✓ Visualisation générée: {output_path}")
    return output_path


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        model_dir = Path(sys.argv[1])
        model_path = model_dir / "model.json"
        metadata_path = model_dir / "metadata.json"
    else:
        model_path = "/mnt/user-data/uploads/model.json"
        metadata_path = "/mnt/user-data/uploads/metadata.json"
        print(f"ℹ️  Aucun dossier spécifié, utilisation des chemins par défaut\n")
    
    # Générer dans le même dossier que le script
    script_dir = Path(__file__).parent
    output_path = script_dir / "network_visualization.html"
    
    generate_visualization_html(model_path, metadata_path, str(output_path))
    print(f"\n🌐 Ouvrez le fichier dans votre navigateur pour explorer le réseau!")
    print(f"   Chemin: {output_path.absolute()}")
