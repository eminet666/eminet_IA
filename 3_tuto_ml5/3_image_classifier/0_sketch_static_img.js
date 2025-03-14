let classifier;
let img;
let label = "waiting...";

function preload() {
  classifier = ml5.imageClassifier('MobileNet');
  img = loadImage("/3_tuto_ml5/3_image_classifier/assets/labrador.jpg");
}

function gotResults(results) {
  console.log(results); // an array of objects
  label = results[0].label;
  console.log(label);
}

function setup() {
  createCanvas(400, 400);
  let res = classifier.classify(img, gotResults); // 1 is the number of results
}

function draw() {
  image(img, 0, 0);
}  