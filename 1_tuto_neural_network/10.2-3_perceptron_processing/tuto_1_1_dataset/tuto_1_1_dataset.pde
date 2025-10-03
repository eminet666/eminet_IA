// source : https://www.youtube.com/watch?v=ntKn5TPHHAk
// de 19:00 à 23:00
Perceptron p;
Point[] points = new Point[100];

void setup() {
  size(400,400);
  p = new Perceptron();
  
  // initialisation d'un dataset
  for (int i = 0; i < points.length; i++) {
    points[i] = new Point();
  }
  
}

void draw(){
  background(255);
  translate(0, height); // 1. Déplacer l'origine en bas à gauche
  scale(1, -1); // 2. Inverser l'axe Y   
  stroke(0);
  line(0,0, width, height);
  for (Point pt : points){
    pt.show();
  }
  
  
}

// lancer pour visualiser le dataset (known training data)
