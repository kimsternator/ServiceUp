document.addEventListener("DOMContentLoaded", (event) => {
  var count = 1;
  
  for(j = 0; j < 8; j++) {
    loadMore();
  }
  
  var post = document.getElementById("post");
  var profile = document.getElementById("profile");
  var setting = document.getElementById("setting");
  var load_more = document.getElementById("load");
  
  post.addEventListener("click", function() {
    console.log("post");
  });
  
  profile.addEventListener("click", function() {
    console.log("profile");
  });
  
  setting.addEventListener("click", function() {
    console.log("setting");
  });
  
  load_more.addEventListener("click", function() {
    console.log("load_more");
  });
  
  window.onscroll = function(ev) {
    if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight) {
      // you're at the bottom of the page
      for(i = 0; i < 8; i++) {
        loadMore();
      }
    }
  };
  
  function loadMore() {
    var row = document.getElementById("posts");
    var col = document.createElement("div");
    var post = document.createElement("div");
    var title = document.createElement("div");
    var poster = document.createElement("img");
    var pic = document.createElement("img");
    var desc = document.createElement("ul");
    var serv = document.createElement("li");
    var who = document.createElement("li");
    var when = document.createElement("li");
    var how = document.createElement("li");

    col.classList.add("column");
    post.classList.add("posting");
    title.classList.add("title");
    poster.classList.add("poster");
    pic.classList.add("image");
    desc.classList.add("description");

    poster.src = "https://mpng.subpng.com/20180404/sqe/kisspng-computer-icons-user-profile-clip-art-big-5ac5283827d286.2570974715228703281631.jpg";
    pic.src = "https://images-na.ssl-images-amazon.com/images/I/615%2BvEiuEEL._AC_SL1226_.jpg";
    
    post.id = "post" + count;
    count++;
    
    serv.innerHTML = "Service: " + "lawn mowing";
    who.innerHTML = "Who: " + "anyone";
    when.innerHTML = "When: " + "This Saturday 11am-5pm";
    how.innerHTML = "How much: " + "$25 for both lawns";
    title.innerHTML = "Lawn Mowing Service";
    
    desc.appendChild(serv);
    desc.appendChild(who);
    desc.appendChild(when);
    desc.appendChild(how);
    
    post.appendChild(title);
    post.appendChild(poster);
    post.appendChild(pic);
    post.appendChild(desc)
    
    post.addEventListener('click', event => {
      //handle click
      console.log(post.id);
    });
    
    col.appendChild(post);
    row.appendChild(col);
  }
  
  function postClicked(anId) {
    console.log(anId);
  }
});


function signOut() {
  logout_url = 'http://localhost:5000/logout'

  var xhr = new XMLHttpRequest();
  xhr.open('GET', logout_url);
  xhr.onload = function() {
    console.log('Logged out ' + xhr.responseText);
    window.location.reload();
  };
  xhr.send();
}