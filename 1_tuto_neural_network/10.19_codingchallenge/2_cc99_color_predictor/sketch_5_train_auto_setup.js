let nb_training = 10000; // nombre d'itérations d'entraînement
let brain;
let r, g, b;
let attendu; // pour afficher dans draw()
let predicted; // pour afficher dans draw()
let outputs; // pour afficher dans draw()
let targets; // pour afficher dans draw()
let nb_guess = 0;
let nb_ok = 0;

// CHOIX ALEATOIRE DE LA COULEUR DE FOND
function pickColor(){
  r = random(255);
  g = random(255);
  b = random(255);

  if (r + g + b > 300){
    attendu = "(B)";
  } else {
    attendu = "(W)";
  }
}

function colorPredictor(r, g, b){
    let guess;
    let inputs = [r/255, g/255, b/255];
    // let outputs = brain.predict(inputs);
    outputs = brain.predict(inputs);    
    //console.log(outputs);

    if(outputs[0] > outputs[1]) {
      predicted = "(B)"; 
    } else {
      predicted = "(W)"; 
    }
}

function trainColor(r,g,b) {
  if (r + g + b > 300){
    return [1,0];
  } else {
    return [0,1];
  }
}

function setup(){
    // createCanvas(600, 300);
    createCanvas(600, 600); // pour afficher les matrices
    background(255);
    brain = new NeuralNetwork(3, 3, 2); // STEP2
    
    console.log("Training ...");
    for (let i = 0; i < nb_training; i++){
      let r = random(255);
      let g = random(255);
      let b = random(255);
      let targets = trainColor(r, g, b);
      let inputs = [r/255, g/255, b/255];
      brain.train(inputs, targets);
    }
    console.log("... Training finished");
    pickColor();
}

function draw(){
    background(r,g,b);
    strokeWeight(4);
    stroke(0);
    line(width/2, 0, width/2, height);

    textSize(64);
    noStroke();
    textAlign(CENTER, CENTER);    
    fill(0);
    text("black", 150, 150);
    fill(255);
    text("white", 450, 150);

    // AFFICHAGE PASTILLE
    if (predicted === "(B)") {
      fill(0);
      ellipse(150,225, 60);
    }
    else {
      fill(255);
      ellipse(450, 225, 60);
    }

    // AFFICHAGE MATRICES
    fill(255);
    rect(0, 300, width, height/2);
    textSize(18);
    noStroke();
    textAlign(LEFT);   
    fill(0);
    if(nb_guess > 0){
        text("Inputs : "+[r.toFixed(0),g.toFixed(0),b.toFixed(0)]+"_"+attendu, 50, 320);
        text("Outputs : "+outputs[0].toFixed(2)+", "+outputs[1].toFixed(2)+"_"+predicted, 310, 320);
        text("Accuracy: "+(nb_ok/nb_guess*100).toFixed(2)+"% ("+nb_ok+"/"+nb_guess+")", 310, 345);
    }
    text("IH weights", 50, 370);
    text("HO weights", 310, 370);
    displayMatrixInCanvas(brain.weights_ih, 50, 390);
    displayMatrixInCanvas(brain.weights_ho, 310, 390); 
}

function mousePressed(){
  pickColor();
  nb_guess++; 
  colorPredictor(r, g, b);
  if (predicted === attendu) nb_ok++;
}

/**
 * Affiche une matrice dans le canvas p5
 * @param {Matrix} matrix - La matrice à afficher
 * @param {number} x - Position x en pixels
 * @param {number} y - Position y en pixels
 * @param {number} cellSize - Taille de chaque cellule en pixels
 */
function displayMatrixInCanvas(matrix, x, y, cellSize = 50) {
    push();
    textSize(18);
    for (let i = 0; i < matrix.rows; i++) {
        for (let j = 0; j < matrix.cols; j++) {
            let val = matrix.data[i][j];
            let str = val.toFixed(2);
            textAlign(CENTER); 
            fill(255);
            stroke(0);
            rect(x + j * cellSize, y + i * cellSize, cellSize, cellSize);
            fill(0);
            noStroke();
            text(str, x + j * cellSize + cellSize / 2, y + i * cellSize + cellSize / 2);
        }
    }
    pop();
}





