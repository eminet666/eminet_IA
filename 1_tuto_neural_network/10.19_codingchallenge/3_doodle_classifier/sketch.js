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

function prepareData(category, data, label){
    category.training = [];
    category.testing = [];
    for (let i = 0; i < total_data; i++){
        let offset = i * len;
        let threshold = floor(0.8 * total_data);
        if(i < threshold) {
            category.training[i] = data.bytes.subarray(offset, offset+len);   
            category.training[i].label = label;
        } else {
            category.testing[i-threshold] = data.bytes.subarray(offset, offset+len);
            category.testing[i-threshold].label = label;
        }
   }
}

function trainingEpoch(training){
    shuffle(training, true); // true = same array
   
    for (let i= 0; i < training.length; i++) {
        let data = training[i];
        let inputs = data.map(x => x /255);        
        let label = training[i].label;
        let targets = [0, 0, 0];
        targets[label] = 1;

        nn.train(inputs, targets);
    }
}

function testAll(testing){
    let correct = 0;
    for (let i= 0; i < testing.length; i++) {
    // for (let i= 0; i < 1; i++) {
        let data = testing[i];
        let inputs = data.map(x => x /255);        
        let label = testing[i].label;
        let guess = nn.predict(inputs);
        let m = max(guess);
        let classification = guess.indexOf(m);
        // console.log(guess);
        // console.log(classification);
        // console.log(label);

        if (classification === label){
            correct++;
        }
    }
    let percent = correct /testing.length;
    return percent;  
}

function setup(){
    createCanvas(280,280);
    background(0);
    prepareData(cats, cats_data, CAT);
    prepareData(rainbows, rainbows_data, RAINBOW);
    prepareData(trains, trains_data, TRAIN);

    nn = new NeuralNetwork(len, 64, 3);    

    // step 0 : prepare shuffle data concatened
    let training = [];
    training = training.concat(cats.training);
    training = training.concat(rainbows.training);
    training = training.concat(trains.training);

    let testing = [];
    testing = testing.concat(cats.testing);
    testing = testing.concat(rainbows.testing);
    testing = testing.concat(trains.testing);    

    // // step 1 : train for one epoch (= nb passage jeu de données de training)   
    // trainingEpoch(training);

    // // step 2 : testing results
    // let percent = testAll(testing);
    // console.log("% correct = "+percent);
    // // résultats : 78% avec le training, 33% sans training

    // step 3 : multiple epoch and testing
    for (let i = 1; i < 6; i++){
        // step 1 : train for one epoch  
        trainingEpoch(training);
        console.log("Epoch: "+i);
        // step 2 : testing results
        let percent = testAll(testing);
        console.log("% correct = "+percent);
    }
    // résultats : 76% / 79% / 81% / 80% / 80%
    // le dataset de training de 2400 reste faible

}