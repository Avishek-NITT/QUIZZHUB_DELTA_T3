const modal = document.querySelector(".upload_modal")
const uploaded_image = document.querySelector(".uploaded_image")
let htmlmarkup =""

function input_clicked(){
    upload_modal.showModal()
}

function close_modal(){
    localStorage.removeItem("my-image");
    upload_modal.close()
    uploaded_image.value = null;
}


uploaded_image.addEventListener("change", function(){

    localStorage.removeItem("my-image");
    const fr = new FileReader()
    fr.readAsDataURL(uploaded_image.files[0])
    fr.addEventListener('load', () =>{
        localStorage.removeItem("my-image");
        const url = fr.result
        localStorage.setItem('my-image', url)
        const imageElement = document.createElement('img');
        imageElement.setAttribute("class", "show_image")
        const imageUrl = localStorage.getItem('my-image');
        console.log(imageUrl)
        imageElement.src = imageUrl;
        modal.appendChild(imageElement);
    })

    
})