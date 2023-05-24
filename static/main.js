function changeBackgroundColor() {
    var color = getRandomColor();
    document.body.style.backgroundColor = color;
  }
  
  function getRandomColor() {
    var letters = '0123456789ABCDEF';
    var color = '#';
    for (var i = 0; i < 6; i++) {
      color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
  }
  
  setInterval(changeBackgroundColor, 2000); // Change color every 2 seconds


