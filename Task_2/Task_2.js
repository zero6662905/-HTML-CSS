function checkEvenOdd(number) {
    if (number % 2 === 0) {
        return "number " + number + " pair.";
    } else {
        return "number " + number + " unmatched.";
    }
}

for (let i = 1; i <= 10; i++) {
    console.log(checkEvenOdd(i));
}