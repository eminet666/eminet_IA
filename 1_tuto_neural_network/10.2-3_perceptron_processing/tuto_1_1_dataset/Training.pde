class Point {
   float x;
   float y;
   int label;
   
   Point() {
     x = random(width);
     y = random(height);
     
     if (x > y) { label = 1;}
     else { label = -1;}
     println("x1:"+nf(x, 3, 3)+" , x2:"+nf(y, 3, 3)+" => label:"+label);
   }
   
   void show() {
       if(label == 1) { fill(255);}
       else { fill(0);}
       ellipse(x,y,10,10);
   }
}
