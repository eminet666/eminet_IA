

function setup(){
    noCanvas();


    // step 0 : shape & dtype
    const values = [];
    for (let i = 0; i < 30; i++){
        values[i] = random(0,100);
    }
    const shape = [2,5,3];
    const tense = tf.tensor3d(values, shape, 'int32');
    //data2.print();
    // console.log(tense.data()); // renvoie Promise { <state>: "pending" } = copie vers GPU
    // tense.data().then( function(stuff){
    //     console.log(stuff); // execute la function quans synchronisée
    // })
    //console.log(tense.dataSync()); // affiche les data une fois synchronisées
    //console.log(tense.get(0)); // renvoie la valeur 0 pb!

    // step 1 : modifier les valeurs du tensor
    // les valeurs d'un tensor ne peuvent être changées donc on passe par une vairable
    const vtense = tf.variable(tense);
    //console.log("vtense : "+vtense);

    // step 2 : operations méthematiques
    const values2 = [];
    for (let i = 0; i < 15; i++){
        values2[i] = random(0,100);
    }    
    const shapeA = [5,3];
    const shapeB = [3,5];
    const a = tf.tensor(values2, shapeA, 'int32');
    const b = tf.tensor(values2, shapeB, 'int32');
    const c=a.matMul(b);
    c.print();
    // const bb = b.transpose();
    // const c = a.matMul(bb)

}