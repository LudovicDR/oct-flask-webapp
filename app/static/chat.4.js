// chat.js

const form = document.getElementById('message-form')
const input = document.getElementById('message')
const chat = document.getElementById('chat')

form.addEventListener('submit', e => {
    e.preventDefault()

    fetch('/message_4', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({message: input.value})
    }).then(res => res.json())
    .then(data => {
        chat.innerHTML += `<div class="row"><div class="col-1"></div><div class="col-10 userbox">${data.message}</div></div>`
        fetchBotResponse()
    })
    input.value = ''
})

async function fetchBotResponse() {
  const res = await fetch('/bot_4')
  const data = await res.json()

  chat.innerHTML += `<div class="row"><div class="col-10 assistantbox">${data.response}</div><div class="col-1"></div></div>`
}