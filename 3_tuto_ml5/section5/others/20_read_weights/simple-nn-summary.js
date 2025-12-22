const fs = require('fs');

// Chemins vers vos fichiers
const MODEL_JSON_PATH = './model/model.json';
const OUTPUT_FILE = './nn_summary.txt';

function summarizeNeuralNetwork() {
  console.log('🔍 Analyse du réseau de neurones...\n');

  // Lire le fichier model.json
  const modelJson = JSON.parse(fs.readFileSync(MODEL_JSON_PATH, 'utf8'));
  
  // Préparer le contenu de sortie
  let output = '═══════════════════════════════════════════\n';
  output += '    RÉSUMÉ DU RÉSEAU DE NEURONES\n';
  output += '═══════════════════════════════════════════\n\n';
  
  // Différentes structures possibles
  let layers = null;
  
  // Structure 1 : modelTopology.config (Sequential - tableau direct)
  if (modelJson.modelTopology?.config && Array.isArray(modelJson.modelTopology.config)) {
    layers = modelJson.modelTopology.config;
  }
  // Structure 2 : modelTopology.model_config.config.layers
  else if (modelJson.modelTopology?.model_config?.config?.layers) {
    layers = modelJson.modelTopology.model_config.config.layers;
  }
  // Structure 3 : modelTopology.config.layers
  else if (modelJson.modelTopology?.config?.layers) {
    layers = modelJson.modelTopology.config.layers;
  }
  // Structure 4 : modelTopology.layers
  else if (modelJson.modelTopology?.layers) {
    layers = modelJson.modelTopology.layers;
  }
  // Structure 5 : config.layers (ml5.js peut avoir cette structure)
  else if (modelJson.config?.layers) {
    layers = modelJson.config.layers;
  }
  // Structure 6 : layers directement
  else if (modelJson.layers) {
    layers = modelJson.layers;
  }
  
  if (layers) {
    
    // Identifier les couches input, hidden et output
    let inputLayers = 0;
    let hiddenLayers = 0;
    let outputLayers = 0;
    let neuronsPerLayer = [];
    
    layers.forEach((layer, index) => {
      const type = layer.class_name;
      const config = layer.config;
      
      // Pour la première couche Dense avec batch_input_shape, c'est l'input
      if (type === 'Dense' && config.batch_input_shape && index === 0) {
        inputLayers++;
        
        // Nombre de neurones d'entrée
        const inputSize = config.batch_input_shape[config.batch_input_shape.length - 1];
        neuronsPerLayer.push({
          name: config.name,
          type: 'Input',
          neurons: inputSize || 0
        });
        
        // La première couche Dense est aussi une Hidden layer
        hiddenLayers++;
        neuronsPerLayer.push({
          name: config.name,
          type: 'Hidden',
          neurons: config.units || 0
        });
      }
      // La dernière couche Dense est l'output
      else if (type === 'Dense' && index === layers.length - 1) {
        outputLayers++;
        neuronsPerLayer.push({
          name: config.name,
          type: 'Output',
          neurons: config.units || 0
        });
      }
      // Les autres couches Dense sont des hidden layers
      else if (type === 'Dense') {
        hiddenLayers++;
        neuronsPerLayer.push({
          name: config.name,
          type: 'Hidden',
          neurons: config.units || 0
        });
      }
      // InputLayer explicite
      else if (type === 'InputLayer') {
        inputLayers++;
        if (config.batch_input_shape) {
          const inputSize = config.batch_input_shape[config.batch_input_shape.length - 1];
          neuronsPerLayer.push({
            name: config.name,
            type: 'Input',
            neurons: inputSize || 0
          });
        }
      }
      // Autres types de couches avec neurones/unités
      else if (type === 'LSTM' || type === 'GRU') {
        hiddenLayers++;
        neuronsPerLayer.push({
          name: config.name,
          type: 'Hidden',
          neurons: config.units || 0
        });
      }
    });
    
    // Affichage console
    console.log('📊 ARCHITECTURE');
    console.log(`   Couches d'entrée (Input):  ${inputLayers}`);
    console.log(`   Couches cachées (Hidden):  ${hiddenLayers}`);
    console.log(`   Couches de sortie (Output): ${outputLayers}`);
    console.log(`   ─────────────────────────────`);
    console.log(`   TOTAL:                      ${inputLayers + hiddenLayers + outputLayers}`);
    
    console.log('\n🔢 NEURONES PAR COUCHE');
    neuronsPerLayer.forEach((layer, index) => {
      console.log(`   Couche ${index + 1} (${layer.type}): ${layer.neurons} neurones`);
    });
    
    // Écriture dans le fichier
    output += 'ARCHITECTURE\n';
    output += '─────────────────────────────────────────\n';
    output += `Couches d'entrée (Input):   ${inputLayers}\n`;
    output += `Couches cachées (Hidden):   ${hiddenLayers}\n`;
    output += `Couches de sortie (Output): ${outputLayers}\n`;
    output += `─────────────────────────────────────────\n`;
    output += `TOTAL:                      ${inputLayers + hiddenLayers + outputLayers}\n\n`;
    
    output += 'NEURONES PAR COUCHE\n';
    output += '─────────────────────────────────────────\n';
    neuronsPerLayer.forEach((layer, index) => {
      output += `Couche ${index + 1} (${layer.type.padEnd(6)}): ${layer.neurons.toString().padStart(4)} neurones\n`;
    });
    
    // Calcul du total de neurones
    const totalNeurons = neuronsPerLayer.reduce((sum, layer) => sum + layer.neurons, 0);
    output += `─────────────────────────────────────────\n`;
    output += `TOTAL:                      ${totalNeurons.toString().padStart(4)} neurones\n`;
    
    console.log(`   ─────────────────────────────`);
    console.log(`   TOTAL:                      ${totalNeurons} neurones`);
    
  } else {
    output += 'Erreur: Structure du modèle non reconnue.\n';
    output += 'Veuillez partager les premières lignes de votre model.json pour diagnostic.\n';
    console.log('❌ Structure du modèle non reconnue.');
    console.log('\n🔍 Diagnostic de la structure:');
    console.log('   modelTopology existe:', !!modelJson.modelTopology);
    console.log('   modelTopology.model_config existe:', !!modelJson.modelTopology?.model_config);
    console.log('   modelTopology.config existe:', !!modelJson.modelTopology?.config);
    console.log('   modelTopology.layers existe:', !!modelJson.modelTopology?.layers);
    console.log('   config existe:', !!modelJson.config);
    console.log('   layers existe:', !!modelJson.layers);
    console.log('\n📋 Clés principales du JSON:');
    console.log('  ', Object.keys(modelJson).join(', '));
    if (modelJson.modelTopology) {
      console.log('\n📋 Clés de modelTopology:');
      console.log('  ', Object.keys(modelJson.modelTopology).join(', '));
    }
  }
  
  // Sauvegarder dans le fichier
  fs.writeFileSync(OUTPUT_FILE, output, 'utf8');
  
  console.log(`\n✅ Résumé sauvegardé dans: ${OUTPUT_FILE}`);
}

// Exécution
try {
  summarizeNeuralNetwork();
} catch (error) {
  console.error('❌ Erreur:', error.message);
  console.error('\n💡 Assurez-vous que le fichier model.json existe dans le même dossier.');
}