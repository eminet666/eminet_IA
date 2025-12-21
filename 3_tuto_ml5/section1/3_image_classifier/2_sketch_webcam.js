let classifier;
let video;
let label = "waiting...";
let confidence = 0;
let resultat;

function preload() {
  classifier = ml5.imageClassifier("MobileNet");
}

function gotResults(results) {
  //console.log(results);
  label = results[0].label;
  confidence = results[0].confidence; 
  confidence *= 100;
  confidence = confidence.toFixed(0);  
  resultat = label + " " + confidence + "%"; 
}

function setup() {
  createCanvas(640, 480);
  video = createCapture(VIDEO);
  video.hide();
  classifier.classifyStart(video, gotResults);
}

function draw() {
  background(220);
  image(video, 0, 0, width,  height);

  rectMode(CENTER);
  fill(0);
  rect(width/2, height -50, width, 50);
  textSize(32);
  fill(255);
  textAlign(CENTER, CENTER);
  noStroke();
  text(resultat, width/2, height - 50);

  // if (confidence > 50) {
  //   background(0, 255, 0,100);
  // }
}