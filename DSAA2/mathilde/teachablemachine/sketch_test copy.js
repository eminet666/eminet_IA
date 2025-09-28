let model;
let images = [];
let currentImageIndex = 0;

function preload() {
    // Charger les images (remplacez les chemins avec ceux de vos images)
    console.log('PRELOADING IMAGES ...');
    for (let i = 0; i < 29; i++) {
        let path = `../dataset/test/target/`;
        images[i] = loadImage(path+`img_${i}.jpg`);
    }
}

function setup() {
    console.log('LOADDING MODEL ...');
    createCanvas(800, 600);
    // Charger le modèle (remplacez 'path/to/model.json' par le chemin de votre modèle)
    tf.loadLayersModel('./model/model.json').then((loadedModel) => {
        model = loadedModel;
        console.log('MODEL LOADED SUCCESSFULLY');
    });
}

function draw() {
    background(220);
    if (images.length > 0 && model) {
        // Afficher l'image actuelle
        let img = images[currentImageIndex];
        image(img, 0, 0, width, height);

        // Utiliser le modèle pour faire une prédiction
        let inputTensor = preprocessImage(img);
        let predictions = model.predict(inputTensor);
        predictions.print(); // Visualiser les prédictions dans la console

        // Changer d'image toutes les 5 secondes
        if (frameCount % (60 * 5) === 0) {
            currentImageIndex = (currentImageIndex + 1) % images.length;
        }
    }
}

function preprocessImage(img) {
    // Convertir l'image p5 en un tenseur
    let resizedImg = img.resize(224, 224);
    let inputTensor = tf.browser.fromPixels(resizedImg).toFloat();
    inputTensor = inputTensor.expandDims(0); // Ajouter une dimension de lot
    return inputTensor;
}
