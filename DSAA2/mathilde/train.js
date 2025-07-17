let classifier;
let images = [];
let labels = [];
let totalImages = 0;
let trainingData = [];
let isTrainingComplete = false;

// Fonction pour charger le fichier dataset.json
function loadFileList() {
  fetch('dataset.json')  // Charger le fichier JSON
    .then(response => response.json())  // Parser le fichier JSON
    .then(data => {
      // Préparer les images et les labels en utilisant les répertoires corrects
      loadImages(data.train.target, 'target');
      loadImages(data.train.others, 'others');  // Charger les images du répertoire 'others'
    })
    .catch(error => {
      console.error('Erreur lors du chargement du fichier JSON:', error);
    });
}

// Fonction pour charger les images à partir des fichiers listés dans dataset.json
function loadImages(imageFiles, label) {
  totalImages += imageFiles.length;
  imageFiles.forEach(file => {
    const img = loadImage(`dataset/train/${label}/${file}`, () => {
      // Ajouter les images et leurs labels au tableau trainingData
      trainingData.push({ image: img, label: label });

      // Vérifier si toutes les images ont été chargées
      if (trainingData.length === totalImages) {
        setupModel();  // Quand toutes les images sont chargées, on commence l'entraînement
      }
    });
  });
}

// Fonction pour configurer et entraîner le modèle
function setupModel() {
  // Créer un classificateur d'images avec ml5.js
  const options = {
    inputs: [64, 64, 4],
    task: 'classification',
    debug: true
  };
  classifier = ml5.neuralNetwork(options);

  // Ajouter les images au classificateur avec le bon label
  for (let data of trainingData) {
    classifier.addData({ image: data.image }, { label: data.label });
  }

  // Normaliser les données
  classifier.normalizeData();

  // Configurer les options d'entraînement
  const trainingOptions = {
    epochs: 20
  };

  // Entraîner le modèle
  classifier.train(trainingOptions, () => {
    console.log("Entraînement terminé !");
    classifier.save();
    console.log("Modèle sauvegardé.");
    isTrainingComplete = true;
    displayResults();  // Afficher les résultats une fois l'entraînement terminé
  });
}

// Fonction pour afficher les résultats de l'entraînement
function displayResults() {
  if (isTrainingComplete) {
    const resultDiv = document.createElement('div');
    resultDiv.innerHTML = `<h2>Entraînement terminé !</h2><p>Le modèle est prêt à être utilisé.</p>`;
    document.body.appendChild(resultDiv);

    // Afficher un bouton ou une interface pour tester le modèle
    const testButton = document.createElement('button');
    testButton.innerText = "Tester le modèle avec une nouvelle image";
    testButton.onclick = () => {
      // Ajouter un test avec une nouvelle image ici si nécessaire
      alert("Test avec une nouvelle image");
    };
    document.body.appendChild(testButton);
  }
}

// Cette fonction s'appelle lorsque la page est prête
function setup() {
  loadFileList();  // Charger et afficher les fichiers depuis dataset.json
}
