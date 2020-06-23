// https://www.w3schools.com/howto/howto_js_toggle_hide_show.asp

const showhide = () => {
    var x = document.getElementById("showhide");
    if (x.style.display === "block") {
      x.style.display = "none";
    } else {
      x.style.display = "block";
    }
  }