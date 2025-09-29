// source : https://www.youtube.com/watch?v=ntKn5TPHHAk
// de 11:40 à 17:30
Perceptron p;

void setup() {
  size(200,200);
  p = new Perceptron();
  float[] inputs = {-1, 0.5};
  int guess = p.guess(inputs);
  println("output : "+guess);
}

void draw(){
}

// lancer plusieurs fois le programme
// guess vaut 1 ou -1 selon la valeur random des weights
