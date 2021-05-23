function updateMessages(){
    fetch("http://localhost:6004/get_messages", {
      method: "GET",
      headers: { "Content-Type": "application/json" }
    })
    .then((response) => response.json())
    .then(response => (response['Response (server):']))
    .then(response => displayTelemetry(response))
   }
    window.setInterval(updateTelemetry, 3000 )