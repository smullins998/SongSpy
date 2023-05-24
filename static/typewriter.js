document.addEventListener("DOMContentLoaded", function() {
    var element = document.getElementById("output-div");
    var text = "Your text goes here."; // Replace with your desired text
    var speed = 50; // Adjust the speed (in milliseconds) to control typing speed
  
    // Function to animate typing effect
    function typeWriter() {
      if (text.length > 0) {
        element.innerHTML += text.charAt(0);
        text = text.substring(1);
        setTimeout(typeWriter, speed);
      }
    }
  
    typeWriter();
  });
  


