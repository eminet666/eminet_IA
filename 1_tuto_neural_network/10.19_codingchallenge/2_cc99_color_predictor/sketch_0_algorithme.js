let r, g, b;

function pickColor(){
  r = random(255);
  g = random(255);
  b = random(255);
}

//let which = "black";

function colorPredictor(r, g, b){
  let sum = r + g + b;
  console.log(sum);
  if(sum > 300){
    return "black";
  } else {
    return "white";
  }
}


function setup(){
    createCanvas(600, 300);
    pickColor();
}

function draw(){
    background(r,g,b);

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




