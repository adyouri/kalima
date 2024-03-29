function add_to_favorites(post_id) {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
     var icon = document.getElementById("favorite-icon")
     icon.style.color = "red";
     icon.setAttribute("title", "Remove from favorites")
     icon.setAttribute("onclick", "remove_from_favorites("+post_id+")")


     reload_list_of_fav_users(post_id)
    
    }
  };
  xhttp.open("GET", "/posts/" + post_id + "/fav", true);
  xhttp.send();
} 

function remove_from_favorites(post_id) {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
     var icon = document.getElementById("favorite-icon")
     icon.style.color = "grey";
     icon.setAttribute("title", "Add to favorites")
     icon.setAttribute("onclick", "add_to_favorites("+post_id+")")

     reload_list_of_fav_users(post_id)

    }
  };
  xhttp.open("GET", "/posts/" + post_id + "/unfav", true);
  xhttp.send();
}


function reload_list_of_fav_users(post_id){
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
     var resault = JSON.parse(xhttp.responseText);
     var users = resault.fav_users_list
     var fav_users = document.getElementById("fav-users")
     fav_users.innerHTML = "";
     for(i = 0; i < users.length; i++){
         var li = document.createElement("li");
         var user = document.createTextNode(users[i]);
         li.appendChild(user);
         fav_users.appendChild(li);
      }
    }
  }
  xhttp.open("GET", "/posts/" + post_id + "/fav_users", true);
  xhttp.send();
};

function set_follow_button_state(user, current_user){

  // if the username is not in the followers list then set button to 'follow'
  // if the username is in the followers list then set button to 'unfollow'

  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {

     var resault = JSON.parse(xhttp.responseText);
     var users = resault.followers;

     var element = document.getElementById("follow-btn")
     
     
     if (users.indexOf(current_user) == -1) { // the current user is not following the user (so it's 'follow')
         element.innerHTML = "follow " + user
         element.setAttribute("class", "label label-info")
         element.setAttribute("onclick", "follow('"+user+"')")

     } else {
         element.innerHTML = "unfollow " + user
         element.setAttribute("class", "label label-danger")
         element.setAttribute("onclick", "unfollow('"+user+"')")

     }

    }
  }
  xhttp.open("GET", "/users/" + user + "/followers", true);
  xhttp.send();
};





















function follow(username) {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
     var element = document.getElementById("follow-btn")
     element.setAttribute("class", "label label-danger")
     element.setAttribute("onclick", "unfollow('"+username+"')")
     element.innerHTML = "unfollow " + username


        //reload_list_of_followers(username)
    
    }
  };
  xhttp.open("GET", "/users/" + username + "/follow", true);
  xhttp.send();
}


function unfollow(username) {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
     var element = document.getElementById("follow-btn")
     element.setAttribute("class", "label label-info")
     element.setAttribute("onclick", "follow('"+username+"')")
     element.innerHTML = "follow " + username

        //reload_list_of_followers(username)
    
    }
  };
  xhttp.open("GET", "/users/" + username + "/unfollow", true);
  xhttp.send();
}
