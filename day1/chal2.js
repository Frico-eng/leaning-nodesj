//Challenge 2: Create a Private Counter with Closure

function createCounter() {
  let count = 0;
  return{
  increment: function() {
    count++
    return count;
  },
  decrement: function() {
    count--
    return count;
  }
}
}
const counter = createCounter();
console.log(counter.increment());//1
console.log(counter.increment());
console.log(counter.decrement());
console.log(counter.increment());
console.log(counter.increment());
console.log(counter.decrement());
console.log(counter.increment());
console.log(counter.increment());
console.log(counter.decrement());
console.log(counter.increment());
console.log(counter.decrement());//3