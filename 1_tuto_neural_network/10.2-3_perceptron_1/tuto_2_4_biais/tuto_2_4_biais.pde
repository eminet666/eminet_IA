// source : https://www.youtube.com/watch?v=DGxIcDjPzac&t=20s
// à partir de 19:00 à 15:00
Perceptron brain;
Point[] points = new Point[100];
int trainingIndex = 0;

void setup() {
  size(400,400);
  brain = new Perceptron(3);
  
  // initialisation d'un dataset
  for (int i = 0; i < points.length; i++) {
    points[i] = new Point();
  }
  
}

void draw(){
  background(255);
  stroke(0);
  //line(0,height, width, 0);
  Point p1 = new Point(-1, f(-1));
  Point p2 = new Point(1, f(1));
  line(p1.pixelX(), p1.pixelY(), p2.pixelX(), p2.pixelY());
  
  // afficher les points
  for (Point pt : points){
    pt.show();
  }
  
  // guess or not by colors
  for (Point pt : points) {
    float[] inputs = {pt.x, pt.y, pt.bias};
    int target = pt.label;
   
    int guess = brain.guess(inputs);
    if(guess == target) { fill(0,255,0); }
    else { fill(255,0,0); }
    
    noStroke();
    ellipse(pt.pixelX(), pt.pixelY(), 6, 6);
  }
  
  // point par point
  Point training = points[trainingIndex];
  float[] inputs = {training.x, training.y, training.bias};
  int target = training.label;
  
  // ajustement des poids
  brain.train(inputs, training.label); 
  
  trainingIndex++;
  if(trainingIndex == points.length){ trainingIndex = 0;}
  
}

// le biais est nécessaire car si x,y = 0,0, les poids sont neutralisés 
// le biais vaut toujours 1
// y = -w0/w1 * x + -w2/w1 * 1 (car w0x + w1y + w2b = 0)
