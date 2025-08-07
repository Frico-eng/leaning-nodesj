const greetJohn = delayedGreeter("John");
greetJohn();  // After 1 second: "Hello, John!"

function delayedGreeter(name){
    return function(){
        setTimeout(function(){console.log(`Hello, ${name}!`)}, 1000);
    }
}
