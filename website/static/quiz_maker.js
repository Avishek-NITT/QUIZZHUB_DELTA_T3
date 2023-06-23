let count = 1
const cont = document.querySelector(".container")
htmlmarkup = ""
function add_ques(){
    count ++;
    htmlmarkup = `<label> Question ${count} </label>
    <input type="text" id="question${count}" name="question"/><br>`
    cont.innerHTML += htmlmarkup
}



