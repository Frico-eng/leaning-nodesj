//predict the following outputs
//format my "prediction | real answer"

console.log(foo);//undefined|undefined
var foo = "bar";

console.log(baz);//undefined|ReferenceError: Cannot access 'baz' before initialization
let baz = "qux";

sayHello();//Hello!|Hello!

function sayHello() {
  console.log("Hello!");
}

sayBye();//undefined|TypeError: sayBye is not a function

var sayBye = function () {
  console.log("Bye!");
};
