// Variables globales
let brain;
let points = [];
let testSet;
let trainingIndex = 0;
let modelTrained = false;
let testingMode = false;
let showTestPoints = false;

// Fonction de la ligne de référence
function f(x) {
    return -0.3 * x + 0.4;
}

// Fonction d'activation
function sign(n) {
    return n >= 0 ? 1 : -1;
}

// Classe Point
class Point {
    constructor(x_, y_) {
        if (x_ !== undefined && y_ !== undefined) {
            this.x = x_;
            this.y = y_;
        } else {
            this.x = random(-1, 1);
            this.y = random(-1, 1);
        }
        this.bias = 1;

        let lineY = f(this.x);
        this.label = this.y > lineY ? 1 : -1;
    }

    pixelX() {
        return map(this.x, -1, 1, 0, width);
    }

    pixelY() {
        return map(this.y, -1, 1, height, 0);
    }

    show() {
        if (this.label === 1) {
            fill(255);
        } else {
            fill(0);
        }
        let px = this.pixelX();
        let py = this.pixelY();
        ellipse(px, py, 10, 10);
    }
}

// Classe Perceptron
class Perceptron {
    constructor(n) {
        this.weights = [];
        this.lr = 0.01;
        this.trained = false;

        for (let i = 0; i < n; i++) {
            this.weights[i] = random(-1, 1);
            console.log('Poids initial ' + i + ' : ' + this.weights[i]);
        }
    }

    guess(inputs) {
        let sum = 0;
        for (let i = 0; i < this.weights.length; i++) {
            sum += inputs[i] * this.weights[i];
        }
        return sign(sum);
    }

    train(inputs, target) {
        let guess = this.guess(inputs);
        let error = target - guess;

        for (let i = 0; i < this.weights.length; i++) {
            this.weights[i] += error * inputs[i] * this.lr;
        }
    }

    guessY(x) {
        let m = -this.weights[0] / this.weights[1];
        let b = -this.weights[2] / this.weights[1];
        return m * x + b;
    }

    isTrained(pointsArray) {
        for (let pt of pointsArray) {
            let inputs = [pt.x, pt.y, pt.bias];
            if (this.guess(inputs) !== pt.label) {
                return false;
            }
        }
        this.trained = true;
        return true;
    }
}

// Classe TestSet
class TestSet {
    constructor(n) {
        this.n = n;
        this.testPoints = [];
        for (let i = 0; i < n; i++) {
            this.testPoints[i] = new Point();
        }
    }
}

// Setup P5.js
function setup() {
    let canvas = createCanvas(400, 400);
    canvas.parent('canvas-container');

    brain = new Perceptron(3);
    testSet = new TestSet(50);

    for (let i = 0; i < 50; i++) {
        points[i] = new Point();
    }
}

// Draw P5.js
function draw() {
    background(255);

    // Ligne de référence (noire)
    stroke(0);
    let p1 = new Point(-1, f(-1));
    let p2 = new Point(1, f(1));
    line(p1.pixelX(), p1.pixelY(), p2.pixelX(), p2.pixelY());

    // Ligne de décision (verte)
    stroke(0, 255, 0);
    let p3 = new Point(-1, brain.guessY(-1));
    let p4 = new Point(1, brain.guessY(1));
    line(p3.pixelX(), p3.pixelY(), p4.pixelX(), p4.pixelY());

    if (!testingMode) {
        // Mode entraînement
        for (let pt of points) {
            pt.show();
        }

        // Colorier les prédictions
        for (let pt of points) {
            let inputs = [pt.x, pt.y, pt.bias];
            let guess = brain.guess(inputs);
            fill(guess === pt.label ? color(0, 255, 0) : color(255, 0, 0));
            noStroke();
            ellipse(pt.pixelX(), pt.pixelY(), 6, 6);
        }

        // Entraînement
        if (!modelTrained) {
            let training = points[trainingIndex];
            let inputs = [training.x, training.y, training.bias];
            brain.train(inputs, training.label);
            trainingIndex = (trainingIndex + 1) % points.length;
        }

        // Vérification de la convergence
        if (!modelTrained && brain.isTrained(points)) {
            console.log("TRAINING MODEL OK");
            console.log("\n--- POIDS FINAUX ---");
            console.log('w0 (x)     : ' + brain.weights[0]);
            console.log('w1 (y)     : ' + brain.weights[1]);
            console.log('w2 (bias)  : ' + brain.weights[2]);
            let m = -brain.weights[0] / brain.weights[1];
            let b = -brain.weights[2] / brain.weights[1];
            console.log('Ligne de décision : y = ' + m + ' * x + ' + b);
            modelTrained = true;
        }
    } else {
        // Mode test
        if (showTestPoints) {
            for (let i = 0; i < testSet.testPoints.length; i++) {
                let pt = testSet.testPoints[i];
                let inputs = [pt.x, pt.y, pt.bias];
                let guess = brain.guess(inputs);

                fill(guess === pt.label ? color(0, 0, 255) : color(255, 0, 0));
                noStroke();
                ellipse(pt.pixelX(), pt.pixelY(), 7, 7);
            }
        }
    }
}

// Gestion des touches
function keyPressed() {
    if (key === 't' || key === 'T') {
        if (modelTrained) {
            testSet = new TestSet(50);
            testingMode = true;
            showTestPoints = true;

            let correct = 0;
            for (let pt of testSet.testPoints) {
                let inputs = [pt.x, pt.y, pt.bias];
                if (brain.guess(inputs) === pt.label) correct++;
            }
            console.log("\n--- NOUVEAU TEST ---");
            console.log('Précision: ' + (100.0 * correct / testSet.testPoints.length).toFixed(2) + '%');
        } else {
            console.log("Le modèle n'est pas encore entraîné. Appuyez sur 't' après la fin de l'entraînement.");
        }
    }
}