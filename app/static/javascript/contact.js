const inputBtn = document.querySelector(".send-btn")
const nameEl = document.querySelector("#name")
const emailEl = document.querySelector("#email")
const messageAreaEl = document.querySelector("#message-text")
const messagesEl = document.querySelector("#messages")

inputBtn.addEventListener("click", function (e) {
  messagesEl.innerHTML = ""
  if (!nameEl.value) {
    e.preventDefault()
    const messageEl = document.createElement("h4")
    messageEl.textContent = "Please input your name"
    messageEl.classList.add("message")
    messagesEl.appendChild(messageEl)
    return false
  } else if (!emailEl.value) {
    e.preventDefault()
    const messageEl = document.createElement("h4")
    messageEl.textContent = "Please input your email address"
    messageEl.classList.add("message")
    messagesEl.appendChild(messageEl)
    return false
  } else if (!messageAreaEl.value) {
    e.preventDefault()
    const messageEl = document.createElement("h4")
    messageEl.textContent = "Please input your message"
    messageEl.classList.add("message")
    messagesEl.appendChild(messageEl)
    return false
  }
})
