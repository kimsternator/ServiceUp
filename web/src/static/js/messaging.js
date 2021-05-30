var getUrl = window.location;
var baseUrl = getUrl .protocol + "//" + getUrl.host + "/" + getUrl.pathname.split('/')[1];

function updateMessages(){
    fetch(baseUrl + "/get_messages", {
      method: "GET",
      headers: { "Content-Type": "application/json" }
    })
    .then((response) => response.json())
    .then(response => (response['Response (server):']))
    .then(response => displayTelemetry(response))
   }
    window.setInterval(updateTelemetry, 3000 )