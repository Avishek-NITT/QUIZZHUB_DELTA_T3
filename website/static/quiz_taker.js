const form_ele = document.querySelector(".form")

form_ele.addEventListener('submit', event =>{
    event.preventDefault();
    const formData = new FormData(form_ele)
    const data = Object.fromEntries(formData)
    console.log(data)
    let currentURL = window.location.href;
    fetch(currentURL, {
        method :'POST',
        headers:{
            'Content-type' : 'application/json'
        },
        body: JSON.stringify(data)
    })
})


