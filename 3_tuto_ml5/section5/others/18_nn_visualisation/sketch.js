var model;
var targetLabel = 'A';
var state = 'training';

var labels = {
'A': [255, 100, 100],
'B': [100, 255, 100],
'C': [100, 100, 255],
'D': [255, 100, 255]
};

function setup() {
createCanvas(400, 400);
background(200);
textAlign(CENTER, CENTER);

let options = {
inputs: ['x', 'y'],
outputs: ['label'],
task: 'classification',
debug: 'true'
}
model = ml5.neuralNetwork(options);
}

function keyPressed() {
if (state == 'training') {
if (key == 't') {
model.normalizeData();
let option = {
epochs: 300
}
model.train(option, () => {}, () => {
state = 'prediction';
for (let x = 0; x < width; x+=5) { for (let y=0; y < height; y+=5) { model.classify({x: x, y: y}, (err, result)=> {
    stroke(...labels[result[0].label], 100);
    strokeWeight(6);
    point(x, y);
    });
    }
    }
    });
    }
    targetLabel = key.toUpperCase();
    }
    }

    function mousePressed() {
    let input = {
    x: mouseX,
    y: mouseY
    }

    if (state == 'training') {
    let output = {
    label: targetLabel
    }
    model.addData(input, output);
    noFill();
    stroke(...labels[targetLabel]);
    ellipse(mouseX, mouseY, 25);

    fill(...labels[targetLabel]);
    text(targetLabel, mouseX, mouseY);
    }
    }