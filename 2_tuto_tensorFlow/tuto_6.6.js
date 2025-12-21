const model = tf.sequential(); // création du modèle  vide (réseau de neurones)

const hidden = tf.layers.dense({ // dense is a fully connected layer
    units: 4,               // nb of nodes
    inputShape : [2],       // input shape
    activation :'sigmoid'   // activation function
});
model.add(hidden);

const output = tf.layers.dense({ // output layer
    units: 1,               // input shape inferred from input layer
    activation :'sigmoid'   // activation function
});
model.add(output);

const lr = 0.1;             // learning rate
const sgdOpt = tf.train.sgd(lr);
model.compile({
    optimizer: sgdOpt,
    // loss : 'meanSquaredError'
    loss : tf.losses.meanSquaredError
});

// fin de 6.5 script

// // STEP 0 : predict
// const xs = tf.tensor2d(     // inputs
//     [0.25, 0.92],
//     [0.12, 0.30],
//     [0.24, 0.27],
//     [0.20, 0.66],
// );
// let ys = model.predict(xs); // outputs
// outputs.print();

// STEP 1 : fit
// training data
const xs = tf.tensor2d([
    [0, 0],
    [0.5, 0.5],
    [0.1, 1]
]);

const ys = tf.tensor2d([
    [1],
    [0.5],
    [0]
]);

// const history = model.fit(xs, ys) ;
// console.log(history) // renvoie une promesse
// model.fit(xs, ys).then((response)=> console.log(history); // loss dans la réponse
// model.fit(xs, ys).then((response)=> console.log(response.history.loss[0]));

// const config = {
//     epochs: 5
// }
// model.fit(xs, ys, config ).then((response)=> console.log(response.history.loss[0]));

// // STEP 2 : train in async function
// train();
// async function train(){
//     const response = await model.fit(xs, ys);
//     console.log("loss : "+response.history.loss[0]);
// }

// STEP 3 : train in loop
train().then(() => {
    console.log("training complete");
    let outputs = model.predict(xs);
    outputs.print();
});

async function train(){
    for(let i = 0; i < 100; i++){
        const config = {
            shuffle: true,
            epochs : 10
        }
        const response = await model.fit(xs, ys, config);
        console.log("loss : "+response.history.loss[0]);
    }
}