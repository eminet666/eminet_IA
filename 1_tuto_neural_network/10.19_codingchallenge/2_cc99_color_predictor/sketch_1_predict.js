let brain;
let r, g, b;

function pickColor(){
  r = random(255);
  g = random(255);
  b = random(255);
}

//let which = "black";

function colorPredictor(r, g, b){
    let inputs = [r/255, g/255, b/255];
    let outputs = brain.predict(inputs);
    console.log(outputs);

    if(outputs[0] > outputs[1]) {
      return "black";
    } else {
      return "white";
    }

}


function setup(){
    createCanvas(600, 300);
    brain = new NeuralNetwork(3, 3, 2); // STEP2
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

    let which = colorPredictor(r, g, b);
    if (which === "black") {
      fill(0);
      ellipse(150,225, 60);
    }
    else {
      fill(255);
      ellipse(450, 225, 60);
    }


}


function mousePressed(){
  pickColor();
}




