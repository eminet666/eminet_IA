void setup() {
  size(400, 400);  // Canvas de 400x400
  background(255); // Fond blanc
  stroke(255, 0, 0); // Couleur rouge pour la droite
  strokeWeight(2);   // Épaisseur du trait

  // Tracer la droite y = x (de (0,0) à (400,400))
  line(0, 0, 400, 400);

  // Optionnel : Tracer les axes X et Y pour visualiser l'origine
  stroke(0); // Noir pour les axes
  line(0, 0, 400, 0); // Axe X (horizontal)
  line(0, 0, 0, 400); // Axe Y (vertical)
}
