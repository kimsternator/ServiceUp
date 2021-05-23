document.addEventListener("DOMContentLoaded", (event) => {
  var profileUser = document.getElementById("profileUser");
  var messageUser = document.getElementById("messageUser");

  profileUser.addEventListener("click", function() {
    console.log("profileUser");
  });
  
  messageUser.addEventListener("click", function() {
    console.log("messageUser");
    window.location = (base_link + 'messageuser');
  });
});