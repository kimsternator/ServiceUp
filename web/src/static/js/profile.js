const database_query_endpoint = 'get_posts'

document.addEventListener("DOMContentLoaded", (event) => {
	var report = document.getElementById("report");
	var msg = document.getElementById("messageUser");

	report.addEventListener('click', event => {
		console.log("report");
	});

	msg.addEventListener('click', event => {
		console.log("message User");
	});

	load_posts(getCookie('email'))
});

/* https://stackoverflow.com/questions/10730362/get-cookie-by-name */
function getCookie(name) {
	const value = `; ${document.cookie}`;
	const parts = value.split(`; ${name}=`);
	if (parts.length === 2) return parts.pop().split(';').shift();
}

function load_posts(email) {
	var xhr = new XMLHttpRequest();
	xhr.open('GET', base_link + database_query_endpoint + '?email=' + email);
	xhr.onload = function () {
		response = JSON.parse(xhr.responseText);
		console.log(response);
		render_posts(response)
	};
	xhr.send();
}

function render_posts(data) {
	var posts = data;
	console.log('got here')
	for (i = 0; i < posts.length; i++) {
		var thePost = posts[i];
		console.log(thePost)

		var row = document.getElementById("posts");
		var col = document.createElement("div");
		var post = document.createElement("div");
		var title = document.createElement("div");
		var pic = document.createElement("img");
		var where = document.createElement("div");
		var time = document.createElement("div");

		col.classList.add("column");
		post.classList.add("posting");
		title.classList.add("title");
		pic.classList.add("image");
		where.classList.add("loc");
		time.classList.add("time");

		pic.src = thePost[8][0];
		title.innerHTML = thePost[2];
		where.innerHTML = thePost[6];
		time.innerHTML = thePost[7];
		post.id = thePost[0];
		post.appendChild(pic);
		post.appendChild(title);
		post.appendChild(where);
		post.appendChild(time);

		post.addEventListener('click', event => {
			var theId;

			if (event.target.parentNode.className == "column") {
				theId = event.target.id;
			}
			else {
				theId = event.target.parentNode.id;
			}

			window.location = (base_link + 'listing?id=' + String(theId));
		});

		col.appendChild(post);
		row.appendChild(col);
	}
}