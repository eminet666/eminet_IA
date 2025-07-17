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
  // Créer un modèle de classification avec ml5.js
  classifier = ml5.imageClassifier('MobileNet', modelReady);

  // Charger le modèle et entraîner avec les images chargées
  function modelReady() {
    console.log("Modèle prêt !");
    trainModel();  // Démarrer l'entraînement
  }
}

// Fonction pour entraîner le modèle
async function trainModel() {
  console.log("Début de l'entraînement...");

  // Vérifiez si classifier est bien défini et a la méthode addImage
  console.log(classifier);

  // Ajouter les images au classificateur avec le bon label
  for (let data of trainingData) {
    if (classifier.addImage) {
      await classifier.addImage(data.image, data.label);
      console.log(`Image ${data.label} ajoutée`);
    } else {
      console.error("La méthode addImage n'existe pas sur l'objet classifier.");
    }
  }

  // Démarrer l'entraînement avec la méthode train()
  classifier.train((loss) => {
    if (loss) {
      console.log("Entraînement en cours, perte : " + loss);
    } else {
      console.log("Entraînement terminé !");
      // Sauvegarder le modèle une fois l'entraînement terminé
      classifier.save();
      console.log("Modèle sauvegardé.");
      isTrainingComplete = true;
      displayResults();  // Afficher les résultats une fois l'entraînement terminé
    }
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
