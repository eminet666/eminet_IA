// Fonction d'activation
int sign(float n) {
  if (n >= 0) return 1;
  else return -1;
}

// Perceptron
class Perceptron {
  float[] weights;
  float lr = 0.01; // learning rate
  boolean trained = false; // Flag pour suivre l'état d'entraînement

  // Constructeur
  Perceptron(int n) {
    weights = new float[n];
    // Initialisation aléatoire des poids
    for (int i = 0; i < weights.length; i++) {
      weights[i] = random(-1, 1);
      println("Poids initial " + i + " : " + weights[i]);
    }
  }

  // Prédiction binaire (-1 ou 1)
  int guess(float[] inputs) {
    float sum = 0;
    for (int i = 0; i < weights.length; i++) {
      sum += inputs[i] * weights[i];
    }
    return sign(sum);
  }

  // Entraînement : ajustement des poids
  void train(float[] inputs, int target) {
    int guess = guess(inputs);
    int error = target - guess; // Erreur : 0 (correct), -2 ou +2 (incorrect)

    // Mise à jour des poids (si erreur ≠ 0)
    for (int i = 0; i < weights.length; i++) {
      weights[i] += error * inputs[i] * lr;
    }
  }

  // Prédiction de y pour un x donné (pour dessiner la ligne de décision)
  float guessY(float x) {
    float m = -weights[0] / weights[1]; // Pente
    float b = -weights[2] / weights[1]; // Ordonnée à l'origine
    return m * x + b;
  }

  // Vérifie si TOUTES les prédictions du dataset sont correctes
  boolean isTrained(Point[] points) {
    for (Point pt : points) {
      float[] inputs = {pt.x, pt.y, pt.bias};
      if (guess(inputs) != pt.label) {
        return false; // Au moins une erreur → pas encore entraîné
      }
    }
    trained = true; // Toutes les prédictions sont correctes
    return true;
  }
}
