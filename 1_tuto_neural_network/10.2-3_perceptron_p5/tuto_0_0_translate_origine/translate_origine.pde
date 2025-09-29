void setup() {
  size(400, 400);
  background(255);
  stroke(255, 0, 0); // Rouge pour la droite
  strokeWeight(2);

  // 1. Déplacer l'origine en bas à gauche
  translate(0, height);
  // 2. Inverser l'axe Y
  scale(1, -1);

  // 3. Tracer y = x (après inversion, c'est line(0, 0, 400, -400))
  line(0, 0, 400, 400); // Oui, 400,400 car scale(-1) inverse déjà !

}
