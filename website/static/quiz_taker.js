const form_ele = document.querySelector(".form")

form_ele.addEventListener('submit', event =>{
    event.preventDefault();
    const formData = new FormData(form_ele)
    const data = Object.fromEntries(formData)
    // let output = "";
    // for (const entry of data) {
    //   output = `${output}${entry[0]}=${entry[1]}\r`;
    // }
    console.log(data)

    // fetch('http://127.0.0.1:5000/quizmaker', {
    //     method :'POST',
    //     headers:{
    //         'Content-type' : 'application/json'
    //     },
    //     body: JSON.stringify(data)
    // })
})


