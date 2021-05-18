const base_link = 'http://localhost:6004/'

document.addEventListener("DOMContentLoaded", (event) => {
  var count = 1;
  
  for(j = 0; j < 12; j++) {
    loadMore();
  }
  var load_more = document.getElementById("load");
  
  load_more.addEventListener("click", function() {
    console.log("load_more");
    for(i = 0; i < 12; i++) {
        loadMore();
      }
  });
  
  window.onscroll = function(ev) {
    if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight) {
      // you're at the bottom of the page
      for(i = 0; i < 12; i++) {
        loadMore();
      }
    }
  };
  
  function loadMore() {
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
    
    pic.src = "https://images-na.ssl-images-amazon.com/images/I/615%2BvEiuEEL._AC_SL1226_.jpg";
    
    
    title.innerHTML = "Lawn Mowing Service";
    where.innerHTML = "San Diego, CA";
    time.innerHTML = "1" + " hrs ago";
    
    post.id = "post" + count;
    count++;
    
    post.appendChild(pic);
    post.appendChild(title);
    post.appendChild(where);
    post.appendChild(time);
    
    post.addEventListener('click', event => {
      console.log(post.id);
      window.location = (base_link + '/post');
    });
    
    col.appendChild(post);
    row.appendChild(col);
  }
  
  function postClicked(anId) {
    console.log(anId);
    console.log("here");
  }
});