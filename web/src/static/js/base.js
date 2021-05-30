var getUrl = window.location;
var baseUrl = getUrl .protocol + "//" + getUrl.host + "/" + getUrl.pathname.split('/')[1];
const base_link = baseUrl + '/'
// const base_link = 'http://localhost:6004/'

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

    function toggleDrop() {
      var drop = document.getElementById("dropDown");
      
      if(drop.style.visibility == "visible") {
        drop.style.visibility = "hidden";
      }
      else {
        drop.style.visibility = "visible";
      }
    }

    var post = document.getElementById("post");
    var profile = document.getElementById("profile");
    var setting = document.getElementById("setting");
    var home_icon = document.getElementById("home_icon");
    var myProfile = document.getElementById("myprof");
    var messaging = document.getElementById("messag");
    var setting = document.getElementById("sett");
    var tos = document.getElementById("tos");
    var pp = document.getElementById("pp");
    var sign_inout = document.getElementById("sign");    

    post.addEventListener("click", function() {
      console.log("post");
      window.location = (base_link + 'new_post');
    });

    sign_inout.addEventListener("click", function() {
      if(sign.innerHTML == "Sign In") {
        console.log("sign_in");
        modal.style.display = "block";
      }
      else {
        console.log("sign_out");
        signOut();
      }
    });
    
    profile.addEventListener("click", function() {
      console.log("profile");
      toggleDrop();
    });
    
    setting.addEventListener("click", function() {
      console.log("setting");
    });

    tos.addEventListener("click", function() {
      console.log("tos");
      window.location = (base_link + 'terms_of_service');
    });

    pp.addEventListener("click", function() {
      console.log("pp");
      window.location = (base_link + 'privacy_policy');
    });

    home_icon.addEventListener("click", function() {
      console.log("home icon");
      window.location = (base_link);
    });

    myProfile.addEventListener("click", function() {
      console.log("my profile");
      window.location = (base_link + 'profile');
    });
    
    messaging.addEventListener("click", function() {
      console.log("messaging");
      window.location = (base_link + 'messaging');
    });
    
    setting.addEventListener("click", function() {
      console.log("setting");
    });
    
    // var modal = document.getElementById("myModal");

    // Get the button that opens the modal
    // var btn = document.getElementById("profile");
    
    // Get the <span> element that closes the modal
    // var span = document.getElementsByClassName("close")[0];
    
    // When the user clicks the button, open the modal 
    // btn.onclick = function() {
    //     modal.style.display = "block";
    // }
    
    // When the user clicks on <span> (x), close the modal
    // span.onclick = function() {
    //     modal.style.display = "none";
    // }
    
    // When the user clicks anywhere outside of the modal, close it
    // window.onclick = function(event) {
    //     if (event.target == modal) {
    //         modal.style.display = "none";
    //     }
    // }
    // });
  
  function signOut() {
    logout_url = base_link + 'logout'
    authInstance = gapi.auth2.getAuthInstance();
    console.log(authInstance)
    authInstance.signOut()
    var xhr = new XMLHttpRequest();
    xhr.open('GET', logout_url);
    xhr.onload = function() {
      console.log('Logged out ' + xhr.responseText);
      document.cookie = "picture=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
      document.cookie = "email=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
      document.cookie = "name=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
      window.location.reload();
    };
    xhr.send();
  }
});

function init(){
  console.log('Init success')
  gapi.load('auth2', function() {
    gapi.auth2.init().then(() => {  })
  });
}

function onSignIn(googleUser) {
  var profile = googleUser.getBasicProfile();
  console.log('ID: ' + profile.getId()); // Do not send to your backend! Use an ID token instead.
  console.log('Name: ' + profile.getName());
  console.log('Image URL: ' + profile.getImageUrl());
  console.log('Email: ' + profile.getEmail()); // This is null if the 'email' scope is not present.

  var id_token = googleUser.getAuthResponse().id_token;
  login_url = base_link + 'login'

  var xhr = new XMLHttpRequest();
  xhr.open('POST', login_url);
  xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
  xhr.onload = function() {
    console.log(xhr.responseText);
    google_info = JSON.parse(xhr.responseText);
    console.log('Signed in as: ' + google_info['picture']);

    var temp = `picture=${google_info['picture']}`
    document.cookie = temp;
    console.log(temp)
    console.log(document.cookie)

    temp = `email=${google_info['email']}`;
    document.cookie = temp;
    console.log(temp)
    console.log(document.cookie)

    temp = `name=${google_info['name']}`;
    document.cookie = temp;
    console.log(temp)
    console.log(document.cookie)

    temp = `email=${google_info['email']}`;
    document.cookie = temp;
    console.log(temp)
    console.log(document.cookie)

    window.location = (base_link);
  };
  xhr.send('idtoken=' + id_token);
}