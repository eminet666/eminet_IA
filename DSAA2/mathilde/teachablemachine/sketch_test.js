let model;
let images = [];
let currentImageIndex = 0;
let imagesLoaded = false;
let temporaryCanvas;
let predictionText = ""; // Variable pour stocker le texte de prédiction

function setup() {
    console.log('LOADING MODEL ...');
    createCanvas(800, 600);

    // Créer un canevas temporaire pour manipuler les images
    temporaryCanvas = createGraphics(224, 224);

    // Charger le modèle
    tf.loadLayersModel('./model/model.json').then((loadedModel) => {
        model = loadedModel;
        console.log('MODEL LOADED SUCCESSFULLY');
    }).catch((error) => {
        console.error('Error loading the model:', error);
    });
}

function preload() {
    console.log('PRELOADING IMAGES ...');
    // Charger les images
    for (let i = 0; i < 29; i++) {
        let path = `../dataset/test/target/`;
        images[i] = loadImage(path+`img_${i}.jpg`, () => {
            console.log(`Image ${i} loaded`);
        }, (event) => {
            console.error(`Error loading image ${i}:`, event);
        });
    }
    imagesLoaded = true;
}

function draw() {
    background(220);
    if (images.length > 0 && imagesLoaded && model) {
        let img = images[currentImageIndex];
        if (img) {
            image(img, 0, 0, img.width, img.height); // Affichez l'image originale

            // try {
            //     tf.tidy(() => {
            //         let inputTensor = preprocessImage(img);
            //         let predictions = model.predict(inputTensor);
            //         // Supposons que votre modèle prédise un tableau de probabilités ou une classe
            //         // Vous devez adapter cette partie selon votre modèle et vos classes.
            //         let predictedClass = predictions.dataSync()[0] > 0.5 ? "Others" : "Target"; // Exemple simple
            //         predictionText = `Prédiction: ${predictedClass}`;
            //         predictions.print(); // Visualiser les prédictions dans la console
            //     });
            // } catch (e) {
            //     console.error('Error during prediction:', e);
            // }

            try {
                tf.tidy(() => {
                    let inputTensor = preprocessImage(img);
                    let predictions = model.predict(inputTensor);
                    // Supposons que votre modèle prédise un tableau de probabilités ou une classe
                    let predictionData = predictions.dataSync();
                    let predictedClassIndex = predictionData[0] > 0.5 ? 1 : 0; // Exemple simple
                    let predictedClass = predictions.dataSync()[0] > 0.5 ? "Others" : "Target";
                    let confidenceScore = predictionData[predictedClassIndex] * 100; // Calculer le score de confiance en pourcentage
                    predictionText = `Prédiction: ${predictedClass}, Confiance: ${confidenceScore.toFixed(2)}%`;
                    predictions.print(); // Visualiser les prédictions dans la console
                });
            } catch (e) {
                console.error('Error during prediction:', e);
            }            

            // Afficher le texte de prédiction
            fill(255); // Couleur du texte (noir)
            textSize(40); // Taille du texte
            textAlign(CENTER, CENTER); // Alignement du texte
            text(predictionText, width / 2, height - 50); // Positionner le texte au bas du canevas
        } else {
            console.log(`Image at index ${currentImageIndex} is not loaded yet.`);
        }

        // Changer d'image toutes les 5 secondes
        if (frameCount % (60 * 5) === 0) {
            currentImageIndex = (currentImageIndex + 1) % images.length;
        }
    }
}

function preprocessImage(img) {
    // Dessinez l'image sur le canevas temporaire
    temporaryCanvas.clear();
    temporaryCanvas.image(img, 0, 0, 224, 224); // Redimensionnement lors du dessin

    // Utilisez le canevas temporaire pour créer le tenseur
    let inputTensor = tf.browser.fromPixels(temporaryCanvas.elt).toFloat();
    inputTensor = inputTensor.expandDims(0); // Ajouter une dimension de lot
    return inputTensor;
}
