document.getElementById("form").onsubmit = function(e) {
    e.preventDefault();
    fetch('/users/create', {
        method: 'POST',
        body: JSON.stringify({
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
            const liItem = document.createElement('li')
            liItem.innerHTML = jsonResponse['name'] + ' ' + jsonResponse['email'] + ' ' + jsonResponse['password']
            document.getElementById("users").appendChild(liItem)
            document.getElementById('name').value = ''
            document.getElementById('email').value = ''
            document.getElementById('password').value = ''
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