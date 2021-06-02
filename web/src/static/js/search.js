var getUrl = window.location;
var baseUrl = getUrl .protocol + "/" + getUrl.host + "/" + getUrl.pathname.split('/')[1];

document.addEventListener("DOMContentLoaded", (event) => {
  var offset = 0;
  var dataURL = base_link + "get_filter/";
  
  loadMore();
  var load_more = document.getElementById("load");
  var search = document.getElementById("searchsubmit");
  
  load_more.addEventListener("click", function() {
    console.log("load_more");
    loadMore();
  });

  search.addEventListener("click", function() {
    console.log("search");
    var query = document.getElementById("searchText").value;
    window.location.href = "/search?filter=" + query;
  });
  
  window.onscroll = function(ev) {
    if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight) {
      // you're at the bottom of the page
      loadMore();
    }
  };

  function update(data) {
    var posts = data["posts"];
    console.log(data);

    for(i = 0; i < posts.length; i++) {
      var thePost = posts[i];
      offset++;

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

      pic.src = thePost["image_url"];
      title.innerHTML = thePost["title"];
      where.innerHTML = thePost["city"];
      time.innerHTML = thePost["elapsed"] + " hrs ago";
      post.id = thePost["id"];
      post.appendChild(pic);
      post.appendChild(title);
      post.appendChild(where);
      post.appendChild(time);
      
      post.addEventListener('click', event => {
        var theId;

        if(event.target.parentNode.className == "column") {
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

    if(offset == 0) {
        document.getElementById("noResults").style.visibility = "visible";
    } 

    if(offset < 11) {
      document.getElementById("load").style.visibility = "hidden";
    }
  }

  function showError(err) {
    console.log(err);
  } 

  function loadMore() {
    var theFilterReq = document.getElementById("filter").innerHTML;

	  fetch(dataURL + String(offset) + "/" + theFilterReq.substring(23))
	    .then(response=>response.json())
	    .then(update)
	    .catch(showError)
  }
  
  function postClicked(anId) {
    console.log(anId);
    console.log("here");
  }
});