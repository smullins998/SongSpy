function showContainer() {
    const container = document.getElementById("hidden-container");
    container.style.display = "flex";
    animationTimeout = setTimeout(stopAnimation, 8000);
  }
  
