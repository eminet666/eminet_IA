

function setup(){
    noCanvas();
}

function draw(){
    // step 0 : in draw function to test memory increase
    const values = [];
    for (let i = 0; i < 150000; i++){
        values[i] = random(0,100);
    }    
    const shape = [500,300];
    // const a = tf.tensor(values2, shape, 'int32');
    // const b = tf.tensor(values2, shape, 'int32');
    // const b_t = b.transpose();
    // const c=a.matMul(b_t);
    //c.print();

    // //step 1 : manuel
    // console.log(tf.memory().numTensors);
    // a.dispose();
    // b.dispose();
    // b_t.dispose();
    // c.dispose();
    // console.log(tf.memory().numTensors);

    // step 2 : tidy function
    // tf.tidy(myStuff);
    // function myStuff(){
    //     console.log("myStuff");
    //     const a = tf.tensor(values2, shape, 'int32');
    //     const b = tf.tensor(values2, shape, 'int32');
    //     const b_t = b.transpose();
    //     const c=a.matMul(b_t);
    // }

    // écriture alternative
    tf.tidy(() => {
        console.log("myStuff");
        const a = tf.tensor(values, shape, 'int32');
        const b = tf.tensor(values, shape, 'int32');
        const b_t = b.transpose();
        const c=a.matMul(b_t);
    });
    //console.log(tf.memory().numTensors);

    // step3 : function dispose
    const test = tf.tensor2d(values, shape);
    test.dispose();
    console.log(tf.memory().numTensors);
}