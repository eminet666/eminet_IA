let training_data = [
    {
        inputs: [0,1], 
        targets:  [1]
    },
    {
        inputs: [1,0], 
        targets: [1]
    }, 
    {
        inputs: [0,0], 
        targets: [0]
    },
    {
        inputs: [1,1], 
        targets: [0]
    }           
];

function setup() {

    // // TEST ECRITURE CODE
    let nn = new NeuralNetwork(2,2,2);
    let inputs = [1,0];
    let targets = [1,0];

    // let output = nn.feedForward(input);
    nn.train(inputs, targets);

    // TEST XOR PROBLEME
    // let nn = new NeuralNetwork(2,2,1);
    // for (let i = 0; i < 10; i++){
    //     let data = random(training_data);
    //     for (data of training_data) {
    //         nn.train(data.inputs, data.targets);
    //     }
    // }
    
    //nn.train([1,0], [1,0]);

    // console.log(nn.feedForward([1,0]));
    // console.log(nn.feedForward([0,1]));
    // console.log(nn.feedForward([1,1]));
    // console.log(nn.feedForward([0,0]));


}

function draw() {
    
}