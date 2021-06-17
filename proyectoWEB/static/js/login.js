document.getElementById("login").onsubmit = function(e){
    e.preventDefault();
    fetch('/authenticate/login', {
        method : 'POST',
        body: JSON.stringify({
            'username': document.getElementById('username').value,
            'password': document.getElementById('password').value
        }),
        headers : {
            'Content-Type' : 'application/json'
        },
    }).then(function(response){
        return response.json()
    }).then(function(jsonResponse){
        console.log(jsonResponse)
        if(jsonResponse['error'] === false){
            window.location.replace('/homepage')
        }else{
            window.location.reload()
        }
    })
}