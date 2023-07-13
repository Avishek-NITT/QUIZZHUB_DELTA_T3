const frnd_req_container = document.querySelector(".frnd_req_container")


function frnd_req(status, sender_name){
    console.log(status, sender_name)

    const frnd_req_data = {
        "sender_user" : sender_name,
        "request_status": status
    };
    let currentURL = window.location.href;
    fetch(currentURL, {
        method: "POST",
        body: JSON.stringify(frnd_req_data),
        headers: {
           "Content-type": "application/json; charset=UTF-8"
        }
     })
      
     setTimeout(() => {
        location.reload()
      }, 100);
}