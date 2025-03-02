const model = tf.sequential();

const hidden = tf.layers.dense({
    units: 4,
    inputShape : [2],
    activation :'sigmoid'
});
model.add(hidden);

const output = tf.layers.dense({
    units: 4,
    activation :'sigmoid'
});
model.add(output);

const sgdOpt = tf.train.sgd(0.1);
model.compile({
    optimizer: sgdOpt,
    // loss : 'meanSquaredError'
    loss : tf.losses.meanSquaredError
});