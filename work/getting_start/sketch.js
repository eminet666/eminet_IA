let classifier;
let img;

function preload() {
  classifier = ml5.imageClassifier("MobileNet");
  img = loadImage("./assets/cat.jpg");
}

function setup() {
  createCanvas(400, 400);
  classifier.classify(img, gotResult);
  image(img, 0, 0);
}

// function draw() {
//   background(192);
// }


// 1 résultat
function gotResult(results) {
  console.log(results);

  fill(0);
  stroke(0);
  textSize(18);
  label = "Label: " + results[0].label;
  confidence = "Confidence: " + nf(results[0].confidence, 0, 2);
  text(label, 10, 360);
  text(confidence, 10, 380);
}

// 3 résultats
function gotResult(results) {
  console.log(results);
  fill(0);
  noStroke(0);
  textSize(10);
  
  for (let i = 0; i < 3 && i < results.length; i++) {
    let label = "label: " + results[i].label;
    let confidence = "confidence: " + nf(results[i].confidence, 0, 2);
    text(label +", "+ confidence, 10, 350 + i * 10);
  }
}