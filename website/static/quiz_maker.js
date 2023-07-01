const ques_container_query = document.querySelector('.ques_conatiner')
const form_ele = document.querySelector(".form")

form_ele.addEventListener('submit', event =>{
    event.preventDefault();

    const formData = new FormData(form_ele)
    const data = Object.fromEntries(formData)


    fetch('http://127.0.0.1:5000/quizmaker', {
        method :'POST',
        headers:{
            'Content-type' : 'application/json'
        },
        body: JSON.stringify(data)
    })
})






