document.addEventListener("DOMContentLoaded", (event) => {
  var submit = document.getElementById("Submit");
  
  submit.addEventListener('click', event => {
    var ele = document.getElementsByName('Accept');

    for(i = 0; i < ele.length; i++) {
      if(ele[i].checked) {
        console.log(ele[i].value);
      }
    }
  });
});