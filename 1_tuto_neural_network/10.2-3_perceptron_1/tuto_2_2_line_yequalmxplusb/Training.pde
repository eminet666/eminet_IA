float f(float x) {
  // y = mx + b
  return 0.3 * x + 0.2;
}


class Point {
   float x;
   float y;
   int label;
   
   Point(float x_, float y_){
      x = x_;
      y = y_;
   }
   
   Point() {
     x = random(-1,1);
     y = random(-1,1);
     
     if (x > y) { label = 1;}
     else { label = -1;}
     //println(x+":"+y+":"+label);
   }
   
   float pixelX() { return map(x, -1, 1, 0, width);}
   float pixelY() { return map(y, -1, 1, height, 0);}
   
   void show() {
       if(label == 1) { fill(255);}
       else { fill(0);}
       
       float px = pixelX();
       float py = pixelY();
       ellipse(px,py,10,10);
   }
}

// affiche une ligne en y = mx + b
