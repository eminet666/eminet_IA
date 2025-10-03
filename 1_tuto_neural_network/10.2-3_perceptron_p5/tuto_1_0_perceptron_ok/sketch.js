let p;

function setup() {
  createCanvas(200, 200);
  p = new Perceptron();
  const inputs = [-1, 0.5];
  const guess = p.guess(inputs);
  console.log("output : " + guess);
}

function draw() {
  // Vide - comme dans l'exemple original
}
