var a = 1;

function outer() {
  var a = 2;

  function inner() {
    a++;
    var a = 3;
    console.log(a);
  }

  inner();
}

outer();
//i believe it will 3 twice|it print 3 only once

//due to holstering 
// a++;
// var a = 3;
// console.log(a);
//becomes
// var a -> undefined;
// a++ -> nan;
// a = 3;
// console.log(a)->3;