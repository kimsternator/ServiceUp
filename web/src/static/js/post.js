document.addEventListener("DOMContentLoaded", (event) => {
  var dataURL = baseUrl + "/add_chat/";
  var profileUser = document.getElementById("profileUser");
  var messageUser = document.getElementById("messageUser");

  profileUser.addEventListener("click", function() {
    console.log("profileUser");
  });

  function update(data) {
    if(data["message"] == "success") {
      window.location = ("/messaging");
    }
    else {
      alert(data["message"]);
    }
  }

  function showError(err) {
    console.log(err);
  } 
  
  messageUser.addEventListener("click", function() {
    fetch(dataURL + String(document.getElementById("posterID").innerHTML))
      .then(response=>response.json())
      .then(update)
      .catch(showError)
  });
});