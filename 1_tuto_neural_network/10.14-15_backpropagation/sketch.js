var brain;

function setup() {

    let nn = new NeuralNetwork(2,2,2);
    let inputs = [1,0];
    let targets = [1,0];

    // let output = nn.feedForward(input);
    nn.train(inputs, targets);


}

function draw() {
    
}