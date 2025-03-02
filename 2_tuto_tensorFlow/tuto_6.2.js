

function setup(){
    noCanvas();
    // tensors are undimentionals groups of numbers

    // syntax tf.tensor(values, shape, dtype)
    // dtype = float32 | int32 | bool

    // // step 0 : tensor array
    // const data0 = tf.tensor([1,2,3,4]);
    // data0.print();
    // console.log(data0.toString);
    // console.log(data0);

    // // step 1 : tensor matrix
    // const data1 = tf.tensor([0,0,127,255,100,50,24,54], [2,2,2]);
    // data1.print();
    // console.log(data1);
    // // int32 > floor (partie entière)

    // step 2 : shape & dtype
    const values = [];
    for (let i = 0; i < 30; i++){
        values[i] = random(0,100);
    }
    const shape = [2,5,3];
    const data2 = tf.tensor(values, shape, 'int32');
    data2.print();

    // step3 : scalar, tensor1d, tensor2d, tensor3d
    const num = tf.scalar(4); // scalar
}