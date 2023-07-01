const ques_container_query = document.querySelector('.ques_container')
const form_ele = document.querySelector(".form")

let ques_count = 1
let htmlmarkup = ""

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


function add_ques(){
    console.log("Hello")
    if(ques_count === 5){
        alert("Cannot add more than 5 questions")
        return 
    }
    ques_count++
    const element = document.getElementById("add_que_btn")
    element.remove()
    htmlmarkup = ""
    htmlmarkup += `
    <div class="question" id="question${ques_count}">
            <h3> Question ${ques_count} </h3>
            <input type="text" class="text2" id="question${ques_count}" name="question${ques_count}"/>
            <br>
            <label class="text2"> Enter Correct option </label> 
            <br>
            <input class="text2" type="text" id="q${ques_count}_c1" name="q${ques_count}_c1"/>
            <br>
            <label class="text2"> Enter other options </label><br>
            <input class="text2" type="text" id="q${ques_count}_c2" name="q${ques_count}_c2"/>
            <br>
            <br>
            <input class="text2" type="text" id="q${ques_count}_c3" name="q${ques_count}_c3"/>
            <br>
            <br>
            <input class="text2" type="text" id="q${ques_count}_c4" name="q${ques_count}_c4"/>
        </div>
        <button id="add_que_btn" onclick="add_ques()">+</button>
    `
    ques_container_query.innerHTML += htmlmarkup
}






