// Fonction pour charger le fichier dataset.json
function loadFileList() {
  fetch('dataset.json')  // Charger le fichier JSON
    .then(response => response.json())  // Parser le fichier JSON
    .then(data => {
      // Afficher les fichiers dans la console et dans la page
      displayFiles(data.train.target, 'Target');
      displayFiles(data.train.other, 'Other');
    })
    .catch(error => {
      console.error('Erreur lors du chargement du fichier JSON:', error);
    });
}

// Fonction pour afficher les fichiers dans la console et dans la page
function displayFiles(fileNames, label) {
  // Afficher les fichiers dans la console
  console.log(`Fichiers dans ${label}:`);
  fileNames.forEach(file => console.log(file));

  // Ajouter à l'interface utilisateur
  const fileListDiv = document.getElementById('fileList');
  const labelElement = document.createElement('h2');
  labelElement.innerText = `Fichiers dans ${label}:`;
  fileListDiv.appendChild(labelElement);

  fileNames.forEach(file => {
    const fileElement = document.createElement('div');
    fileElement.className = 'file';
    fileElement.innerText = file;
    fileListDiv.appendChild(fileElement);
  });
}

// Cette fonction s'appelle au chargement de la page
function setup() {
  loadFileList();  // Charger et afficher les fichiers depuis dataset.json
}
