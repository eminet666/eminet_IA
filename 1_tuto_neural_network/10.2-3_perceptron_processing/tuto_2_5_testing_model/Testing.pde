class TestSet {
  Point[] testPoints;
  int n;

  TestSet(int n_) {
    n = n_;
    testPoints = new Point[n];
    for (int i = 0; i < n; i++) {
      testPoints[i] = new Point(); // Nouveaux points aléatoires à chaque création
    }
  }
}
