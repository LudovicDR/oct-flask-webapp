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
        fetchBotResponse(version.value)
    });
    input.value = '';
})

async function fetchBotResponse(version)
{
    const res = await fetch('/bot/' + version);
    const data = await res.json();

    console.log(data.response);
    var to_print = data.response.replaceAll("\n", "<br>");
    console.log(to_print);
    chat.innerHTML += `<div class="row"><div class="col-10 assistantbox"><p style="margin: 0px;">${to_print}</p></div><div class="col-1"></div></div>`;
}