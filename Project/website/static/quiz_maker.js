const ques_container_query = document.querySelector('.ques_container')
const form_ele = document.querySelector(".form")

let ques_count = 1
let htmlmarkup = ""

form_ele.addEventListener('submit', event =>{
    event.preventDefault();
    const formData = new FormData(form_ele)
    const data = Object.fromEntries(formData)
    if(check_quiz(data,ques_count)){

    }else{
        return
    }
    fetch('http://127.0.0.1:5000/quizmaker', {
        method :'POST',
        headers:{
            'Content-type' : 'application/json'
        },
        body: JSON.stringify(data)
    })
})

function add_ques(){
    if(ques_count === 5){
        alert("Cannot add more than 5 questions")
        return 
    }
    ques_count++
    const element = document.getElementById("add_que_btn")
    element.remove()
    let ques_box = document.createElement("div")
    htmlmarkup = ""
    htmlmarkup += `

            <h3> Question ${ques_count} </h3>
            <input type="text" class="text text2" id="question${ques_count}" name="question${ques_count}"/>
            <br>
            <label class="text2"> Enter Correct option </label> 
            <br>
            <input class="text text2" type="text" id="q${ques_count}_c1" name="q${ques_count}_c1"/>
            <br>
            <label class="text2"> Enter other options </label><br>
            <input class="text text2" type="text" id="q${ques_count}_c2" name="q${ques_count}_c2"/>
            <br>
            <br>
            <input class="text text2" type="text" id="q${ques_count}_c3" name="q${ques_count}_c3"/>
            <br>
            <br>
            <input class="text text2" type="text" id="q${ques_count}_c4" name="q${ques_count}_c4"/> 
    `
    ques_box.innerHTML = htmlmarkup
    ques_box.classList.add("question")
    ques_box.classList.add("secondary_question")
    ques_box.setAttribute('id', `question${ques_count}`)
    // ques_container_query.innerHTML += htmlmarkup
    ques_container_query.appendChild(ques_box)
    ques_box = document.createElement("button")
    htmlmarkup = "+"
    ques_box.innerHTML = htmlmarkup
    ques_box.setAttribute('id', "add_que_btn")
    ques_box.setAttribute('onclick', "add_ques();")
    ques_container_query.appendChild(ques_box)
}



function check_quiz(data, total_ques){
    if (!data.quiz_name){
        alert("Quiz must have a name")
        return 0
    }
    if(!data.quiz_desc){
        alert("Quiz must have a description")
        return 0
    }
    
    for (let ques_counter = 1; ques_counter <= total_ques ; ques_counter++){
        if (!data[`question${ques_counter}`]) {
            alert(`Question ${ques_counter} is not provided`);
            return 0;
          }
        for(let i = 1; i < 5 ; i++){
            if(!data[`q${ques_counter}_c${i}`]){
                alert("Fill in all the options")
                return 0 
            }
        }
    }
    return 1
}






