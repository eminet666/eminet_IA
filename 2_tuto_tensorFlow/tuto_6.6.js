const model = tf.sequential();

const hidden = tf.layers.dense({ // dens is a fully connected layer
    units: 4,               // nb of nodes
    inputShape : [2],       // input shape
    activation :'sigmoid'
});
model.add(hidden);

const output = tf.layers.dense({
    units: 1, // input shape inferred from input layer
    activation :'sigmoid'
});
model.add(output);

const lr = 0.1;
const sgdOpt = tf.train.sgd(lr);
model.compile({
    optimizer: sgdOpt,
    // loss : 'meanSquaredError'
    loss : tf.losses.meanSquaredError
});

// // step 0 : predict
// const xs = tf.tensor2d(     // inputs
//     [0.25, 0.92],
//     [0.12, 0.30],
//     [0.24, 0.27],
//     [0.20, 0.66],
// );
// let ys = model.predict(xs); // outputs
// outputs.print();

// fit
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

// model.fit(xs, ys).then((response)=> console.log(response.history.loss[0]));
// const config = {
//     epochs: 5
// }
// model.fit(xs, ys, config ).then((response)=> console.log(response.history.loss[0]));

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
        console.log(response.history.loss[0]);
    }
}