// source : https://www.youtube.com/watch?v=ntKn5TPHHAk
// à partir de 28:00 à 36:00
Perceptron brain;
Point[] points = new Point[100];

void setup() {
  size(400,400);
  brain = new Perceptron();
  
  // initialisation d'un dataset
  for (int i = 0; i < points.length; i++) {
    points[i] = new Point();
  }
  
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
    int target = pt.label;
    //brain.train(inputs, pt.label); //à désactiver pour voir juste run 1
    
    int guess = brain.guess(inputs);
    if(guess == target) { fill(0,255,0); }
    else { fill(255,0,0); }
    
    noStroke();
    ellipse(pt.x, pt.y, 6, 6);
  }
}

// lancer ... mais on ne voit toujours pas (sauf déactiver le training)  
