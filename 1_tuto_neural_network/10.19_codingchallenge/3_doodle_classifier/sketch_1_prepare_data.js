const len = 784;
const total_data = 1000;

let cats_data;
let trains_data;
let rainbows_data;

let cats = {};
let trains = {};
let rainbows = {};

// step 0 : chargement des data
function preload(){
    cats_data = loadBytes("./data/cats1000.bin");
    trains_data = loadBytes("./data/trains1000.bin");
    rainbows_data = loadBytes("./data/rainbows1000.bin");
}

function prepareData(category, data){
    category.training = [];
    category.testing = [];
    for (let i = 0; i < total_data; i++){
        let offset = i * len;
        let threshold = floor(0.8 * total_data);
        if(i < threshold) {
            category.training[i] = data.bytes.subarray(offset, offset+len);   
        } else {
            category.testing[i-threshold] = data.bytes.subarray(offset, offset+len);
        }
   }
}


function setup(){
    createCanvas(280,280);
    background(0);

    // // step1 check images 
    // // (en javascript un pixel est divisé en 4 valeurs rgba)
    // let total = 100;
    // for (let n = 0; n < total; n++){
    //     let img = createImage(28,28);
    //     img.loadPixels();
    //     let offset = n * 784;
    //     for (let i = 0; i < 784; i++){
    //         let val = 255 - cats.bytes[i + offset];
    //         img.pixels[i * 4 + 0] = val;
    //         img.pixels[i * 4 + 1] = val;
    //         img.pixels[i * 4 + 2] = val;
    //         img.pixels[i * 4 + 3] = 255;
    //     }
    //     img.updatePixels();
    //     let x = (n % 10) * 28;
    //     let y = floor(n / 10) * 28;
    //     image(img, x, y);
    // }

    // // step 2 : prepare data cat
    // cats.training = [];
    // cats.testing = [];
    // for (let i = 0; i < total_data; i++){
    //     let offset = i * len;
    //     let threshold = floor(0.8 * total_data);
    //     if(i < threshold) {
    //         cats.training[i] = cats_data.bytes.subarray(offset, offset+len);   
    //     } else {
    //         cats.testing[i-threshold] = cats_data.bytes.subarray(offset, offset+len);
    //     }
    // }

    // step 3 : prepare data function
    prepareData(cats, cats_data);
    prepareData(rainbows, rainbows_data);
    prepareData(trains, trains_data);

}