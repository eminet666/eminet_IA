const len = 784;

let datafile = "./data/rainbows1000.bin";
let xxx_data;

function preload(){
    xxx_data = loadBytes(datafile);
    console.log(xxx_data);
}


function setup(){
    createCanvas(280,280);
    background(0);

    // step1 check images 
    // (en javascript un pixel est divisé en 4 valeurs rgba)
    let total = 100;
    for (let n = 0; n < total; n++){
        let img = createImage(28,28);
        img.loadPixels();
        let offset = n * len;
        for (let i = 0; i < len; i++){
            let val = 255 - xxx_data.bytes[i + offset];
            img.pixels[i * 4 + 0] = val;
            img.pixels[i * 4 + 1] = val;
            img.pixels[i * 4 + 2] = val;
            img.pixels[i * 4 + 3] = 255;
        }
        img.updatePixels();
        let x = (n % 10) * 28;
        let y = floor(n / 10) * 28;
        image(img, x, y);
    }

}