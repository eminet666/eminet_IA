const len = 784;
const totalData = 1000;

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

function preload(){
    cats_data = loadBytes("./data/cats1000.bin");
    trains_data = loadBytes("./data/trains1000.bin");
    rainbows_data = loadBytes("./data/rainbows1000.bin");
}

function setup(){
    createCanvas(280,280);
    background(255);
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

    // step 4
    let trainButton = select('#train');
    let epochCounter = 0;
    trainButton.mousePressed(function() {
        console.log("Training ...");       
        trainEpoch(training);
        epochCounter++;
        console.log("Epoch : "+epochCounter); 
    });

    let testButton = select('#test');
    testButton.mousePressed(function() {
        let percent = testAll(testing);
        console.log("Percent : "+nf(percent,2,2)+"%");
    });

    let guessButton = select('#guess');
    guessButton.mousePressed(function() {
        let inputs = [];
        let img = get(); // get all the pixels of the canvas
        //console.log(img);
        img.resize(28,28);
        img.loadPixels();
        for (let i = 0; i < len; i++){ 
            let bright = img.pixels[i*4]; // 1 pixel sur 4 car r=g=b
            inputs[i] = (255 - bright) / 255.0;
        }
        //console.log(inputs); 
        
        let guess = nn.predict(inputs);
        let m = max(guess);
        let classification = guess.indexOf(m);
        if(classification === CAT){ console.log("CAT"); }
        else if (classification === RAINBOW) { console.log("RAINBOW"); }
        else if (classification === TRAIN) { console.log("TRAIN"); }

        // image(img, 0, 0); // image 28x28 for 
    });

    let clearButton = select('#clear');
    clearButton.mousePressed(function() {
        background(255);
    });


}