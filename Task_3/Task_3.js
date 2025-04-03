document.addEventListener('DOMContentLoaded', function() {
    const colors = ["red", "blue", "green", "yellow", "purple"];
    let currentIndex = 0;

    document.getElementById('colorButton').addEventListener('click', function() {
        document.body.style.backgroundColor = colors[currentIndex];
        currentIndex = (currentIndex + 1)
    });
});