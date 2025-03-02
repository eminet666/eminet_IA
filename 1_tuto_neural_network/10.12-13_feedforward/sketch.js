var brain;

function setup() {

    let nn = new NeuralNetwork(2,2,1);
    
    let input = [1, 0];

    let output = nn.feedForward(input);
    console.log("guess = "+output);

}

function draw() {
    
}

// TEST fromArray
// let arr = [1, 0, -5];
// Matrix.fromArray(arr);