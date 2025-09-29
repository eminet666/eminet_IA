Perceptron brain;
Point[] points = new Point[50];
TestSet testSet;
int trainingIndex = 0;
boolean modelTrained = false;
boolean testingMode = false;
boolean showTestPoints = false;

void setup() {
  size(400, 400);
  brain = new Perceptron(3);
  testSet = new TestSet(50); // Initialisation avec 50 points

  for (int i = 0; i < points.length; i++) {
    points[i] = new Point();
  }
}

void draw() {
  background(255);

  // Toujours afficher les lignes de référence et de décision
  stroke(0);
  Point p1 = new Point(-1, f(-1));
  Point p2 = new Point(1, f(1));
  line(p1.pixelX(), p1.pixelY(), p2.pixelX(), p2.pixelY());

  stroke(0, 255, 0);
  Point p3 = new Point(-1, brain.guessY(-1));
  Point p4 = new Point(1, brain.guessY(1));
  line(p3.pixelX(), p3.pixelY(), p4.pixelX(), p4.pixelY());

  if (!testingMode) {
    // Mode entraînement: afficher les points d'entraînement
    for (Point pt : points) {
      pt.show();
    }

    // Colorier les prédictions
    for (Point pt : points) {
      float[] inputs = {pt.x, pt.y, pt.bias};
      int guess = brain.guess(inputs);
      fill(guess == pt.label ? color(0, 255, 0) : color(255, 0, 0));
      noStroke();
      ellipse(pt.pixelX(), pt.pixelY(), 6, 6);
    }

    // Entraînement seulement si le modèle n'est pas encore entraîné
    if (!modelTrained) {
      Point training = points[trainingIndex];
      float[] inputs = {training.x, training.y, training.bias};
      brain.train(inputs, training.label);
      trainingIndex = (trainingIndex + 1) % points.length;
    }

    // Vérification de la convergence
    if (!modelTrained && brain.isTrained(points)) {
      println("TRAINING MODEL OK");
      println("\n--- POIDS FINAUX ---");
      println("w0 (x)     : " + brain.weights[0]);
      println("w1 (y)     : " + brain.weights[1]);
      println("w2 (bias)  : " + brain.weights[2]);
      float m = -brain.weights[0] / brain.weights[1];
      float b = -brain.weights[2] / brain.weights[1];
      println("Ligne de décision : y = " + m + " * x + " + b);
      modelTrained = true;
    }
  } else {
    // Mode test: afficher les points de test
    if (showTestPoints) {
      for (int i = 0; i < testSet.testPoints.length; i++) {
        Point pt = testSet.testPoints[i];
        float[] inputs = {pt.x, pt.y, pt.bias};
        int guess = brain.guess(inputs);

        fill(guess == pt.label ? color(0, 0, 255) : color(255, 0, 0));
        noStroke();
        ellipse(pt.pixelX(), pt.pixelY(), 7, 7); // Disques de 7px
      }
    }
  }
}

void keyPressed() {
  if (key == 't' || key == 'T') {
    if (modelTrained) {
      // Générer un NOUVEAU jeu de test à chaque appui sur 't'
      testSet = new TestSet(50);
      testingMode = true;
      showTestPoints = true;

      // Calculer et afficher la précision
      int correct = 0;
      for (Point pt : testSet.testPoints) {
        float[] inputs = {pt.x, pt.y, pt.bias};
        if (brain.guess(inputs) == pt.label) correct++;
      }
      println("\n--- NOUVEAU TEST ---");
      println("Précision: " + nf(100.0 * correct / testSet.testPoints.length, 1, 2) + "%");
    } else {
      println("Le modèle n'est pas encore entraîné. Appuyez sur 't' après la fin de l'entraînement.");
    }
  }

//   if (key == 'c' || key == 'C') {
//     if (modelTrained) {
//       showTestPoints = false;
//       testingMode = false;
//       println("Écran nettoyé (lignes conservées)");
//     } else {
//       println("Le modèle n'est pas encore entraîné. Impossible de nettoyer.");
//     }
//   }
}
