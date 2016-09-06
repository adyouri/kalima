function add_to_favorites(post_id) {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
     document.getElementById("favorite-icon").style.color = "red";
    }
  };
  xhttp.open("GET", "/posts/" + post_id + "/fav", true);
  xhttp.send();
} 
