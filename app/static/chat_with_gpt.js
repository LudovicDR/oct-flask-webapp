// chat_with_gpt.js

const form = document.getElementById('message-form');
const input = document.getElementById('message');
const version = document.getElementById('model_version');
const chat = document.getElementById('chat');

form.addEventListener('submit', e => {
    e.preventDefault();

    fetch('/message/' + version.value, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({message: input.value})
    }).then(res => res.json())
    .then(data => {
        chat.innerHTML += `<div class="row"><div class="col-1"></div><div class="col-10 userbox">${data.message}</div></div>`
        chat.innerHTML += `<div class="row"><div class="col-10 assistantbox" id="content_${chat.childElementCount+1}">Rédaction de la réponse...</div><div class="col-1"></div></div>`;
        new_fetchBotResponse(version.value)
    });
    input.value = '';
})

async function fetchBotResponse(version)
{
    const res = await fetch('/bot/' + version);
    const data = await res.json();

    //console.log(data.response);
    var to_print = data.response.replaceAll("\n", "<br>");
    //console.log(to_print);
    chat.innerHTML += `<div class="row"><div class="col-10 assistantbox">${to_print}</div><div class="col-1"></div></div>`;
}

function new_fetchBotResponse(version)
{
    var messageDiv = document.getElementById("content_" + chat.childElementCount);
    var source = new EventSource("/bot/" + version);

    source.onopen = (e) => console.log("Connection opened");
    source.addEventListener("start", function(e) { messageDiv.innerHTML = ""; });
    source.onerror = (e) => console.log("Error:", e);
    source.onmessage = (e) => {
        var msg = JSON.parse(e.data);
        //console.log("data=" + msg.text + "/§/");
        messageDiv.innerHTML += msg.text.replaceAll("\n", "<br/>");
    }
    source.addEventListener("end", function(e) { source.close(); });
}