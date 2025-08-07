//code snippet testing hoisting, works with functions but not variables

console.log(foo());
function foo(){
    return "hello";
}
console.log(bar);
var bar="world";

console.log(baz);
var baz = "!!!"
//doesn't work because var
sayHello();
var sayHello = function () {
  console.log("Hi");
};

//works because it uses function
sayHello(); 

function sayHello() {
  console.log("Hi");
}