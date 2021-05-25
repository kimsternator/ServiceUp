const base_link = 'http://localhost:6004/'

function onSignIn(googleUser) {
  var profile = googleUser.getBasicProfile();
  console.log('ID: ' + profile.getId()); // Do not send to your backend! Use an ID token instead.
  console.log('Name: ' + profile.getName());
  console.log('Image URL: ' + profile.getImageUrl());
  console.log('Email: ' + profile.getEmail()); // This is null if the 'email' scope is not present.

  var id_token = googleUser.getAuthResponse().id_token;
  login_url = base_link + 'login'

  var xhr = new XMLHttpRequest();
  xhr.open('POST', login_url);
  xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
  xhr.onload = function() {
    console.log(xhr.responseText);
    google_info = JSON.parse(xhr.responseText);
    console.log('Signed in as: ' + google_info['picture']);

    var temp = `picture=${google_info['picture']}`
    document.cookie = temp;
    console.log(temp)
    console.log(document.cookie)

    temp = `email=${google_info['email']}`;
    document.cookie = temp;
    console.log(temp)
    console.log(document.cookie)

    temp = `name=${google_info['name']}`;
    document.cookie = temp;
    console.log(temp)
    console.log(document.cookie)

    temp = `email=${google_info['email']}`;
    document.cookie = temp;
    console.log(temp)
    console.log(document.cookie)

    window.location = (base_link);
  };
  xhr.send('idtoken=' + id_token);
}