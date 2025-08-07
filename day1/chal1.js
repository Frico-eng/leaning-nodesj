//Challenge 1: Fix the Closure in a Loop


// for (var i = 0; i < 5; i++) {
//   setTimeout(function () {
//     console.log(i);
//   }, i * 100);
// }

// Explain why it prints 5 five times.
// Modify the code so it prints 0, 1, 2, 3, 4 with the same timing.

// i believe it prints 5 times because the for loop uses var i = 0, this causes a closure problem where a new instance is started on every loop as a result it prints the first number 5 times
// to fix it we should replace "var i" with "let i"
//here's the fixed code
for (let i = 0; i < 5; i++) {
  setTimeout(function () {
    console.log(i);
  }, i * 100);
}
