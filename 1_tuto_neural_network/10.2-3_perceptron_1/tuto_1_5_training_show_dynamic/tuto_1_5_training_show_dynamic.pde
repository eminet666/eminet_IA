// source : https://www.youtube.com/watch?v=ntKn5TPHHAk
// à partir de 36:00 à 39:00
Perceptron brain;
Point[] points = new Point[100];
int trainingIndex = 0;

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
   
    int guess = brain.guess(inputs);
    if(guess == target) { fill(0,255,0); }
    else { fill(255,0,0); }
    
    noStroke();
    ellipse(pt.x, pt.y, 6, 6);
  }
  
  // point par point
  Point training = points[trainingIndex];
  float[] inputs = {training.x, training.y};
  int target = training.label;
  brain.train(inputs, training.label); 
  trainingIndex++;
  if(trainingIndex == points.length){ trainingIndex = 0;}
  
}

// lancer on voit le training converger  
