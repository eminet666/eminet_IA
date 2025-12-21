

function setup(){
    noCanvas();


    // STEP 0 : shape & dtype
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

    // STEP 1 : modifier les valeurs du tensor
    // les valeurs d'un tensor ne peuvent être changées donc on passe par une variable
    const vtense = tf.variable(tense); // crée une variable à partir du tensor
    //console.log("vtense : "+vtense);

    // STEP 2 : operations méthematiques
    const values2 = [];
    for (let i = 0; i < 15; i++){
        values2[i] = random(0,100);
    }    
    const shapeA = [5,3];
    const shapeB = [3,5];
    const a = tf.tensor(values, shapeA, 'int32');
    const b = tf.tensor(values2, shapeB, 'int32');
    const sum = a.add(b.transpose()); // additionne a et la transposée de b
    sum.print();
    const c=a.matMul(b); // produit matriciel de a et b
    c.print();
    // const bb = b.transpose();
    // const c = a.matMul(bb)

}