let classifier;
let img;
let label = "waiting...";
let confidence = 0;
let resultat;

function preload() {
  classifier = ml5.imageClassifier("MobileNet");
  img = loadImage("/3_tuto_ml5/3_image_classifier/assets/cat.jpg");
}

function gotResults(results) {
  console.log(results);
  label = results[0].label;
  confidence = results[0].confidence; 
  confidence *= 100;
  confidence = confidence.toFixed(0);  
  resultat = label + " " + confidence + "%"; 
}

function setup() {
  createCanvas(400, 400);
  classifier.classify(img, gotResults);
}

function draw() {
  background(220);
  image(img, 0, 0);

  rectMode(CENTER);
  fill(0);
  rect(200, 200, 400, 50);
  textSize(32);
  fill(255);
  textAlign(CENTER, CENTER);
  noStroke();
  text(resultat, 200, 200);
}