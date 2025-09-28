// Fonction d'activation
int sign(float n) {
  if (n >=0) return 1;
  else return -1;
}

// Perceptron
class Perceptron {
   float[] weights = new float[2];
   float lr = 0.01; // learning rate
   int guess;
   int error;
   float delta;
   
   // constructeur
   Perceptron() {
     // initialisation des poids
     for(int i = 0; i < weights.length; i++){
       weights[i] = random(-1,1);
       println("initial w"+i+" : "+weights[i]);
     }
   }
    
   int guess(float[] inputs){
     float sum = 0;
     for(int i = 0; i < weights.length; i++){
       sum += inputs[i]*weights[i];
     }
     int output = sign(sum);
     return output;
   }
   
   void train(float[] inputs, int target){
     guess = guess(inputs);
     // int guess = guess(inputs);
     error = target - guess; // vaut 0 si ok, -2 ou +2 sinon
     // int error = target - guess; // vaut 0 si ok, -2 ou +2 sinon
     
     // correction des poids
     for (int i = 0; i < weights.length; i++) {
       delta = error * inputs[i] * lr;       
       //float delta = error * inputs[i] * lr;
       weights[i] += delta; // pas de correction si vaut 0     
       //println(i+" : "+weights[i]+"_err,inp,lr : "+error+" , "+inputs[i]+","+lr+"_delta : "+delta); 
       //println(i+" : "+weights[i]);        
     }
   }
   
}
