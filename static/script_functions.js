function runFunction1() {
    fetch('/function1')
        .then(response => response.text())
        .then(result => alert('Function 1 Result: ' + result))
        .catch(error => console.error(error));
}

function runFunction2() {
    fetch('/function2')
        .then(response => response.text())
        .then(result => alert('Function 2 Result: ' + result))
        .catch(error => console.error(error));
}
