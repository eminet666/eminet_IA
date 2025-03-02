var brain;

function setup() {

    // TEST multiply
    // let a = new Matrix(2, 3);
    // let b = new Matrix(3, 2);
    // a.randomize();
    // b.randomize();
    // console.table(a.data);
    // console.table(b.data);

    // let c = a.multiply(b);
    // console.table(c.data);

    // TEST transpose
    // let a = new Matrix(2, 3);
    // a.randomize();
    // let b = a.transpose();
    // console.table(a.data);
    // console.table(b.data);

    // TEST static multiply, print
    // let m1 = new Matrix(2, 2);
    // m1.randomize();
    // m1.print();
    // m1.multiply(2);
    // m1.print();

    // let m2 = new Matrix(2,2);
    // m2.randomize();
    // m2.print();
    
    // let m3 = Matrix.multiply(m1, m2);
    // m3.print();

    // TEST map
    // let a = new Matrix(2, 3);
    // a.randomize();
    // a.print();

    // function doubleIt(x){
    //     return x * 2;
    // }

    // a.map(doubleIt);
    // a.print();

    // TEST static transpose
    let a = new Matrix(2, 3);
    a.randomize();
    a.print();
    let b = Matrix.transpose(a);
    b.print();



}

function draw() {
    
}