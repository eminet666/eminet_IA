let model;
let targetLabel = 'C';
let trainingData = [];
let state = 'collection';

function setup() {  
  createCanvas(400, 400);
  background(192);

  // STEP 0: define the model
  let options = {
    inputs: ['x', 'y'],         //  input features
    outputs: ['label'],         // output labels
    task: 'regression',     // type of model
    learningRate: 0.5,          // learning rate
    debug : true                // show a graph of loss during training
  };
  model = ml5.neuralNetwork(options); // create the model
  // model.loadData('mouse-data.json', dataLoaded); // load the data from file
  const modelInfo = {
    model: 'model/model.json',
    metadata: 'model/model_meta.json',
    weights: 'model/model.weights.bin'
  }
  model.load(modelInfo, modelLoaded); // load the model from files
}


function modelLoaded() {
    console.log('model loaded');
    state = 'prediction';
}

// when data is loaded
function dataLoaded() {
    console.log('data loaded');
    console.log(model.data);
    let data = model.data.data.raw;
    // let data = model.getData(); // alternative way to get the data
    for (let i = 0; i < data.length; i++) {
        let inputs = data[i].xs;
        let target = data[i].ys;

        // visualize the point
        stroke(0);
        noFill();
        ellipse(inputs.x, inputs.y, 24);  
        fill(0);
        noStroke();
        textAlign(CENTER, CENTER);  
        text(target.label, inputs.x, inputs.y);
    } 
    
    // call training automatically after loading data
        state = 'training';
        console.log('starting training');
        model.normalizeData(); // normalize the data before training        
        let options = {
            epochs: 200
        };
        model.train(options, whileTraining, finishedTraining); // train the model
}

// STEP 1: add data
function keyPressed() {
    if (key == 't') {
        // 't' key to start training
        state = 'training';
        console.log('starting training');
        model.normalizeData(); // normalize the data before training        
        let options = {
            epochs: 200
        };
        model.train(options, whileTraining, finishedTraining); // train the model
    } else if (key == 's') { // save data
        model.saveData('mouse-data');   // save the data (function .saveData())
    } else if (key == 'm') { // save model
        model.save();      // save the model (function .save())
    } else { // change target label
        targetLabel = key.toUpperCase();
    }
}

function mousePressed() {  
    let inputs = { 
        x: mouseX, 
        y: mouseY 
    };  

    if (state == 'collection') {

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

// STEP 2: train the model
function whileTraining(epoch, loss) {
    console.log(`Epoch: ${epoch}`);
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
    // console.log(results);
    stroke(0);
    fill(0, 0, 255, 100);
    ellipse(mouseX, mouseY, 24);
    fill(0);
    noStroke();
    textAlign(CENTER, CENTER);
    let label = results[0].label;
    text(label, mouseX, mouseY);   
}

