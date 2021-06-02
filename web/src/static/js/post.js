document.addEventListener("DOMContentLoaded", (event) => {
  var dataURL = base_link + "add_chat/";
  var removeURL = base_link + "remove_post/";
  var profileUser = document.getElementById("profileUser");
  var messageUser = document.getElementById("messageUser");
  var mac = document.getElementById("markAsComplete");
  var postHead = document.getElementById("postHead");

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

  function showResponse(data) {
    alert(data["message"]);

    if(data["message"] == "success") {
      window.location = base_link;
    }
  }

  mac.addEventListener("click", function() {
    fetch(removeURL + String(postHead.getAttribute("data-src")))
      .then(response=>response.json())
      .then(showResponse)
      .catch(showError)
  });
});