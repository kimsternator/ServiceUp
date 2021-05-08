document.addEventListener("DOMContentLoaded", (event) => {
  var post = document.getElementById("post");
  var profile = document.getElementById("profile");
  var setting = document.getElementById("setting");
  var messaging = document.getElementById("messaging");
  var messageUser = document.getElementById("messageUser");
  var home = document.getElementById("logo");
  var report = document.getElementById("report");
  
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