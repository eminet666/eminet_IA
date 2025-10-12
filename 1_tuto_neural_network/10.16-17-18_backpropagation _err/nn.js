// fonction sigmoid
function sigmoid(x){
    return (1 / (1 + Math.exp(-x)));
}

// dérivée sigmoid
function dsigmoid(y) {
    //return sigmoid(x) * (1 - sigmoid(x));
    return y * (1 - y);
}

class NeuralNetwork {

    constructor(input_nodes, hidden_nodes, output_nodes) {
        this.input_nodes = input_nodes;
        this.hidden_nodes = hidden_nodes;
        this.output_nodes = output_nodes;

        this.weights_ih = new Matrix(this.hidden_nodes, this.input_nodes);
        this.weights_ho = new Matrix(this.output_nodes, this.hidden_nodes);
        this.weights_ih.randomize();
        this.weights_ho.randomize();
        // this.weights_ih.print();
        // this.weights_ho.print();
    
        this.bias_h = new Matrix(this.hidden_nodes, 1);
        this.bias_o = new Matrix(this.output_nodes, 1);
        this.bias_h.randomize();
        this.bias_o.randomize();
        // this.bias_h.print();
        // this.bias_o.print();

        this.learning_rate = 0.1;
    }

    feedForward(input_array){

        // Generating the Hidden
        let inputs = Matrix.fromArray(input_array);
        let hidden = Matrix.multiply(this.weights_ih, inputs);
        hidden.add(this.bias_h);
       
        // Hidden activation function;
        hidden.map(sigmoid);
        hidden.print();

        // Generating the Output
        let output = Matrix.multiply(this.weights_ho, hidden);
        output.add(this.bias_o);  

        // Output activation function
        output.map(sigmoid);    

        return output.toArray();
    }   
    
    // rappel calcul : video n°18 7:16 / demonstration video n°16
    train(inputs_array, targets_array){       
        //let outputs = this.feedForward(inputs);
        // lignes de la fonction feedforward pour remplacer lignre précédente
        let inputs = Matrix.fromArray(inputs_array);
        console.log("inputs");
        inputs.print();
        let hidden = Matrix.multiply(this.weights_ih, inputs);
        hidden.add(this.bias_h);
        hidden.map(sigmoid);
        console.log("hidden");
        hidden.print();
        
        let outputs = Matrix.multiply(this.weights_ho, hidden);
        outputs.add(this.bias_o);  
        outputs.map(sigmoid);
        console.log("outputs");
        outputs.print();
        // remplacé par les 3 lignes précédentes (output devient outputs)
        //outputs = Matrix.fromArray(outputs);
        let targets = Matrix.fromArray(targets_array);
        console.log("targets");
        targets.print();

        // error = target - outputs
        let output_errors = Matrix.subtract(targets, outputs);
        console.log("output_errors  = targets - outputs");
        output_errors.print();
        // let gradients = outputs * (1 - outputs);
        let gradients = Matrix.map(outputs, dsigmoid);
        // gradients.print();        
        gradients.multiply(output_errors);
        // gradients.print();
        gradients.multiply(this.learning_rate);
        // gradients.print();

        // calculate deltas
        let hidden_T = Matrix.transpose(hidden);
        let weights_ho_deltas = Matrix.multiply(gradients, hidden_T);

        // adjust the weights by deltas
        this.weights_ho.add(weights_ho_deltas);
        console.log("weights_ho");
        weights_ho_deltas.print();
        // adjust the weights by its deltas (which is just the gradients)
        this.bias_o.add(gradients);
        console.log("bias_o");
        this.bias_h.print();

        // calculate the hidden layer errors
        let who_t = Matrix.transpose(this.weights_ho);
        let hidden_errors =  Matrix.multiply(who_t, output_errors);

        // calculate hidden gradient
        let hidden_gradient = Matrix.map(hidden, dsigmoid);  
        // hidden_errors.print();
        hidden_gradient.multiply(hidden_errors);
        // hidden_errors.print();        
        hidden_gradient.multiply(this.learning_rate);
        // hidden_errors.print();


        // calculate input->hidden deltas
        let inputs_T = Matrix.transpose(inputs);
        let weights_ih_deltas = Matrix.multiply(hidden_gradient, inputs_T);

        this.weights_ih.add(weights_ih_deltas);
        console.log("weights_ih");
        this.weights_ih.print();
        // adjust the weights by its deltas (which is just the gradients)
        this.bias_h.add(hidden_gradient);
        console.log("bias_h");
        this.bias_h.print();

        // avec plusieurs layers, il faut une boucle (stochastic gradient descent)

        // console.log("inputs");
        // inputs.print();
        // console.log("hidden");
        // hidden.print();
        // console.log("outputs");
        // outputs.print();
        // console.log("targets");
        // targets.print();
        // console.log("output_errors  = targets - outputs");
        // output_errors.print();
        // console.log("gradients");
        // gradients.print();
        // console.log("weights_ho_deltas");
        // weights_ho_deltas.print();
        // console.log("hidden_errors");
        // hidden_errors.print();
        // console.log("hidden_gradient");
        // hidden_gradient.print();
        // console.log("weights_ih_deltas");
        // weights_ih_deltas.print();
    }


} 
