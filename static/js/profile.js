document.addEventListener("DOMContentLoaded", (event) => {
  var post = document.getElementById("post");
  var homepage = document.getElementById("homepage");
  var profile = document.getElementById("profile");
  var setting = document.getElementById("setting");
  var messaging = document.getElementById("messaging");
  var messageUser = document.getElementById("messageUser");
  var home = document.getElementById("logo");
  var report = document.getElementById("report");
  
  post.addEventListener("click", function() {
    console.log("post");
    window.location = ('http://localhost:5000/post');
  });
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
  
  home.addEventListener("click", function() {
    console.log("home");
  });
  
  messageUser.addEventListener("click", function() {
    console.log("messageUser");
  });
  
  report.addEventListener("click", function() {
    console.log("report");
  });
});