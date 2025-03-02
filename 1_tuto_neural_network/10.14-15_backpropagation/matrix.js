class Matrix {

    constructor(rows, cols){
        this.rows = rows;
        this.cols = cols;
        this.data = [];

        for (let i = 0; i < this.rows; i++){
            this.data[i] = [];
            for (let j = 0; j < this.cols; j++){
                this.data[i][j] = 0;
            }
        }

    }

    static fromArray(arr) {
        let m = new Matrix(arr.length, 1);
        for (let i = 0; i < arr.length; i++){
            m.data[i][0] = arr[i];
        }
        //m.print();
        return m;
    }

    toArray(){
        let arr = [];
        for (let i = 0; i < this.rows; i++){
            for (let j = 0; j < this.cols; j++){
                arr.push(this.data[i][j]);
            }
        }  
        return arr;      
    }

    randomize() {
        for (let i = 0; i < this.rows; i++){
            for (let j = 0; j < this.cols; j++){
                this.data[i][j] = Math.random() * 2 - 1;
            }
        }
    }

    static subtract(a, b){
        // return new Matrix a-b
        // b.print();
        let result = new Matrix(a.rows, a.cols);
        for (let i = 0; i < result.rows; i++){
            for (let j = 0; j < result.cols; j++){
                result.data[i][j] = a.data[i][j] - b.data[i][j];
            }
        }  
        return result;      
    }

    add(n) {
        
        if (n instanceof Matrix){
            for (let i = 0; i < this.rows; i++){
                for (let j = 0; j < this.cols; j++){
                    this.data[i][j] += n.data[i][j];
                }
            }
        }
        else {
            for (let i = 0; i < this.rows; i++){
                for (let j = 0; j < this.cols; j++){
                    this.data[i][j] += n;
                }
            }
        }
        
    }

    static multiply(a,b){
            // data product
            if(a.cols != b.rows){
                console.log("columns of A must match rows of B");
                return undefined;
            }
            let result = new Matrix(a.rows, b.cols);

            for (let i = 0; i < result.rows; i++){
                for (let j = 0; j < result.cols; j++){
                    // dot product of values in cells
                    let sum  = 0;
                    for (let k = 0; k < a.cols; k++){
                        sum += a.data[i][k] * b.data[k][j];
                    }
                    result.data[i][j] = sum;
                }
            }
            return result;
    }

    multiply(n) {
        // scalar product
        for (let i = 0; i < this.rows; i++){
            for (let j = 0; j < this.cols; j++){
                this.data[i][j] *= n;
            }
        }
    }

    map(func) {
        // apply a function to every element of matrix
        for (let i = 0; i < this.rows; i++){
            for (let j = 0; j < this.cols; j++){
                let val = this.data[i][j];
                this.data[i][j] = func(val);
            }
        }
    }

    // transpose() {
    //     let result = new Matrix(this.cols, this.rows);
    //     for (let i = 0; i < this.rows; i++){
    //         for (let j = 0; j < this.cols; j++){
    //             result.data[j][i] = this.data[i][j];
    //         }
    //     }
    //     return result;
    // }

    static transpose(a) {
        let result = new Matrix(a.cols, a.rows);
        for (let i = 0; i < a.rows; i++){
            for (let j = 0; j < a.cols; j++){
                result.data[j][i] = a.data[i][j];
            }
        }
        return result;
    }    

    print(){
        console.table(this.data);
    }

}