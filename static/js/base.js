document.addEventListener("DOMContentLoaded", (event) => {

    var cookies = document.cookie;
    var res = cookies.split(';');
    for (var cookie of res) {
        temp = cookie.split(/=(.+)/);
        console.log(temp)
        if(temp[0] == ' picture') {
            console.log(document.getElementById("profile"))
            var profile = document.getElementById("profile").src = temp[1];
        }
    }

    var post = document.getElementById("post");
    var sign_in = document.getElementById("sign_in");
    var sign_out = document.getElementById("sign_out");
    var profile = document.getElementById("profile");
    var setting = document.getElementById("setting");
    var home_icon = document.getElementById("home_icon");

    post.addEventListener("click", function() {
      console.log("post");
      window.location = ('http://localhost:5000/post');
    });
  
    if (sign_in != null) {
      sign_in.addEventListener("click", function() {
        console.log("sign_in");
        window.location = ('http://localhost:5000/login');
      });
    }
    else if (sign_out != null) {
      sign_out.addEventListener("click", function() {
        console.log("sign_out");
        signOut();
      });
    }
    
    profile.addEventListener("click", function() {
      console.log("profile");
      window.location = ('http://localhost:5000/profile');
    });
    
    setting.addEventListener("click", function() {
      console.log("setting");
    });

    home_icon.addEventListener("click", function() {
        console.log("home icon");
        window.location = ('http://localhost:5000');
      });
    
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