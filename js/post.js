document.addEventListener("DOMContentLoaded", (event) => {
  var post = document.getElementById("post");
  var profile = document.getElementById("profile");
  var setting = document.getElementById("setting");
  var messaging = document.getElementById("messaging");
  var profileUser = document.getElementById("profileUser");
  var messageUser = document.getElementById("messageUser");
  var home = document.getElementById("logo");
  
  post.addEventListener("click", function() {
    console.log("post");
  });
  
  profile.addEventListener("click", function() {
    console.log("profile");
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