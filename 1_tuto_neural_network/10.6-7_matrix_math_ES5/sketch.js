var brain;

function setup() {

    brain = NeuralNetwork(3, 3, 1);
}

function draw() {
    
}

// test program
// var m = new NeuralNetwork(3,2);
// m.add(5);
// m.multiply(3);
// console.table(m.matrix);
//
// var m = new NeuralNetwork(3,2);
// m.randomize();
// m.multiply(2);
// console.table(m.matrix);
//
// var m1 = new NeuralNetwork(3,2);
// var m2 = new NeuralNetwork(3,2);
// m1.randomize();
// m2.randomize();
// console.table(m1.matrix);
// console.table(m2.matrix);
// m1.add(m2);
// console.table(m1.matrix);
//
// var m1 = new NeuralNetwork(3,2);
// var m2 = new NeuralNetwork(3,2);
// m1.randomize();
// m2.randomize();
// console.table(m1.matrix);
// console.table(m2.matrix);
// m1.multiply(m2);
// console.table(m1.matrix);