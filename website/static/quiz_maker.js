let ques_count = 1


const form_ele = document.querySelector(".form")

form_ele.addEventListener('submit', event =>{
    event.preventDefault();

    const formData = new FormData(form_ele)
    console.log(formData)
})



