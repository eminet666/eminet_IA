// Add some header info
// For TM template code

// Video
let video;
let label = "Waiting...";
let classifier;

// STEP 1: Load the model!
function preload() {
  classifier = ml5.imageClassifier('https://teachablemachine.withgoogle.com/models/3f6NL2TAd/model.json');
} 

function setup() {
  createCanvas(640, 520);
  // Create the video
  video = createCapture(VIDEO);
  video.hide();

  // STEP 2: Start classifying
  classifyVideo();
}

// STEP 2 classify!
function classifyVideo() {
  classifier.classify(video, gotResult);
}

function draw() {
  background(0);
  
  // Draw the video
  image(video, 0, 0);

  // STEP 3: Draw the label 
  textSize(32);
  textAlign(CENTER, CENTER);
  text(label, width / 2, height - 16); 
}

// STEP 3: Get the classification!

function gotResult(error, results) { 
  if (error) {
    console.error(error);
    return;
  } 
  // The results are in an array ordered by confidence.
  // Store the label and classify again!
  label = results[0].label;
  classifyVideo();
}

