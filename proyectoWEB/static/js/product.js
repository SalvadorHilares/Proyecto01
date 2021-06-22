document.getElementById("public_product").onsubmit = function(e){
    e.preventDefault();
    fetch('/publish/product', {
        method : 'POST',
        body : JSON.stringify({
            'name' : document.getElementById('name').value,
            'price' : document.getElementById('price').value,
            'features' : document.getElementById('features').value,
            'TI' : document.getElementById('TI').value,
            'TF' : document.getElementById('TF').value,
            'DNI' : document.getElementById('DNI').value
        }),
        headers : {
            'Content-type' : 'application/json'
        }
    }).then(function(response){
        return response.json()
    }).then(function(jsonResponse){
        console.log(jsonResponse)
        if(jsonResponse['error'] === false){
            const liItem = document.createElement('li')
            const  buttonItem = document.createElement('button')
            buttonItem.innerHTML = "&cross;"
            buttonItem.className = "delete-button"
            buttonItem.setAttribute('data-id',jsonResponse.id)
            liItem.innerHTML = jsonResponse['name'] + ' ' + jsonResponse['price'] + ' ' + jsonResponse['features']
            liItem.appendChild(buttonItem)
            document.getElementById("products").appendChild(liItem)
            document.getElementById('name').value = ''
            document.getElementById('price').value = ''
            document.getElementById('features').value = ''
            document.getElementById("error").className='hidden'
            window.location.reload(true)
        }else{
            document.getElementById("error").className=''
            document.getElementById("error").innerHTML = jsonResponse['error_message']
        }
    }).catch(function(error){
        console.log(error)
        document.getElementById("error").className = ''
    })
}

    const items = document.querySelectorAll('.delete-button')
        for (let i = 0; i < items.length; i++) {
            const item = items[i]
            item.onclick = function(e) {
                console.log('click event: ', e)
                const product_id = e.target.dataset['id'];
                fetch('/product/'+product_id+'/delete-product', {
                    method: 'DELETE'
                }).then(function() {
                    const item = e.target.parentElement
                    item.remove()
                });
            }
        }