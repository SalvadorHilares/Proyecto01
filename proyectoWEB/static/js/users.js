document.getElementById("register").onsubmit = function(e) {
    e.preventDefault();
    fetch('/users/create', {
        method: 'POST',
        body: JSON.stringify({
            'DNI' : document.getElementById('DNI').value,
            'name': document.getElementById('name').value,
            'email': document.getElementById('email').value,
            'password': document.getElementById('password').value
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(function(response){
        return response.json()
    }).then(function(jsonResponse) {
        console.log(jsonResponse)
        if (jsonResponse['error'] === false) {
            var dni = jsonResponse['dni'].toString()
            window.location.replace('/homepage/'+dni)
            document.getElementById("error").className='hidden'
        } else {
            document.getElementById("error").className=''
            document.getElementById("error").innerHTML = jsonResponse['error_message']
        }
    }).catch(function(error) {
        console.log(error)
        document.getElementById("error").className=''
    });
};