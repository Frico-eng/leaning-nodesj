//small script to test the concept of closure
function createGreeter(name){
    return function(greeting){
        console.log(`${greeting}, ${name}!`);
    }
}

const greetHello = createGreeter("Hello");
greetHello("alice");

const greetOi = createGreeter("Oi");
greetOi("joão");