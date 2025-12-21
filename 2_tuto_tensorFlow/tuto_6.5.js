const model = tf.sequential(); // création du modèle  vide (réseau de neurones)

// couche cachée
const hidden = tf.layers.dense({ // création de la couche cachée
    units: 4,               // nombre de neurones   
    inputShape : [2],       // forme des données d'entrée => 2 valeurs en entrée
    activation :'sigmoid'   // fonction d'activation = sigmoïde
});
model.add(hidden);  // ajout de la couche cachée au modèle

// couche de sortie
const output = tf.layers.dense({ // création de la couche de sortie
    units: 3,               // nombre de neurones de sortie => 4 valeurs en sortie
    activation :'sigmoid'   // fonction d'activation = sigmoïde
});
model.add(output); // ajout de la couche de sortie au modèle

const sgdOpt = tf.train.sgd(0.1); // optimiseur SGD avec un taux d'apprentissage de 0.1
model.compile({             // compilation du modèle
    optimizer: sgdOpt,      // optimiseur = SGD
    // loss : 'meanSquaredError'      // fonction de perte = erreur quadratique moyenne
    loss : tf.losses.meanSquaredError // fonction de perte = erreur quadratique moyenne
});


