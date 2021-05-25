document.addEventListener("DOMContentLoaded", (event) => {
  var count = 1;
  var offset = 0;
  var dataURL = "http://localhost:6004/get_main_posts/";
  
  loadMore();
  var load_more = document.getElementById("load");
  var search = document.getElementById("searchsubmit");
  
  var filter = false;
  
  load_more.addEventListener("click", function() {
    console.log("load_more");
      loadMore();
  });

  search.addEventListener("click", function() {
    console.log("search");
    clearPosts();
    var query = document.getElementById("searchText").value;
    
    if(query) {
      filter = true;
    }
    else {
      filter = false;
    }
    
    loadMore();
  });
  
  window.onscroll = function(ev) {
    if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight) {
      // you're at the bottom of the page
      loadMore();
    }
  };

  function update(data) {
    var posts = data["posts"];

    for(i = 0; i < posts.length; i++) {
      var thePost = posts[i];

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
      where.innerHTML = "San Diego, CA";
      time.innerHTML = "1" + " hrs ago";
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

        window.location = (base_link + 'listing/?id=' + String(theId));
      });

      col.appendChild(post);
      row.appendChild(col);
    }
  }

  function showError(err) {
    console.log(err);
  } 

  function loadMore() {
    if(filter) {
      console.log("filtering");
    }
    else {
      console.log("no filtering");
      fetch(dataURL + String(offset))
        .then(response=>response.json())
        .then(update)
        .catch(showError)
    }
  }
  
  function postClicked(anId) {
    console.log(anId);
    console.log("here");
  }

  function clearPosts() {
    var rows = document.getElementById("posts");
    
    while (rows.firstChild) {
      rows.removeChild(rows.lastChild);
    }
  }
  
  var count = 1;
});