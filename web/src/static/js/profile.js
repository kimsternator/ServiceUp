document.addEventListener("DOMContentLoaded", (event) => {
	var report = document.getElementById("report");
	var msg = document.getElementById("messageUser");
  
	report.addEventListener('click', event => {
	  console.log("report");
	});

	msg.addEventListener('click', event => {
      console.log("message User");
    });
});