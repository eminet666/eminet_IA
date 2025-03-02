import java.io.File;
File sketchFolder = new File(sketchPath()); // Récupère le chemin du dossier du sketch
File parentFolder = sketchFolder.getParentFile(); // Va dans le dossier parent
File targetFile = new File(parentFolder, "data/full_numpy_bitmap_train.npy");
size(280,280);

//// step 0 _ taille du fichier
byte[] data = loadBytes(targetFile);
//println(data.length); //99446560
//int nbimg = data.length/784; // image 28x28px
//println(nbimg); // 126845 environ car en-tête

//// step 1 : visualisation de la première image
//int start = 80; // offset de l'en-tête
//PImage img = createImage(28,28, RGB);
//img.loadPixels();
//for (int i = 0; i < 784; i++){
//    int index = i + start; 
//    int val = data[index];
//    img.pixels[i] = color(val & 0xff); // pour mettre au format 0-255
//}
//img.updatePixels();
//image(img,0,0);

//// step 2 : chargement 100 images
//int total = 100;
//for(int n = 0; n < total; n++){
//    int start = 80 + n * 784; 
//    PImage img = createImage(28,28, RGB);
//    img.loadPixels();
//    for (int i = 0; i < 784; i++){
//        int index = i + start;
//        int val = data[index];
//        img.pixels[i] = color(255 - val & 0xff); // fond blanc
//    }
//    img.updatePixels();
//    int x = 28 * (n % 10);
//    int y = 28 * (n / 10);
//    image(img, x, y);
//}

// step3 : save in a format usable in P5
// json or just save bytes
int total = 1000;
byte[] outdata = new byte[total*784];
int outindex = 0;

println("Binary dataset creating ...");
for(int n = 0; n < total; n++){
    int start = 80 + n * 784; 
    for (int i = 0; i < 784; i++){
        int index = i + start;
        byte val = data[index]; // change format
        outdata[outindex] = val;
        outindex++;
    }
}

File outDataFile = new File(parentFolder, "data/trains1000.bin");
saveBytes(outDataFile, outdata);
println("Binary dataset created");
