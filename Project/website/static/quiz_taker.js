const form_ele = document.querySelector(".form")
const score_displayer = document.getElementById("modal_text")


form_ele.addEventListener('submit', event =>{
    event.preventDefault();
    const formData = new FormData(form_ele)
    const data = Object.fromEntries(formData)
    let currentURL = window.location.href;
    fetch(currentURL, {
        method :'POST',
        headers:{
            'Content-type' : 'application/json'
        },
        body: JSON.stringify(data)
    })

    score_display_modal.showModal() 
})


function redirectTo(url) {
    window.location.href = url;
  }

function retake_quiz(){
    location.reload()
}



