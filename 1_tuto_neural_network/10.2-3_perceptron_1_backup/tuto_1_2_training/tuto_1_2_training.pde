// source : https://www.youtube.com/watch?v=ntKn5TPHHAk
// à partir de 28:00
Perceptron brain;
Point[] points = new Point[100];

void setup() {
  size(400,400);
  brain = new Perceptron();
  
  // initialisation d'un dataset
  for (int i = 0; i < points.length; i++) {
    points[i] = new Point();
  }
  
  float[] inputs = {-1, 0.5};
  int guess = brain.guess(inputs);
  //println("guess : "+guess);
}

void draw(){
  background(255);
  stroke(0);
  line(0,0, width, height);
  
  // afficher les points
  for (Point pt : points){
    pt.show();
  }
  
  // modifier les poids
  for (Point pt : points) {
    float[] inputs = {pt.x, pt.y};
    brain.train(inputs, pt.label);
  }
  
}

// lancer ... mais on ne voit pas le processus
