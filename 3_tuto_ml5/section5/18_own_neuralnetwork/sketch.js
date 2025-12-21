let model;
let targetLabel = 'C';
let trainingData = [];
let state = 'collection';

function setup() {  
  createCanvas(400, 400);
  // STEP 0: define the model
  let options = {
    inputs: ['x', 'y'],         //  input features
    outputs: ['label'],         // output labels
    task: 'classification',     // type of model
    debug : true                // show a graph of loss during training
  };
  model = ml5.neuralNetwork(options); // create the model
}

// STEP 1: add data
function keyPressed() {
    // 't' key to start training
    state = 'training';
    console.log('starting training');
    model.normalizeData(); // normalize the data before training
    if (key == 't') {
        let options = {
            epochs: 200
        };
        model.train(options, whileTraining, finishedTraining); // train the model
    } else { // change target label
        targetLabel = key.toUpperCase();
    }
}

function mousePressed() {  
    let inputs = { 
        x: mouseX, 
        y: mouseY 
    };  

    if (state !== 'collection') {

        let target = { 
            label: targetLabel 
        };
        model.addData(inputs, target); // add data to the model
        
        // visualize the point
        stroke(0);
        noFill();
        ellipse(mouseX, mouseY, 24);  
        fill(0);
        noStroke();
        textAlign(CENTER, CENTER);  
        text(targetLabel, mouseX, mouseY);
    } else if (state == 'prediction') {
        // STEP 3: make a prediction
        model.classify(inputs, gotResults); // make a prediction
    }
}

function draw() {  
  background(255);     
}

// STEP 2: train the model
function whileTraining(epoch, loss) {
    console.log(`Epoch: ${epoch}, Loss: ${loss}`);
}
function finishedTraining() {
    console.log('Finished training!'); 
    state = 'prediction'; 
}

// STEP 3: get the prediction results
function gotResults(error, results) {
    if (error) {        
        console.error(error);
        return;
    }
    console.log(results);
    // visualize the point
    stroke(0);
    noFill();
    ellipse(mouseX, mouseY, 24);  
    fill(0, 0, 255, 100);
    noStroke();
    textAlign(CENTER, CENTER);  
    text(results[0].label, mouseX, mouseY);    
}

