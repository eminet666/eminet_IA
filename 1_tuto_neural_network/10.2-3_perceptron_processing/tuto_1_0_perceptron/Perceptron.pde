// Fonction d'activation
int sign(float n) {
  if (n >=0) return 1;
  else return -1;
}

// Perceptron
class Perceptron {
   float[] weights = new float[2];
   
   // constructeur
   Perceptron() {
     // initialisation des poids
     for(int i = 0; i < weights.length; i++){
       weights[i] = random(-1,1);
     }
     println("poids : "+weights[0]+", "+weights[1]);
   }
    
   int guess(float[] inputs){
     println("inputs : "+inputs[0]+", "+inputs[1]);
     float sum = 0;
     for(int i = 0; i < weights.length; i++){
       sum += inputs[i]*weights[i];
     }
     println( "sum = "+sum);
     int output = sign(sum);
     return output;
   }
  
  
}
