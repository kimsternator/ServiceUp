function preview_image(event) {
  var reader = new FileReader();

  reader.onload = function() {
    var output = document.getElementById('preview');
    output.src = reader.result;
  };

  reader.readAsDataURL(event.target.files[0]);
}

function sendToServ() {
  var dict = {};
  var serv = document.getElementById("serv");
  var who = document.getElementById("who");
  var when = document.getElementById("when");
  var how = document.getElementById("how");
  var desc = document.getElementById("desc");
  
  dict[serv.id] = serv.value;
  dict[who.id] = who.value;
  dict[when.id] = when.value;
  dict[how.id] = how.value;
  dict[desc.id] = desc.value;
  
  console.log(JSON.stringify(dict));
}

document.getElementById('serv').onkeyup = function () {
  document.getElementById('servCount').innerHTML = this.value.length;
};

document.getElementById('who').onkeyup = function () {
  document.getElementById('whoCount').innerHTML = this.value.length;
};

document.getElementById('when').onkeyup = function () {
  document.getElementById('whenCount').innerHTML = this.value.length;
};

document.getElementById('how').onkeyup = function () {
  document.getElementById('howCount').innerHTML = this.value.length;
};

document.getElementById('desc').onkeyup = function () {
  document.getElementById('descCount').innerHTML = this.value.length;
};