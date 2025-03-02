const len = 784;
const total_data = 1000;

const CAT = 0;
const RAINBOW = 1;
const TRAIN = 2;

let cats_data;
let trains_data;
let rainbows_data;

let cats = {};
let trains = {};
let rainbows = {};

let nn;

// step 0 : chargement des data
function preload(){
    cats_data = loadBytes("./data/cats1000.bin");
    trains_data = loadBytes("./data/trains1000.bin");
    rainbows_data = loadBytes("./data/rainbows1000.bin");
}

function prepareData(category, data, label) {
  category.training = [];
  category.testing = [];
  for (let i = 0; i < total_data; i++) {
    let offset = i * len;
    let threshold = floor(0.8 * total_data);
    if (i < threshold) {
      category.training[i] = data.bytes.subarray(offset, offset + len);
      category.training[i].label = label;
    } else {
      category.testing[i - threshold] = data.bytes.subarray(offset, offset + len);
      category.testing[i - threshold].label = label;
    }
  }
}


function setup(){
    createCanvas(280,280);
    background(0);
    prepareData(cats, cats_data, CAT);
    prepareData(rainbows, rainbows_data, RAINBOW);
    prepareData(trains, trains_data, TRAIN);
    console.log(trains);    

    nn = new NeuralNetwork(len, 64, 3);

    // step 0 : prepare shuffle data concatened
    let training = [];
    training = training.concat(cats.training);
    training = training.concat(rainbows.training);
    training = training.concat(trains.training);
    shuffle(training, true); // true = same array

    // step 1 : train for one epoch    
    for (let i= 0; i < training.length; i++) {
        let inputs = training[i];
        let data = training[i];
        for (j = 0; j < data.length; j++){
            inputs[j] = data[j]/255.0; // inputs normalized
        }
        let label = training[i].label;
        let targets = [0, 0, 0];
        targets[label] = 1;

        nn.train(inputs, targets);
        console.log("Train for one epoch"); //epoch = nb de passage d'un jeu de données de training
    }
}