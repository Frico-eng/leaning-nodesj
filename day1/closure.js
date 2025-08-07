//small script testing some closure concepts
function makeCounter() {
  let count = 0;
  return function () {
    count++;
    return count;
  };
}

const counter = makeCounter();
console.log(counter()); // 1
console.log(counter()); // 2


for (var i = 0; i < 3; i++) {
  setTimeout(function () {
    console.log(i);
  }, 1000);
}
for (let i = 0; i < 3; i++) {
  setTimeout(function () {
    console.log(i);
  }, 1000);
}
