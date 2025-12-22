const fs = require('fs');

// Chemins vers vos fichiers
const MODEL_JSON_PATH = './model/model.json';
const WEIGHTS_BIN_PATH = './model/model.weights.bin';
const OUTPUT_FILE = './weights_matrices.txt';

function extractWeightsAsMatrices() {
  console.log('🔍 Extraction des poids sous forme de matrices...\n');

  // 1. Lire le fichier model.json
  const modelJson = JSON.parse(fs.readFileSync(MODEL_JSON_PATH, 'utf8'));
  
  // 2. Lire le fichier .bin
  const buffer = fs.readFileSync(WEIGHTS_BIN_PATH);
  const float32Array = new Float32Array(buffer.buffer);
  
  // 3. Préparer le contenu de sortie
  let output = '═══════════════════════════════════════════════════════\n';
  output += '           MATRICES DES POIDS DU RÉSEAU\n';
  output += '═══════════════════════════════════════════════════════\n\n';
  
  console.log('📊 Extraction des matrices de poids:\n');
  
  let offset = 0;
  let matrixCount = 0;
  
  if (modelJson.weightsManifest) {
    modelJson.weightsManifest.forEach(manifest => {
      manifest.weights.forEach(weightInfo => {
        const name = weightInfo.name;
        const shape = weightInfo.shape;
        const dtype = weightInfo.dtype;
        const numElements = shape.reduce((a, b) => a * b, 1);
        
        // Extraire les poids
        const weights = Array.from(float32Array.slice(offset, offset + numElements));
        
        // Déterminer le type (matrice de poids ou vecteur de biais)
        const isKernel = name.includes('kernel');
        const isBias = name.includes('bias');
        
        if (isKernel) {
          matrixCount++;
          console.log(`\n📦 Matrice ${matrixCount}: ${name}`);
          console.log(`   Dimensions: ${shape[0]} × ${shape[1]}`);
          console.log(`   (${shape[0]} neurones source → ${shape[1]} neurones destination)\n`);
          
          output += `\n${'═'.repeat(55)}\n`;
          output += `MATRICE ${matrixCount}: ${name}\n`;
          output += `${'═'.repeat(55)}\n`;
          output += `Dimensions: ${shape[0]} lignes × ${shape[1]} colonnes\n`;
          output += `(${shape[0]} neurones source → ${shape[1]} neurones destination)\n\n`;
          
          // Construire la matrice
          const matrix = [];
          for (let i = 0; i < shape[0]; i++) {
            const row = [];
            for (let j = 0; j < shape[1]; j++) {
              const index = i * shape[1] + j;
              row.push(weights[index]);
            }
            matrix.push(row);
          }
          
          // Afficher la matrice dans la console (première et dernière ligne)
          console.log('   Première ligne:', matrix[0].slice(0, 5).map(v => v.toFixed(6)).join(', '), '...');
          if (matrix.length > 1) {
            console.log('   Dernière ligne:', matrix[matrix.length-1].slice(0, 5).map(v => v.toFixed(6)).join(', '), '...');
          }
          
          // Écrire la matrice dans le fichier
          output += formatMatrix(matrix, shape[0], shape[1]);
          
        } else if (isBias) {
          console.log(`\n🔷 Biais: ${name}`);
          console.log(`   Dimensions: ${shape[0]} éléments\n`);
          console.log('   Valeurs:', weights.slice(0, Math.min(10, weights.length)).map(v => v.toFixed(6)).join(', '));
          if (weights.length > 10) console.log('   ...');
          
          output += `\n${'─'.repeat(55)}\n`;
          output += `VECTEUR DE BIAIS: ${name}\n`;
          output += `${'─'.repeat(55)}\n`;
          output += `Dimensions: ${shape[0]} éléments\n\n`;
          output += formatBiasVector(weights);
        }
        
        offset += numElements;
      });
    });
  }
  
  // Résumé
  output += `\n\n${'═'.repeat(55)}\n`;
  output += `RÉSUMÉ\n`;
  output += `${'═'.repeat(55)}\n`;
  output += `Nombre de matrices de poids: ${matrixCount}\n`;
  output += `Nombre total de paramètres: ${float32Array.length.toLocaleString()}\n`;
  
  console.log(`\n✅ Nombre de matrices extraites: ${matrixCount}`);
  console.log(`📊 Nombre total de paramètres: ${float32Array.length.toLocaleString()}`);
  
  // Sauvegarder
  fs.writeFileSync(OUTPUT_FILE, output, 'utf8');
  console.log(`\n💾 Matrices sauvegardées dans: ${OUTPUT_FILE}`);
  console.log(`📁 Taille du fichier: ${(fs.statSync(OUTPUT_FILE).size / 1024).toFixed(2)} KB`);
}

function formatMatrix(matrix, rows, cols) {
  let output = '';
  
  // Trouver la largeur maximale pour l'alignement
  let maxWidth = 0;
  matrix.forEach(row => {
    row.forEach(val => {
      const width = val.toFixed(6).length;
      if (width > maxWidth) maxWidth = width;
    });
  });
  
  // Formatage avec alignement
  for (let i = 0; i < rows; i++) {
    output += '[ ';
    for (let j = 0; j < cols; j++) {
      const val = matrix[i][j].toFixed(6);
      output += val.padStart(maxWidth, ' ');
      if (j < cols - 1) output += ',  ';
    }
    output += ' ]\n';
  }
  
  return output;
}

function formatBiasVector(biases) {
  let output = '[ ';
  biases.forEach((bias, index) => {
    output += bias.toFixed(6);
    if (index < biases.length - 1) output += ',  ';
  });
  output += ' ]\n';
  return output;
}

// Exécution
try {
  extractWeightsAsMatrices();
} catch (error) {
  console.error('❌ Erreur:', error.message);
  console.error('\n💡 Assurez-vous que les fichiers model.json et model.weights.bin existent.');
}