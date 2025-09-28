let model;
let images = [];
let currentImageIndex = 0;
let imagesLoaded = false;
let temporaryCanvas; // Canevas temporaire pour le traitement des images

function preload() {
    console.log('PRELOADING IMAGES ...');
    // Charger les images (remplacez les chemins avec ceux de vos images)
    for (let i = 0; i < 3; i++) {
        let path = `../dataset/test/target/`;
        images[i] = loadImage(path+`img_${i}.jpg`, () => {
            console.log(`Image ${i} loaded`);
        }, (event) => {
            console.error(`Error loading image ${i}:`, event);
        });
    }
    imagesLoaded = true; // Considérons que les images sont chargées ici
}

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

function draw() {
    background(220);
    if (images.length > 0 && imagesLoaded && model) {
        let img = images[currentImageIndex];
        if (img) {
            image(img, 0, 0, width, height); // Affichez l'image originale

            try {
                tf.tidy(() => {
                    let inputTensor = preprocessImage(img);
                    let predictions = model.predict(inputTensor);
                    predictions.print(); // Visualiser les prédictions dans la console
                });
            } catch (e) {
                console.error('Error during prediction:', e);
            }
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
