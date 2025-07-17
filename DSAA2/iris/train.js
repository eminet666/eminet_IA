// Charger ml5.js
console.log("Chargement de ml5...");
let nn;

function setup() {
    // Initialiser le modèle de réseau de neurones
    nn = ml5.neuralNetwork({ task: 'classification', debug: true });

    // Ajouter les images au dataset
    loadImages();
}

function loadImages() {
    const categories = ["target", "others"];
    
    categories.forEach(category => {
        for (let i = 1; i <= 800; i++) {  // 800 images d'entraînement
            let imgPath = `dataset/train/${category}/${i}.jpg`;
            nn.addData({ image: imgPath }, { label: category });
        }
    });

    console.log("Images chargées, début de l'entraînement...");
    trainModel();
}

function trainModel() {
    nn.normalizeData();  // Normaliser les données
    nn.train({ epochs: 50 }, () => {
        console.log("Entraînement terminé !");
        nn.save();  // Sauvegarde du modèle entraîné
    });
}

// Lancer l'entraînement
setup();
