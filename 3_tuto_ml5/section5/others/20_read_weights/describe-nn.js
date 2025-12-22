const fs = require('fs');

// Chemins vers vos fichiers
const MODEL_JSON_PATH = './model/model.json';
const OUTPUT_FILE = './nn.txt';

function describeNeuralNetwork() {
  console.log('🔍 Lecture de l\'architecture du réseau de neurones...\n');

  // Lire le fichier model.json
  const modelJson = JSON.parse(fs.readFileSync(MODEL_JSON_PATH, 'utf8'));
  
  // Préparer le contenu de sortie
  let output = '═══════════════════════════════════════════════════════\n';
  output += '        ARCHITECTURE DU RÉSEAU DE NEURONES\n';
  output += '═══════════════════════════════════════════════════════\n\n';
  
  // Informations générales
  if (modelJson.modelTopology) {
    const topology = modelJson.modelTopology;
    
    output += `Format: ${modelJson.format || 'Non spécifié'}\n`;
    output += `Version TensorFlow.js: ${modelJson.generatedBy || 'Non spécifié'}\n`;
    output += `Convertie depuis: ${modelJson.convertedBy || 'Non spécifié'}\n`;
    
    if (topology.model_config) {
      const config = topology.model_config;
      output += `Type de modèle: ${config.class_name || 'Non spécifié'}\n`;
      output += `Nom du modèle: ${topology.model_config.config?.name || 'Non spécifié'}\n\n`;
    }
    
    output += '───────────────────────────────────────────────────────\n';
    output += '                    COUCHES DU RÉSEAU\n';
    output += '───────────────────────────────────────────────────────\n\n';
    
    console.log('📊 STRUCTURE DU RÉSEAU:\n');
    
    // Parcourir les couches
    if (topology.model_config && topology.model_config.config && topology.model_config.config.layers) {
      const layers = topology.model_config.config.layers;
      
      layers.forEach((layer, index) => {
        const layerNum = index + 1;
        const layerType = layer.class_name;
        const layerName = layer.config.name;
        const config = layer.config;
        
        console.log(`\n🔷 Couche ${layerNum}: ${layerName}`);
        console.log(`   Type: ${layerType}`);
        
        output += `\n┌─ COUCHE ${layerNum}: ${layerName}\n`;
        output += `│  Type: ${layerType}\n`;
        
        // Informations spécifiques selon le type de couche
        switch(layerType) {
          case 'Dense':
            if (config.units) {
              console.log(`   Neurones: ${config.units}`);
              output += `│  Nombre de neurones: ${config.units}\n`;
            }
            if (config.activation) {
              console.log(`   Activation: ${config.activation}`);
              output += `│  Fonction d'activation: ${config.activation}\n`;
            }
            if (config.use_bias !== undefined) {
              output += `│  Utilise un biais: ${config.use_bias}\n`;
            }
            break;
            
          case 'InputLayer':
            if (config.batch_input_shape) {
              console.log(`   Forme d'entrée: [${config.batch_input_shape.join(', ')}]`);
              output += `│  Forme d'entrée (batch_input_shape): [${config.batch_input_shape.join(', ')}]\n`;
            }
            if (config.dtype) {
              output += `│  Type de données: ${config.dtype}\n`;
            }
            break;
            
          case 'Conv2D':
          case 'Conv1D':
            if (config.filters) {
              console.log(`   Filtres: ${config.filters}`);
              output += `│  Nombre de filtres: ${config.filters}\n`;
            }
            if (config.kernel_size) {
              console.log(`   Taille du noyau: [${config.kernel_size.join(', ')}]`);
              output += `│  Taille du noyau: [${config.kernel_size.join(', ')}]\n`;
            }
            if (config.strides) {
              output += `│  Strides: [${config.strides.join(', ')}]\n`;
            }
            if (config.padding) {
              output += `│  Padding: ${config.padding}\n`;
            }
            if (config.activation) {
              console.log(`   Activation: ${config.activation}`);
              output += `│  Fonction d'activation: ${config.activation}\n`;
            }
            break;
            
          case 'MaxPooling2D':
          case 'MaxPooling1D':
          case 'AveragePooling2D':
            if (config.pool_size) {
              console.log(`   Taille du pool: [${config.pool_size.join(', ')}]`);
              output += `│  Taille du pool: [${config.pool_size.join(', ')}]\n`;
            }
            if (config.strides) {
              output += `│  Strides: [${config.strides.join(', ')}]\n`;
            }
            break;
            
          case 'Dropout':
            if (config.rate) {
              console.log(`   Taux de dropout: ${config.rate}`);
              output += `│  Taux de dropout: ${config.rate}\n`;
            }
            break;
            
          case 'Flatten':
            output += `│  (Aplatit les entrées en 1D)\n`;
            break;
            
          case 'LSTM':
          case 'GRU':
            if (config.units) {
              console.log(`   Unités: ${config.units}`);
              output += `│  Nombre d'unités: ${config.units}\n`;
            }
            if (config.return_sequences !== undefined) {
              output += `│  Retourne les séquences: ${config.return_sequences}\n`;
            }
            if (config.activation) {
              output += `│  Fonction d'activation: ${config.activation}\n`;
            }
            break;
        }
        
        // Informations supplémentaires communes
        if (config.trainable !== undefined) {
          output += `│  Entraînable: ${config.trainable}\n`;
        }
        
        // Informations sur les connexions
        if (layer.inbound_nodes && layer.inbound_nodes.length > 0) {
          const connections = layer.inbound_nodes[0].map(node => node[0]).join(', ');
          output += `│  Connecté à: ${connections}\n`;
        }
        
        output += `└─────────────────────────────────────────────────────\n`;
      });
      
      // Résumé
      output += `\n═══════════════════════════════════════════════════════\n`;
      output += `                      RÉSUMÉ\n`;
      output += `═══════════════════════════════════════════════════════\n\n`;
      output += `Nombre total de couches: ${layers.length}\n`;
      
      // Identifier les couches input, hidden et output
      let inputLayers = 0;
      let hiddenLayers = 0;
      let outputLayers = 0;
      let neuronsPerLayer = [];
      
      layers.forEach((layer, index) => {
        const type = layer.class_name;
        const config = layer.config;
        
        // Compter input layers
        if (type === 'InputLayer') {
          inputLayers++;
        }
        // La dernière couche Dense est généralement l'output
        else if (type === 'Dense' && index === layers.length - 1) {
          outputLayers++;
        }
        // Les autres couches Dense sont des hidden layers
        else if (type === 'Dense') {
          hiddenLayers++;
        }
        
        // Collecter le nombre de neurones par couche
        if (type === 'Dense' || type === 'LSTM' || type === 'GRU') {
          neuronsPerLayer.push({
            name: config.name,
            type: type,
            neurons: config.units || 0,
            layerIndex: index + 1
          });
        } else if (type === 'InputLayer' && config.batch_input_shape) {
          // Pour les input layers, prendre la dernière dimension
          const inputSize = config.batch_input_shape[config.batch_input_shape.length - 1];
          neuronsPerLayer.push({
            name: config.name,
            type: type,
            neurons: inputSize || 0,
            layerIndex: index + 1
          });
        } else if (type === 'Conv2D' || type === 'Conv1D') {
          neuronsPerLayer.push({
            name: config.name,
            type: type,
            neurons: config.filters || 0,
            layerIndex: index + 1
          });
        }
      });
      
      output += `\n--- ARCHITECTURE DU RÉSEAU ---\n`;
      output += `Couches d'entrée (Input): ${inputLayers}\n`;
      output += `Couches cachées (Hidden): ${hiddenLayers}\n`;
      output += `Couches de sortie (Output): ${outputLayers}\n`;
      
      output += `\n--- NEURONES PAR COUCHE ---\n`;
      neuronsPerLayer.forEach(layer => {
        output += `Couche ${layer.layerIndex} (${layer.name} - ${layer.type}): ${layer.neurons} neurones/unités\n`;
      });
      
      console.log(`\n📈 RÉSUMÉ:`);
      console.log(`   Nombre total de couches: ${layers.length}`);
      console.log(`   - Couches d'entrée (Input): ${inputLayers}`);
      console.log(`   - Couches cachées (Hidden): ${hiddenLayers}`);
      console.log(`   - Couches de sortie (Output): ${outputLayers}`);
      
      console.log(`\n   Neurones par couche:`);
      neuronsPerLayer.forEach(layer => {
        console.log(`     Couche ${layer.layerIndex} (${layer.name}): ${layer.neurons}`);
      });
      
      // Compter les types de couches
      const layerTypes = {};
      layers.forEach(layer => {
        const type = layer.class_name;
        layerTypes[type] = (layerTypes[type] || 0) + 1;
      });
      
      output += `\n--- RÉPARTITION PAR TYPE ---\n`;
      console.log(`\n   Répartition par type:`);
      
      Object.entries(layerTypes).forEach(([type, count]) => {
        output += `  - ${type}: ${count}\n`;
        console.log(`     - ${type}: ${count}`);
      });
    }
  }
  
  // Informations sur les poids
  if (modelJson.weightsManifest) {
    output += `\n───────────────────────────────────────────────────────\n`;
    output += `                  INFORMATIONS SUR LES POIDS\n`;
    output += `───────────────────────────────────────────────────────\n\n`;
    
    let totalParams = 0;
    modelJson.weightsManifest.forEach(manifest => {
      manifest.weights.forEach(weight => {
        const numElements = weight.shape.reduce((a, b) => a * b, 1);
        totalParams += numElements;
        output += `${weight.name}:\n`;
        output += `  Shape: [${weight.shape.join(', ')}]\n`;
        output += `  Type: ${weight.dtype}\n`;
        output += `  Paramètres: ${numElements.toLocaleString()}\n\n`;
      });
    });
    
    output += `Nombre total de paramètres: ${totalParams.toLocaleString()}\n`;
    console.log(`\n🔢 Nombre total de paramètres: ${totalParams.toLocaleString()}`);
  }
  
  // Sauvegarder dans le fichier
  fs.writeFileSync(OUTPUT_FILE, output, 'utf8');
  
  console.log(`\n✅ Architecture sauvegardée dans: ${OUTPUT_FILE}`);
  console.log(`📁 Taille du fichier: ${(fs.statSync(OUTPUT_FILE).size / 1024).toFixed(2)} KB`);
}

// Exécution
try {
  describeNeuralNetwork();
} catch (error) {
  console.error('❌ Erreur:', error.message);
  console.error('\n💡 Assurez-vous que le fichier model.json existe dans le même dossier.');
  console.error('Stack trace:', error.stack);
}