document.addEventListener("DOMContentLoaded", (event) => {
  var homepage = document.getElementById("homepage");
  var profile = document.getElementById("profile");
  var setting = document.getElementById("setting");
  var messaging = document.getElementById("messaging");
  var profileUser = document.getElementById("profileUser");
  var messageUser = document.getElementById("messageUser");
  var home = document.getElementById("logo");
  
  homepage.addEventListener("click", function() {
    console.log("homepage");
    window.location = ('http://localhost:5000/');
  });
  
  profile.addEventListener("click", function() {
    console.log("profile");
    window.location = ('http://localhost:5000/profile');
  });
  
  setting.addEventListener("click", function() {
    console.log("setting");
  });
  
  messaging.addEventListener("click", function() {
    console.log("messaging");
  });
  
  profileUser.addEventListener("click", function() {
    console.log("profileUser");
  });
  
  messageUser.addEventListener("click", function() {
    console.log("messageUser");
  });
  
  home.addEventListener("click", function() {
    console.log("home");
  });
});