// Fonction d'activation
function sign(n) {
  return n >= 0 ? 1 : -1;
}

// Classe Perceptron
class Perceptron {
  constructor() {
    this.weights = [0, 0];
    // Initialisation des poids
    for (let i = 0; i < this.weights.length; i++) {
      this.weights[i] = random(-1, 1);
    }
    console.log("poids : " + this.weights[0] + ", " + this.weights[1]);
  }

  guess(inputs) {
    console.log("inputs : " + inputs[0] + ", " + inputs[1]);
    let sum = 0;
    for (let i = 0; i < this.weights.length; i++) {
      sum += inputs[i] * this.weights[i];
    }
    console.log("sum = " + sum);
    const output = sign(sum);
    return output;
  }
}
