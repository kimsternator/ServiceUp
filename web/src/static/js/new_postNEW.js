function preview_images(event) {
  var previews = document.getElementById('imageStart');

  while (previews.firstChild) {
    previews.removeChild(previews.lastChild);
  }

  function readAndPreview(file) {
    var reader = new FileReader();

    reader.onload = function() {
      var newDiv = document.createElement("div");
      var image = document.createElement("img");
      
      image.classList.add("preview");
      image.src    = reader.result;
      newDiv.appendChild(image);
      previews.appendChild(newDiv);
    };
    
    reader.readAsDataURL(file);
  }
    
  if (event.target.files) {
    [].forEach.call(event.target.files, readAndPreview);
  }
  else {
    console.log("Invalid file(s)");
  }
}

document.getElementById('title').onkeyup = function () {
  document.getElementById('titleCount').innerHTML = this.value.length;
};

document.getElementById('city').onkeyup = function () {
  document.getElementById('cityCount').innerHTML = this.value.length;
};

document.getElementById('tag').onkeyup = function () {
  document.getElementById('tagCount').innerHTML = this.value.length;
};

document.getElementById('desc').onkeyup = function () {
  document.getElementById('descCount').innerHTML = this.value.length;
};

var post = document.getElementById("post");
var profile = document.getElementById("profile");
var setting = document.getElementById("setting");
var messaging = document.getElementById("messaging");
var messageUser = document.getElementById("messageUser");
var home = document.getElementById("logo");
var report = document.getElementById("report");

post.addEventListener("click", function() {
  console.log("post");
});

profile.addEventListener("click", function() {
  console.log("profile");
});

setting.addEventListener("click", function() {
  console.log("setting");
});

messaging.addEventListener("click", function() {
  console.log("messaging");
});

home.addEventListener("click", function() {
  console.log("home");
});