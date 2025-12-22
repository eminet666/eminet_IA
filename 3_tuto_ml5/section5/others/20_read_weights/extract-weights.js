const fs = require('fs');
const path = require('path');

// Chemins vers vos fichiers
const MODEL_JSON_PATH = './model/model.json';
const WEIGHTS_BIN_PATH = './model/model.weights.bin';
const OUTPUT_FILE = './weights.txt';

function extractWeights() {
  console.log('🔍 Lecture du modèle...\n');

  // 1. Lire le fichier model.json pour obtenir la structure
  const modelJson = JSON.parse(fs.readFileSync(MODEL_JSON_PATH, 'utf8'));
  
  // 2. Lire le fichier .bin de façon synchrone
  const buffer = fs.readFileSync(WEIGHTS_BIN_PATH);
  const float32Array = new Float32Array(buffer.buffer);
  
  console.log(`📊 Nombre total de poids: ${float32Array.length}\n`);
  
  // 3. Préparer le contenu pour le fichier de sortie
  let output = `=== POIDS DU MODÈLE ===\n`;
  output += `Nombre total de poids: ${float32Array.length}\n\n`;
  
  // 4. Extraire les informations des couches depuis model.json
  if (modelJson.weightsManifest) {
    output += `=== STRUCTURE DES COUCHES ===\n\n`;
    
    let offset = 0;
    modelJson.weightsManifest.forEach((manifest, manifestIdx) => {
      manifest.weights.forEach((weightInfo, idx) => {
        const name = weightInfo.name;
        const shape = weightInfo.shape;
        const dtype = weightInfo.dtype;
        
        // Calculer le nombre d'éléments
        const numElements = shape.reduce((a, b) => a * b, 1);
        
        // Extraire les poids correspondants
        const weights = Array.from(float32Array.slice(offset, offset + numElements));
        
        console.log(`\n📦 ${name}`);
        console.log(`   Shape: [${shape.join(', ')}]`);
        console.log(`   Type: ${dtype}`);
        console.log(`   Nombre d'éléments: ${numElements}`);
        console.log(`   Premiers poids: [${weights.slice(0, 5).map(w => w.toFixed(6)).join(', ')}...]`);
        
        output += `\n--- ${name} ---\n`;
        output += `Shape: [${shape.join(', ')}]\n`;
        output += `Type: ${dtype}\n`;
        output += `Nombre d'éléments: ${numElements}\n`;
        output += `Poids:\n`;
        output += `[${weights.map(w => w.toFixed(6)).join(', ')}]\n`;
        
        offset += numElements;
      });
    });
  } else {
    // Si pas de weightsManifest, afficher tous les poids bruts
    output += `=== TOUS LES POIDS (BRUTS) ===\n\n`;
    const allWeights = Array.from(float32Array);
    
    console.log(`\n📦 Tous les poids (${allWeights.length} éléments)`);
    console.log(`   Premiers poids: [${allWeights.slice(0, 10).map(w => w.toFixed(6)).join(', ')}...]`);
    
    output += allWeights.map(w => w.toFixed(6)).join('\n');
  }
  
  // 5. Sauvegarder dans le fichier
  fs.writeFileSync(OUTPUT_FILE, output, 'utf8');
  
  console.log(`\n✅ Poids sauvegardés dans: ${OUTPUT_FILE}`);
  console.log(`📁 Taille du fichier: ${(fs.statSync(OUTPUT_FILE).size / 1024).toFixed(2)} KB`);
}

// Exécution
try {
  extractWeights();
} catch (error) {
  console.error('❌ Erreur:', error.message);
  console.error('\n💡 Assurez-vous que les fichiers model.json et model.weights.bin existent dans le même dossier.');
}