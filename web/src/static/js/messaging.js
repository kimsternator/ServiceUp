document.addEventListener("DOMContentLoaded", (event) => {
  var send = document.getElementById("send");
  var message = document.getElementById("theNewMessage");
  var msgURL = baseUrl + "/get_messages";
  var chatURL = baseUrl + "/get_chats";
  var sendMsgURL = baseUrl + "/add_message";
  var offset = 0;
  var theId = 0;
  
  function addChat(data) {
    var theList = document.getElementById("messageList");

    var theItem = document.createElement("div");
    var theName = document.createElement("h1");

    theItem.classList.add("messageListItem");
    theName.classList.add("recipientName");

    theName.innerHTML = data[0];
    theItem.id = data[1]

    theItem.addEventListener("click", event => {
      document.querySelectorAll('.messageListItem').forEach(subitem => {
        if (subitem.classList.contains("active")) {
          if(theItem != subitem) {
            subitem.classList.remove("active");
          }
        } 
      });

      removeMessages();

      if (theItem.classList.contains("active")) {
        document.getElementById("emptyMsg").style.visibility = "visible";
        document.getElementById("emptyMsg").innerHTML = "Please Select a Chat"
        theItem.classList.remove("active");
        offset = 0;
        theId = 0;
      } 
      else {
        document.getElementById("emptyMsg").style.visibility = "hidden";
        document.getElementById("emptyMsg").innerHTML = "There are no messages to display";
        theItem.classList.add("active");
        theId = theItem.id;
        loadMessages();
      }
    });

    theItem.appendChild(theName);
    theList.appendChild(theItem);
  }

  function updateChat(data) {
    var theNames = data["chats"];

    for(i = 0; i < theNames.length; i++) {
      addChat(theNames[i]);
    }
  }

  function showError(err) {
    console.log(err);
  } 

  function loadChats() {
    fetch(chatURL)
      .then(response=>response.json())
      .then(updateChat)
      .catch(showError)
  }

  function addMessages(data) {
    var theData = data["messages"];

    for(i = 0; i < theData.length; i++) {
      offset++;
      if(theData[i][1] == 0) {
        addSenderMessage(theData[i][0]);
      }
      else {
        addRecipientMessage(theData[i][0]);
      }
    }
  }

  function loadMessages(id) {
    fetch(msgURL + "/" + String(id) + "/" + String(offset))
      .then(response=>response.json())
      .then(addMessages)
      .catch(showError)
  }

  function updateMessages(data) {
    loadMessages();
  }

  loadChats();

  function sendMessage(msgText) {    
    fetch(sendMsgURL, {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        'message': msgText,
        "recipient": theId
      })
    })
      .then(updateMessages)
      .catch(showError)
  }
  
  function addSenderMessage(text) {
    var theDiv = document.createElement("div");
    var thep = document.createElement("p");
    
    theDiv.classList.add("senderMessage");
    thep.classList.add("message");
    
    thep.innerHTML = text;
    theDiv.appendChild(thep);
    document.getElementById("allMessages").appendChild(theDiv);
  }
  
  function addRecipientMessage(text) {
    var theDiv = document.createElement("div");
    var thep = document.createElement("p");
    
    theDiv.classList.add("recipientMessage");
    thep.classList.add("message");
    
    thep.innerHTML = text;
    theDiv.appendChild(thep);
    document.getElementById("allMessages").appendChild(theDiv);
  }
  
  function removeMessages() {
    const myNode = document.getElementById("allMessages");
    
    while (myNode.childNodes.length > 3) {
        myNode.removeChild(myNode.lastChild);
    }
  }
  
  send.addEventListener("click", function() {
    var activeChat = false;
  
    document.querySelectorAll('.messageListItem').forEach(item => {
      if (item.classList.contains("active")) {
        activeChat = true;
      } 
    });

    if(activeChat) {
      var messageText = message.value;

      while(messageText[messageText.length - 1] == '\n') {
        messageText = messageText.substring(0, messageText.length - 1);
      }

      sendMessage(messageText);
      message.value = "";
    }
  });
  
  message.addEventListener("keyup", function(event) {
    if(event.which == 13) {
      var activeChat = false;
    
      document.querySelectorAll('.messageListItem').forEach(item => {
        if (item.classList.contains("active")) {
          activeChat = true;
        } 
      });

      if(activeChat) {
        var messageText = message.value;

        while(messageText[messageText.length - 1] == '\n') {
          messageText = messageText.substring(0, messageText.length - 1);
        }
        sendMessage(messageText);
        message.value = "";
      }
    }
  });
  
  setInterval(function(){
    if(theId != 0) {
      loadMessages(theId);
    }
  }, 3000);
});